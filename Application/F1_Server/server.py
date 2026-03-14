# Python 3 server example

import time
import requests
import json
import http.client
from pymongo import MongoClient
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from datetime import date
from pydantic import BaseModel
import paho.mqtt.client as mqtt
import ssl
from urllib.request import urlopen
import json
#CONNECTION MANAGER TO ALLOW FOR OUR WEBSOCEKTS TO BE USED

app = FastAPI()


origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )


class ConnectionManager:
  def __init__(self):
    self.active_connections: list[WebSocket] = []

  async def connect(self,websocket: WebSocket):
    await websocket.accept()
    print("We should have connected to the websocket!!!")
    self.active_connections.append(websocket)

  async def disconnect(self, websocket: WebSocket):
    self.active_connections.remove(websocket)
  async def send_personal_message(self,message: str, websocket: WebSocket):
    await websocket.send_text(message)
  async def broadcast(self,message):
    print("We are broadcasting the message")
    print("Active connections:", len(self.active_connections))
    for connection in self.active_connections:
      await connection.send_json(message)
    print("Working??")


manager = ConnectionManager()
loop = None
#This is going to be used for live telem
token_url = "https://api.openf1.org/token"
paramsLive_Telem = {
    "username": "joelines194@gmail.com",
    "password": "BlTLAeNSZNu6pavN"
}
response_F1= requests.post(token_url,data=paramsLive_Telem)

#This is working
if response_F1.status_code == 200:
  response = response_F1.json()
  access_token = response["access_token"]


#Hyprace is going to be used for everything else

response = http.client.HTTPSConnection("hyprace-api.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "6d3141966dmsh933f874f2dc3823p144d62jsn81e5fa2d240f",
    'x-rapidapi-host': "hyprace-api.p.rapidapi.com",
   'Accept': "application/json",
    }



clientDatabase = MongoClient()

#Get the current year
Year = date.today().year

clientDatabase = MongoClient("mongodb://username:password@database:27017/Drivers?authSource=admin")
newdatabase = clientDatabase["Drivers"]
Driver_Lap_Times = newdatabase["Driver_Lap_Times"]
Races = newdatabase['Races']
#we need to store the standings after each race in the database
Drivers_Standings = newdatabase["Drivers_Standings"]
Teams_Standings = newdatabase["Teams_Standings"]
Driver_Names = newdatabase["Driver_Names"]
Team_Names = newdatabase["Team_Names"]
SessionData = newdatabase["SessionData"]
RaceResults = newdatabase["RaceResults"]
def on_connect(client, userdata, flags, rc, properties = None):
  print("we are here!!")
  if rc == 0:
        #we can change all of this shit
        print("Connected to OpenF1 MQTT broker")
        #client.subscribe("v1/location")
        #client.subscribe("v1/laps")
        client.subscribe("v1/laps")
        client.subscribe("v1/race_control")
        client.subscribe("v1/car_telemetry")
        print(client.subscribe("v1/laps"))
        print(client.subscribe("v1/race_control"))
        print(client.subscribe("v1/car_telemetry"))
        #client.subscribe("#")
  else:
    print(f"Failed to connect, return code {rc}")
  
#AFTER THE RACE HAS FINISHED WE NEED TO BE UPDATING STANDINGS AS WELL AS UPDATING RACE RESULTS - THIS IS IMPERITIVE - Also need to get the ML model running after qualifying

SessionType = ""
def on_message(client,userdata,msg):
  #global SessionType
  print("We have recived a message for OpenF1 API!!!")
  data = json.loads(msg.payload.decode())
  print(data)

  #Get the session type based on the ID for the live timings
  
  if SessionType == "":
    response = requests.get(f"https://api.openf1.org/v1/sessions?session_key={data["session_key"]}",headers={"Authorization": f"Bearer {access_token}"})
    data2 = response.json()
    print(data2)
    SessionData.delete_many({})
    SessionType = data2[0]["session_name"]
  if SessionType == "Sprint Qualifying" or SessionType == "Qualifying":
    PresentQualifyingData(data)
  if SessionType == "Practice 1" or SessionType == "Practice 2" or SessionType == "Practice 3":
    PresentPracticeData()

  if SessionType == "Main Race":
    print(data)

  print(SessionType)
  #Check what the actual thing is for this
  #if SessionType == "Race Sprint":
    #PresentRace_Data(data)
  
#def PresentRace_Data(RaceData):



