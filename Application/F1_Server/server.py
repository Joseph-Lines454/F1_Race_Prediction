# Python 3 server example


from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import requests
import json
import http.client
from pymongo import MongoClient
#We want to put all of this datawithin the mongoDB database so we dont have to make to many API calls

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

HOST = "0.0.0.0"
PORT = 8001

#Get all current drivers from a list and find them in the database, if they are not in the database, then we can get all of the laptimes related to that driver

class NeuralHTTP(BaseHTTPRequestHandler):

  
 

  def do_OPTIONS(self):           
        self.send_response(200, "ok")       
        self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header("Access-Control-Allow-Headers", "*")        
        self.end_headers()
  def do_GET(self):
    print("Connected!")

    
    if self.path == "/F1_Statistics":
      mydict = { "name": "John", "address": "Highway 27" }

      x = newcollection.insert_one(mydict)
      data = newcollection.find_one()
      print(data)
      self.F1_Statistics()
      
  

  
  def F1_Statistics(self):
    #Get current constructors standings
    #Get map the ID's to the drivers name
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
    print(newData)


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
    self.send_response(200)
    self.do_OPTIONS()
    return self.wfile.write(json.dumps(sendJSON).encode('utf-8'))

  def do_POST(self):
    

    self.send_response(200)
    self.send_header("Content-type","application/json")
    self.end_headers()

    date = time.strftime("%Y-%M-%D %H:%M:%S", time.localtime(time.time()))
    self.wfile.write(bytes('{"time"}: "' + date + '"}',"utf-8"))

 

print("Server is now working!")

server = HTTPServer((HOST,PORT), NeuralHTTP)
server.serve_forever()


print("Hello!!!")