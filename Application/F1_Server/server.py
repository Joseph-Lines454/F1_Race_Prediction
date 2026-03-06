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


def on_connect(client, userdata, flags, rc, properties = None):
  print("we are here!!")
  if rc == 0:
        #we can change all of this shit
        print("Connected to OpenF1 MQTT broker")
        client.subscribe("v1/location")
        client.subscribe("v1/laps")
        # client.subscribe("#") # Subscribe to all topics
  else:
    print(f"Failed to connect, return code {rc}")
  

def on_message(client,userdata,msg):
  print("We have recived a message for OpenF1 API!!!")


mqtt_broker = "mqtt.openf1.org"
mqtt_port = 8883
mqtt_username = "joelines194@gmail.com"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username=mqtt_username, password=access_token)
client.tls_set(tls_version=ssl.PROTOCOL_TLS)
#client.on_connect = on_connect
#client.on_message = on_message





client.on_connect = on_connect
client.on_message = on_message



#This is the function which got all of the races and stored them in the database
async def functionStoreRaces():
  page = 1
  while True:
    print("page")
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
 

  await GetLiveData()
  response = requests.get("https://hyprace-api.p.rapidapi.com/v2/seasons/3d24e122-216e-4328-abcf-0af0c5f3fb9e/teams?pageSize=20", headers=headers)


  data = response
  newData = data.json()
  #print(newData)

  count = 0
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
            data.append({
              "name" : j["firstName"] + " " + j["lastName"],
              "id" : j["id"],
              "position": j["standing"]["position"],
              "points": j["standing"]["points"]
            }
            )
            print(j["firstName"])

          
    
  sendJSON = [data,teams]
    
  return sendJSON



#Championship Might have to do this with sportsradar

@app.post("/Historical")
async def root(Data: SeasonYearData):
  
  #Get the data based on the year
  x = list(Races.find({'season': Data.year}))
  
  #x = list(x)
  for races in x:
    races["_id"] = str(races["_id"])
    
  
  return x

###THIS SECTION IS FOR LIVE DATA















#@app.post("/seasonRaces")
#async def root(Data: SeasonYearData):
  
 
  

#We want to request new data every minete but for now will just use HTTP requests





  #sendJSON = [data,teams]
    
  #return sendJSON
"""
@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
   await websocket.accept()
   while True:
      data = await websocket.receive_text()
      await websocket.send_text(f"Message text was {data}")

      
"""




# So we want get all of the drivers lap times for each race they competed in
# We need to get a list of all drivers,
# Then we need to query the APi for each of the drivers data
# Store that in database and figure out the rest.
# But we also need to do it in a way which ensures that we can keep getting the drivers data after the race.cccccccc