#This is looking like it is done which is fantastic
def PresentQualifyingData(DataQualifying):
  #Convert the lap time back to zero
  x = (SessionData.find_one({"driver_number" : DataQualifying["driver_number"]}))
  print(x)
  
  if "message" in DataQualifying and "qualifying_phase" in DataQualifying:
    if DataQualifying["message"] == "SESSION FINISHED":
      print("delete all data from that collection")
      global SessionType
      SessionType = ""
      SessionData.delete_many({})
      print("success maybe???")
      #we delete all data from qualifying
  else:
    x = list(SessionData.find({"driver_number" : DataQualifying["driver_number"]}))
    print(x)
    
    if x == [] and DataQualifying["lap_duration"] != None:
      SessionData.insert_one(DataQualifying)
    
    
    elif x[0]["lap_duration"] <= DataQualifying["lap_duration"] and DataQualifying["lap_duration"] != None :
      #Aim of this is to delete laptimes which are old - and replace with new ones
      SessionData.delete_one({"driver_number" : x[0]["driver_number"]})
      SessionData.insert_one(DataQualifying)
      print("Success!!")
    #WE NEED TO TRIGER A WEBSOCKET HERE to get data back -
    
  GetCurrentSessionsData()

def GetCurrentSessionsData():
  print("We are here and need to be")
  x = list(SessionData.find())
  print(x)
  asyncio.run_coroutine_threadsafe(manager.broadcast({"type" : "qyalifying_update", "data": x }), loop)

#def UpdateSessionStatus():

#We know what this data will look like
def PresentPracticeData():
  print("This is where we present practice data")
  #We need to put all of the data into the database then based on new data compare that drivers old times and see if it is faster then replace and send a response to the client

mqtt_broker = "mqtt.openf1.org"
mqtt_port = 8883
mqtt_username = "joelines194@gmail.com"

client = mqtt.Client()
client.username_pw_set(username=mqtt_username, password=access_token)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
client.tls_insecure_set(False)
client.on_connect = on_connect
client.on_message = on_message


def GetStandings(newData):
  data = []
  teams = []
  for i in newData["items"]:  
    teams.append({
        "name": i["name"],
        "team_position": i["constructors"][0]["standing"]["position"],
        "points": i["constructors"][0]["standing"]["points"]
      })
    for j in i["drivers"]:
          if j["drivingLevel"] == "GrandPrix":
            if "standing" in j:
              data.append({
                "name" : j["firstName"] + " " + j["lastName"],
                "id" : j["id"],
                "position": j["standing"]["position"],
                "points": j["standing"]["points"]
              }
              )
  return [data,teams]

# THIS is ready for the race in China - This is important
async def UpdateStandings():
  season = await CurrentSeason()
  response = requests.get(f"https://hyprace-api.p.rapidapi.com/v2/seasons/{season}/teams?pageSize=25", headers=headers)

  data = response
  newData = data.json()
  dataStore = GetStandings(newData)
  #we need to add the date each time that we store the data
 
  for i in dataStore[0]:      
    i["timestamp"] = str(datetime.today().strftime("%y-%m-%d"))
  x = Drivers_Standings.insert_many(dataStore[0])

  for j in dataStore[1]:
    j["timestamp"] = str(datetime.today().strftime("%y-%m-%d"))
  x = Teams_Standings.insert_many(dataStore[1])
  #print("We are here!!")

#Function to get the standings back

#This is the function which got all of the races and stored them in the database
async def functionStoreRaces():
  page = 1
  while True:
    response = requests.get(f"https://hyprace-api.p.rapidapi.com/v2/grands-prix?pageNumber={page}",headers=headers)
    data = response
    newData = data.json()
    #print(newData)
    #Loop through all items
    mylist = []
    for item in newData["items"]:
      items = {"Raceid" : item["id"],"round" : item["round"],"name" : item["name"],"season" : item["season"]["year"], "Eventid": item["schedule"][0]["id"] }
      mylist.append(items)
      #print(items)
   # print(newData["hasNext"])
    
    x = Races.insert_many(mylist)
   
    
    if newData["hasNext"] != True:
      break
    
    page = page + 1

