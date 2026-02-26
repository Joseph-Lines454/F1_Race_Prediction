# Python 3 server example

import time
import requests
import json
import http.client
from pymongo import MongoClient
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

client = MongoClient()

client = MongoClient("mongodb://username:password@database:27017/Drivers?authSource=admin")
newdatabase = client["Drivers"]
newcollection = newdatabase["Driver_Lap_Times"]


response = http.client.HTTPSConnection("hyprace-api.p.rapidapi.com")
headers = {
   'x-rapidapi-key': "6d3141966dmsh933f874f2dc3823p144d62jsn81e5fa2d240f",
    'x-rapidapi-host': "hyprace-api.p.rapidapi.com",
    'Acccept': 'application/json'
}



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

@app.get("/F1_Statistics")
def root():
  arrayDrivers = []
  arrayDriverNames = []
  ConstructorData = []
  headers = {
   'x-rapidapi-key': "6d3141966dmsh933f874f2dc3823p144d62jsn81e5fa2d240f",
    'x-rapidapi-host': "hyprace-api.p.rapidapi.com"
    }

  headers = {
    'x-rapidapi-key': "6d3141966dmsh933f874f2dc3823p144d62jsn81e5fa2d240f",
    'x-rapidapi-host': "hyprace-api.p.rapidapi.com",
   'Accept': "application/json",
    }

  response.request("GET", "/v2/seasons/3d24e122-216e-4328-abcf-0af0c5f3fb9e/teams", headers=headers)
  data = response.getresponse().read()
  newData = json.loads(data)  


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

@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
   await websocket.accept()
   while True:
      data = await websocket.receive_text()
      await websocket.send_text(f"Message text was {data}")
