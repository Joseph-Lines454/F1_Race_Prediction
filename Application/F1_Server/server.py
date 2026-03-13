# Python 3 server example

import time
import requests
import json
import http.client
from pymongo import MongoClient

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from datetime import date
from pydantic import BaseModel
import paho.mqtt.client as mqtt
import ssl
from urllib.request import urlopen
import json
#we want to make a check that if each year has not been added 

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )


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
def on_connect(client, userdata, flags, rc, properties = None):
  print("we are here!!")
  if rc == 0:
        #we can change all of this shit
        print("Connected to OpenF1 MQTT broker")
        #client.subscribe("v1/location")
        #client.subscribe("v1/laps")
        client.subscribe("v1/laps")
        client.subscribe("v1/race_control")
  else:
    print(f"Failed to connect, return code {rc}")
  
#AFTER THE RACE HAS FINISHED WE NEED TO BE UPDATING STANDINGS AS WELL AS UPDATING RACE RESULTS - THIS IS IMPERITIVE - Also need to get the ML model running after qualifying


def on_message(client,userdata,msg):
  print("We have recived a message for OpenF1 API!!!")
  data = json.loads(msg.payload.decode())
  print(data)
  #response = requests.get(f"https://api.openf1.org/v1/sessions?session_key={data["session_key"]}",headers={"Authorization": f"Bearer {access_token}"})
  #data2 = response.json()
  #print(data2)

mqtt_broker = "mqtt.openf1.org"
mqtt_port = 8883
mqtt_username = "joelines194@gmail.com"

client = mqtt.Client()
client.username_pw_set(username=mqtt_username, password=access_token)
client.tls_set()

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
    if (data["participations"] != []):
        for individual_results in data["participations"]:
          #we need to sort through the data, would be better if it was individual rows
          if "time" in individual_results["result"]:
            items = {"Raceid" : item["Raceid"],"Eventid": item["Eventid"], "Driverid" : individual_results["driverId"], "Teamid" : individual_results["teamId"], "FinishedPostion" : individual_results["result"]["finishedPosition"], "Finaltime": individual_results["result"]["time"],"points": individual_results["result"]["points"],"laps": individual_results["result"]["laps"],"gaptoleader": individual_results["result"]["gapToLeader"] }
            myList.append(items)
          else:
            items = {"Raceid" : item["Raceid"],"Eventid": item["Eventid"], "Driverid" : individual_results["driverId"], "Teamid" : individual_results["teamId"], "FinishedPostion" : individual_results["result"]["finishedPosition"], "Finaltime": "N/A","points": individual_results["result"]["points"],"laps": individual_results["result"]["laps"],"gaptoleader": individual_results["result"]["gapToLeader"] }
            myList.append(items)
          #print(items) 
     
  
    break    
  
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


class SeasonYearData(BaseModel):
  year: int

@app.on_event("startup")
def startup_mqtt():
  try:
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_start()
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

@app.post("/Historical")
async def root(Data: SeasonYearData):
  #await GetTeams()
  #await GetRaceResults()
  #Get the data based on the year
  x = list(Races.find({'season': Data.year}))
  
  x = list(x)
  for races in x:
    races["_id"] = str(races["_id"])
    
  return x





"""
@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
   await websocket.accept()
   while True:
      data = await websocket.receive_text()
      await websocket.send_text(f"Message text was {data}")

      
"""