#if i get this done tommorow,that might be better - because more API requests
async def GetRaceResults():
  #We need to get all of the race results from the Races section first off, then loop through and apply all of the items that we need 
  #we could also send a request to get the drivers name but i think it would be better downloading becuase i highly doubt we are going to have enough API requests for that
  x = list(Races.find({}))
  myList = []
  for item in x:
    #print(item)
    response = requests.get(f"https://hyprace-api.p.rapidapi.com/v2/grands-prix/{item["Raceid"]}/races/{item["Eventid"]}/results", headers=headers)

    #print("Right place")
    #c0c47b04-21d3-4765-c8fa-08d94ab130d2
    data  = response.json()
    #print(data)
    #print(data)
    if (data["participations"] != [] ):
        for individual_results in data["participations"]:
          #we need to sort through the data, would be better if it was individual rows          
          if "time" in individual_results["result"] and "gapToLeader" not in individual_results["result"]:
            items = {"Raceid" : item["Raceid"],"Eventid": item["Eventid"], "Driverid" : individual_results["driverId"], "Teamid" : individual_results["teamId"], "FinishedPostion" : individual_results["result"]["finishedPosition"], "Finaltime": individual_results["result"]["time"],"points": individual_results["result"]["points"],"laps": individual_results["result"]["laps"],"gapToLeader": 0 }
            myList.append(items)
          if "time" in individual_results["result"] and "gapToLeader" in individual_results["result"]:
            print(individual_results["result"])
            items = {"Raceid" : item["Raceid"],"Eventid": item["Eventid"], "Driverid" : individual_results["driverId"], "Teamid" : individual_results["teamId"], "FinishedPostion" : individual_results["result"]["finishedPosition"], "Finaltime": individual_results["result"]["time"],"points": individual_results["result"]["points"],"laps": individual_results["result"]["laps"],"gapToLeader": individual_results["result"]["gapToLeader"] }
            myList.append(items)
          else:
            items = {"Raceid" : item["Raceid"],"Eventid": item["Eventid"], "Driverid" : individual_results["driverId"], "Teamid" : individual_results["teamId"], "FinishedPostion" : individual_results["result"]["finishedPosition"], "Finaltime": "N/A","points": individual_results["result"]["points"],"laps": individual_results["result"]["laps"],"gapToLeader": "N/A" }
            myList.append(items)
          print(items) 
          

      
    
  xin = RaceResults.insert_many(myList)
  print("Indatabase")
    
       
  
async def GetTeams():
  #print("We want to go through all of the pages and put the teams inside of the mongodb database")
 # print("73ee4826-7cf7-410e-a4c0-eb48b2f4ae79")
  page = 1
  
  while True:
    response = requests.get(f"https://hyprace-api.p.rapidapi.com//v2/teams?pageSize=25&pageNumber={page}", headers=headers)
    data = response
    newData = data.json()
    #print(newData)
    #Loop through all items
    mylist = []
    
    for item in newData["items"]:
      if "fullName" in item:
        items = {"teamid" : item["id"], "fullName" : item["fullName"], "color" : item["color"], "country" : item["country"]["name"], "countryshort" : item["country"]["alphaThreeCode"]}
        mylist.append(items)
        print(items)
      else:
        items = {"teamid" : item["id"], "fullName" : item["name"]}
        mylist.append(items)
    #print(newData["hasNext"])
    
    x = Team_Names.insert_many(mylist)
   
    
    if newData["hasNext"] != True:
      break
    
    page = page + 1
    


async def GetDrivers():
  """
  #response = requests.get("https://hyprace-api.p.rapidapi.com/v2/drivers/8a99b5a0-8e1a-4bbc-2155-08d9161fe7c5", headers=headers)
  response = requests.get("https://hyprace-api.p.rapidapi.com//v2/drivers?pageSize=25&pageNumber=1", headers=headers)
  
  data = response
  newData = data.json()

  print(newData)
  print("e78d2503-7af4-4f96-1ec3-08d9161fe7c5")
  """
  page = 1
  while True:
    response = requests.get(f"https://hyprace-api.p.rapidapi.com//v2/drivers?pageSize=25&pageNumber={page}", headers=headers)
    data = response
    newData = data.json()
    print(newData)
    #Loop through all items
    mylist = []
    for item in newData["items"]:
      items = {"driverid" : item["id"], "firstName" : item["firstName"], "lastName" : item["lastName"], "birthdate" : item["birthDate"], "country" : item["country"]["name"], "countryshort" : item["country"]["alphaThreeCode"]}
      mylist.append(items)
      #print(items)
    #print(newData["hasNext"])
    
    x = Driver_Names.insert_many(mylist)
   
    
    if newData["hasNext"] != True:
      break
    
    page = page + 1
  

#We probably will be fine just storing them  
async def CurrentSeason():
  response = requests.get("https://hyprace-api.p.rapidapi.com/v2/seasons?year=2026", headers=headers)
  data = response
  newData = data.json()
  return newData["items"][0]["id"]

async def CheckAPIStrings():
  response = requests.get("https://hyprace-api.p.rapidapi.com/v2/grands-prix/87cbb3ec-830b-4fa4-849d-6db01c1461fb/races/3969ed3f-e874-4d18-a621-f3e2bfe060d3/results", headers=headers)

  print("Right place")
  #c0c47b04-21d3-4765-c8fa-08d94ab130d2
  data  = response.json()
  print(data)

  
  #print(response.json())

class GetRaceR(BaseModel):
  EventID: str
  RaceID: str

class SeasonYearData(BaseModel):
  year: int

