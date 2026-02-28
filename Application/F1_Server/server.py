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


#we want to make a check that if each year has not been added 

client = MongoClient()

#Get the current year
Year = date.today().year

client = MongoClient("mongodb://username:password@database:27017/Drivers?authSource=admin")
newdatabase = client["Drivers"]
Driver_Lap_Times = newdatabase["Driver_Lap_Times"]
TimingsCollection = newdatabase['Race_Schedule']

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
#token_url = "https://api.openf1.org/token"
#params = {
#    "username": "joelines194@gmail.com",
#    "password": "BlTLAeNSZNu6pavN"
#}
#response_F1= requests.post(token_url,data=params)#

#if response_F1.status_code == 200:
#  response = response_F1.json()
#  access_token = response["access_token"]

#conn = http.client.HTTPSConnection("hyprace-api.p.rapidapi.com")

#headers = {
#    'x-rapidapi-key': "6d3141966dmsh933f874f2dc3823p144d62jsn81e5fa2d240f",
#    'x-rapidapi-host': "hyprace-api.p.rapidapi.com"
#}


#Hyprace is going to be used for everything else

response = http.client.HTTPSConnection("hyprace-api.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "6d3141966dmsh933f874f2dc3823p144d62jsn81e5fa2d240f",
    'x-rapidapi-host': "hyprace-api.p.rapidapi.com",
   'Accept': "application/json",
    }



class SeasonYearData(BaseModel):
  id: str




@app.get("/F1_Statistics")
def root():
  arrayDrivers = []
  arrayDriverNames = []
  ConstructorData = []
 

 
  response = requests.get("https://hyprace-api.p.rapidapi.com/v2/seasons/3d24e122-216e-4328-abcf-0af0c5f3fb9e/teams", headers=headers)
  data = response
  newData = data.json()


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
          })
          
    
  sendJSON = [data,teams]
    
  return sendJSON



#Championship Might have to do this with sportsradar

@app.get("/Historical")
def root():
  StartYear = 1950
  #Get the current year
  Year = date.today().year
  #Fill an array with the current Years and Return Them - Save on API requests
  DatesList = list(range(StartYear,Year))



  #response = requests.get("https://hyprace-api.p.rapidapi.com/v2/seasons", headers=headers)
  #data = response
  #newData = data.json()
  #print(newData)
  
  return DatesList


#Constructors Standings Implemented





#@app.post("/seasonRaces")
#async def root(Data: SeasonYearData):
  
 
  



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