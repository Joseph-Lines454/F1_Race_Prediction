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


def on_connect(client, userdata, flags, rc, properties = None):
  print("we are here!!")
  if rc == 0:
        #we can change all of this shit
        print("Connected to OpenF1 MQTT broker")
        #client.subscribe("v1/location")
        #client.subscribe("v1/laps")
        client.subscribe("#") # Subscribe to all topics
  else:
    print(f"Failed to connect, return code {rc}")
  
#AFTER THE RACE HAS FINISHED WE NEED TO BE UPDATING STANDINGS AS WELL AS UPDATING RACE RESULTS - THIS IS IMPERITIVE - Also need to get the ML model running after qualifying
def on_message(client,userdata,msg):
  print("We have recived a message for OpenF1 API!!!")


mqtt_broker = "mqtt.openf1.org"
mqtt_port = 8883
mqtt_username = "joelines194@gmail.com"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username=mqtt_username, password=access_token)
client.tls_set(tls_version=ssl.PROTOCOL_TLS)

client.on_connect = on_connect
client.on_message = on_message


def GetStandings(newData):
  data = []
  teams = []
  for i in newData["items"]:  
    teams.append({
        "name": i["name"],
        "team_position": i["constructors"][0]["standing"]["position"],
        "team_points": i["constructors"][0]["standing"]["points"]
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
  print("We are here!!")

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
      items = {"id" : item["id"],"round" : item["round"],"name" : item["name"],"season" : item["season"]["year"]}
      mylist.append(items)
      #print(items)
    #print(newData["hasNext"])
    #break
    x = Races.insert_many(mylist)
    
    if newData["hasNext"] != True:
      break

    page = page + 1




#We probably will be fine just storing them  
async def CurrentSeason():
  response = requests.get("https://hyprace-api.p.rapidapi.com/v2/seasons?year=2026", headers=headers)
  data = response
  newData = data.json()
  return newData["items"][0]["id"]

async def GetLiveData():
  response = requests.get("https://api.openf1.org/v1/position?meeting_key=1217&position<=3", headers=paramsLive_Telem)
  


  
  #print(response.json())


class SeasonYearData(BaseModel):
  year: int

@app.on_event("startup")
def startup_mqtt():
  try:
    client.connect(mqtt_broker, mqtt_port,60)
    client.loop_start()
  except:
    print("computer says no")

@app.get("/F1_Statistics")
async def root():

  arrayDrivers = []
  arrayDriverNames = []
  ConstructorData = []
  season = await CurrentSeason()
  await GetLiveData()
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