@app.on_event("startup")
def startup_mqtt():
  try:
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_start()
    global loop
    loop = asyncio.get_running_loop()
    print("MQTT connection started")
  except Exception as e:
        print("MQTT failed:", e)

@app.get("/F1_Statistics")
async def root():

  arrayDrivers = []
  arrayDriverNames = []
  ConstructorData = []
  season = await CurrentSeason()
  #await CheckAPIStrings()
  response = requests.get(f"https://hyprace-api.p.rapidapi.com/v2/seasons/{season}/teams?pageSize=25", headers=headers)
  #await UpdateStandings()
  data = response
  newData = data.json()

  data = []
  sendJSON = GetStandings(newData)
    
  return sendJSON
#Might need to return the races in order but we can do this no problem
@app.get("/F1_Standings_Over_Time")
async def root():
  #code that gets all of the data needed back from the database
  x = list(Drivers_Standings.find({"timestamp" : {"$regex": "26"}}).sort({"timestamp": 1}))
  list(x)

  for data in x:
    data["_id"] = str(data["_id"])

  y = list(Teams_Standings.find({"timestamp" : {"$regex": "26"}}).sort({"timestamp": 1}))
  list(y)
  for data in y:
    data["_id"] = str(data["_id"])

  data = [x,y]

  return data


#Historical is looking good also need to get race results based on id, need to store in database

async def WebsocketSend_Test():
  #print("This is running")
  #print (f"Broadcasting to {len(manager.active_connections)} clients")
  if loop:
    print("There is a loop")
    asyncio.run_coroutine_threadsafe(manager.broadcast({"type" : "qualifying_update", "data": "This is somedatahahaha" }), loop)
  else:
    print("No loop")


def GetRaceResults():
  print("Getting race results here...")
  #we have the id associated with races, we can use it 

@app.post("/GetData")
def root(Data: GetRaceR):
  x = list(RaceResults.find({'Raceid': Data.RaceID, "Eventid" : Data.EventID }))
  print("We are here!")
  myList = []
  #Here we need to get the driver name as well as the team name
  
  for d in x:
    TN = Team_Names.find_one({"teamid" : d["Teamid"]})
    DN = Driver_Names.find_one({"driverid" : d["Driverid"]})
    DriverData = {"raceid" : d["Raceid"], "Eventid" : d["Eventid"], "Driverid" : d["Driverid"], "FinishedPosition" : d["FinishedPostion"], "Finaltime" : d["Finaltime"],"DriverName" : DN["firstName"] + " " + DN["lastName"], "country": DN["countryshort"], "fullName" : TN["fullName"], "country": TN['countryshort'], "colour" : TN["color"]  }
    print(DriverData)
    myList.append(DriverData)

  return myList

@app.post("/Historical")
async def root(Data: SeasonYearData):
  #await GetTeams()
  #await GetRaceResults()
  

  #await WebsocketSend_Test()
  #await GetRaceResults()
  """
  PresentQualifyingData({'meeting_key': 1280, 'session_key': 11236, 'driver_number': 18, 'lap_number': 2, 'date_start': '2026-03-13T07:32:44.269000', 'duration_sector_1': 25.675, 'duration_sector_2': 30.157, 'duration_sector_3': 42.546, 'i1_speed': 277, 'i2_speed': 267, 'is_pit_out_lap': False, 'lap_duration': 98.378, 'segments_sector_1': [2049, 2049, 2049, 2049, 2049, 2049, 2049], 'segments_sector_2': [2049, 2049, 2049, 2049, 2049, 2049], 'segments_sector_3': [2049, 2049, 2049, 2049, 2049, 2049, 2049, 2049, 2049, 2049], 'st_speed': 310, '_key': '11236_2_18', '_id': 1773387264612})
  
  PresentQualifyingData( {'meeting_key': 1280, 'session_key': 11236, 'date': '2026-03-13T07:59:00.269000+00:00', 'driver_number': None, 'lap_number': None, 'category': 'SessionStatus', 'flag': None, 'scope': None, 'sector': None, 'qualifying_phase': 2, 'message': 'SESSION FINISHED', '_key': '1773388740269_None_None_SessionStatus_None_None_None', '_id': 1773388742443})
  """
 

  #Get the data based on the year
  x = list(Races.find({'season': Data.year}))
  x = list(x)
  for races in x:
    races["_id"] = str(races["_id"])
    
  return x






@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
  try:
    await websocket.accept()
    manager.active_connections.append(websocket)
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was {data}")
  except:
     manager.active_connections.remove(websocket)

  
@app.get("/testaba")
def root():
  #await GetTeams()
  #await GetRaceResults()
  
  #await WebsocketSend_Test()
  print("We have reached test")
  GetCurrentSessionsData()