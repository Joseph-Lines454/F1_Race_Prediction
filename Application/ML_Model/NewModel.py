import polars as pl
import numpy as np
import torch
from torch import nn
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import f1_score
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import requests
import joblib
import json
#We still need to do some pre-proccessing to the data - For qualifying data we need to use an arbitary value with out binary indicator flag (Reached Q2 ect)
#Values also need to be encoded because some are in string formats which ML models do not like

class QualifyingData(BaseModel):
  driverId: str
  teamId: str
  q1: str
  q2: Optional[str] = None
  q3: Optional[str] = None
  gridposition: Optional[str] = None
  circuitId: str
  date: str

class F1_Race_Prediction(nn.Module):
  def __init__(self):
    super(F1_Race_Prediction, self).__init__()
    self.Input1 = nn.Linear(26, 136)
    self.relu1 = nn.Tanh()
    self.Input2 = nn.Linear(136, 136)
    self.relu2 = nn.Tanh()
    #self.dropout = nn.Dropout(0)
    # its because we are returning an output
    self.Input4 = nn.Linear(136,4)
    #Our 4 classes currently are outputed and given a probability via softmax - dim1 makes sure its applied across the class scores.
   

  def forward(self,x):
    out = self.Input1(x)
    out = self.relu1(out)
    out = self.Input2(out)
    out = self.relu2(out)
    out = self.Input4(out)
    #out = self.activitation(out)
    return torch.argmax(out, dim=1)

def ConvertToMilliSeconds(time):
  minutes, seconds = time.split(":")
  total_time_in_ms = int(minutes) * 60 * 100 + float(seconds) * 1000
  return int(total_time_in_ms)

def WeatherDataRes(lat,lng,date):
  WeatherData = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline" + "/" + str(lat) + "," + str(lng) + "/" + date + "?key=HAWRLDPJJULW8C79XWHQGZP2F&include=current")

  
  WeatherData = json.loads(WeatherData.text)
  #We now need to get weather data
  return WeatherData


def DataPrepANDRunModel(QualiData):
  GetData = [[1170,"5d86760d-5842-4ca1-214d-08d9161fe7c5",11111,"d5802ec3-7d45-4b65-b83b-fbb496f87b2d",2,2026,2,17,"08/03/2026",31.3389,121.22,75.8,54.4,63.9,75.8,54.4,0,0,0,18.8,169.6,60,1,1,1,1,1,79435,78811,80120,5]]

  GetData = pl.DataFrame(GetData, schema=["raceId",	"driverId","qualifyId","constructorId","grid","year","Race_round","circuitId","date","lat","lng","tempmax","tempmin","temp","dew","humidity",	"precip",	"snow",	"snowdepth","windspeed","winddir","cloudcover","ReachedQ2","ReachedQ3","Finished Race","SetQ1Time","Finished_Race","Q2_Millsec","Q3_Millsec","Q1_Millsec","race_time_hr"

  ])

  GetData = pl.read_csv("F1_Data/Prerace_Prediction.csv", separator=",", encoding="latin1",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)

  Data = GetData.filter(pl.col('circuitId').cast(pl.Utf8) == QualiData[0].circuitId)
  lng = float(Data['lng'][0])
  lat = float(Data['lat'][0])

  WeatherData = WeatherDataRes(lat,lng,QualiData[0].date)
  #now manipulation needs to be done on oter data
  
  data = [WeatherData['days'][0]['tempmax'], WeatherData['days'][0]['tempmin'], WeatherData['days'][0]['temp'],WeatherData['days'][0]['dew'],WeatherData['days'][0]['humidity'], WeatherData['days'][0]['precip'], WeatherData['days'][0]['snow'],WeatherData['days'][0]['snowdepth'],WeatherData['days'][0]['windspeed'],WeatherData['days'][0]['winddir'], WeatherData['days'][0]['pressure'],WeatherData['days'][0]['cloudcover'],WeatherData['days'][0]['visibility']]


  WeatherData = {"tempmax": WeatherData['days'][0]['tempmax'], "tempmin": WeatherData['days'][0]['tempmin'], "temp":WeatherData['days'][0]['temp'], "dew" : WeatherData['days'][0]['dew'], "humidity": WeatherData['days'][0]['humidity'], "precip": WeatherData['days'][0]['precip'], "snow": WeatherData['days'][0]['snow'], "snowdepth": WeatherData['days'][0]['snowdepth'], "windspeed":WeatherData['days'][0]['windspeed'], "winddir": WeatherData['days'][0]['winddir'], "pressure": WeatherData['days'][0]['pressure'], "cloudcover": WeatherData['days'][0]['cloudcover'], 'visibility': WeatherData['days'][0]['visibility']}


  #Then we need to get the data - we need to get year out of that fuuck...


  #Get Qualifying ID
  QualifyingId = int(GetData["qualifyId"][-1])

  RaceId = int(GetData["raceId"][-1] + 1)
  #Get Round
  RaceRound = int(GetData["Race_round"][-1] + 1)


  MyList = []
  for item in QualiData:
    #convert each qualitime into a milliseconds then get assign a onehot encoding value for each column
    QualifyingId = QualifyingId + 1
    #format date

    #split the string into date and year, then with the date part [0] split it in year,month and date then reassemble using the other date format
    year, month, day = item.date.split("T")[0].split("-")
    finalDate = f"{year}"
    # Have to get race time hr - Missing vairable
    item = item.dict()
    if item.get("q3") is not None:
      items = {"driverId" : str(item.get("driverId")),"constructorId": str(item.get("teamId")), "Q1_Millsec" : ConvertToMilliSeconds(item.get("q1")), "Q2_Millsec" : ConvertToMilliSeconds(item.get("q2")), "Q3_Millsec": ConvertToMilliSeconds(item.get("q3")), "grid": item.get("position"), "circuitId": str(item.get("circuitId")),"year": str(finalDate),"ReachedQ3" : "1", "ReachedQ2": "1", "SetQ1Time": "1", "raceId": str(RaceId), "qualifyId" : str(QualifyingId), "lat": str(lat), "lng" :str(lng), "Race_round": str(RaceRound) }
      items = items | WeatherData
      MyList.append(items)

    elif item.get("q2") is not None:
      
      items = {"driverId" : str(item.get("driverId")),"constructorId": str(item.get("teamId")), "Q1_Millsec" : ConvertToMilliSeconds(item.get("q1")), "Q2_Millsec" :  ConvertToMilliSeconds(item.get("q2")), "Q3_Millsec" : -9999, "grid": item.get("position"), "circuitId": str(item.get("circuitId")),"year": str(finalDate), "ReachedQ3" : "0", "ReachedQ2": "1", "SetQ1Time": "1", "raceId": str(RaceId), "qualifyId" : str(QualifyingId),"lat": str(lat), "lng" :str(lng),"Race_round": str(RaceRound)}
      items = items | WeatherData
      MyList.append(items)


      #MyList.append(items)
    elif item.get("q1") is not None:
      q1 = ConvertToMilliSeconds(str(item.get("q1")))
      #Q2 needs to be inputted as -9999

      items = {"driverId" : str(item.get("driverId")),"constructorId": str(item.get("teamId")), "Q1_Millsec" : ConvertToMilliSeconds(item.get("q1")), "Q2_Millsec" : -9999, "Q3_Millsec" : -9999, "grid": item.get("position"),"circuitId": str(item.get("circuitId")),"year": str(finalDate), "ReachedQ3" : "0", "ReachedQ2": "0", "SetQ1Time": "1", "raceId": str(RaceId), "qualifyId" : str(QualifyingId),"lat": str(lat), "lng" :str(lng),"Race_round": str(RaceRound)}
      #MyList.append(items)
      items = items | WeatherData
      MyList.append(items)
  print(MyList)

  #We need to fix a bunch of columns
  MyList = pl.DataFrame(MyList)
  
  #to_physical opperates my converted the UUID's into a scale from zero, adding 1000 means it does not get misinterpreted as another drivers id
  MyList = MyList.with_columns(pl.col('driverId').cast(pl.Categorical).to_physical() + 1000)
  MyList = MyList.with_columns(pl.col('constructorId').cast(pl.Categorical).to_physical() + 1000)
  MyList = MyList.with_columns(pl.col('circuitId').cast(pl.Categorical).to_physical() + 1000)
  
  MyList = MyList.cast({"raceId": pl.Int64, "driverId" : pl.Int64, "qualifyId" : pl.Int64, "constructorId" : pl.Int64, "grid": pl.Int64, "year": pl.Int64, "Race_round": pl.Int64, "circuitId" : pl.Int64, "lat": pl.Float64, "lng": pl.Float64, "tempmax": pl.Float64,"tempmin": pl.Float64, "temp": pl.Float64, "dew": pl.Float64, "humidity": pl.Float64, "precip": pl.Float64, "snow": pl.Float64, "snowdepth": pl.Float64, "windspeed": pl.Float64, "winddir": pl.Float64, "cloudcover": pl.Float64, "ReachedQ2": pl.Int32, "ReachedQ3": pl.Int32,"SetQ1Time": pl.Int32, "Q2_Millsec": pl.Int64,"Q3_Millsec": pl.Int64,"Q1_Millsec": pl.Int64})
  #Splitting values between expected outcome as well as the data which is used to predict the race.

  
  #So we can query the dataset and get the appropriate longditude and lat stuff for our data


  #Exclude DNF's for now

  #This needs to be changed so any values after 2026 are classed differently
  #GetData = GetData.filter(pl.col('final_race_pos') != 0)
  #GetData = GetData.with_columns(pl.when(pl.col("final_race_pos") <= 3).then(0).when((pl.col("final_race_pos") > 3) & (pl.col("final_race_pos") <= 10) ).then(1).when((pl.col("final_race_pos") > 10) & (pl.col("final_race_pos") <= 15)).then(2).when((pl.col("final_race_pos") > 15) & (pl.col("final_race_pos") <= 24 )).then(3).alias('race_f'))


  #Need to get the time as well as correct circuit from the data


  #GetData = GetData.filter(pl.col('final_race_pos') <= 20)
  print(len(GetData))
  dataLen = len(GetData)

  #Train = int(int(dataLen) * 0.7)
  #Test = dataLen - Train
  #print("Train",Train)
  #print("Test",Test)
  #y = GetData.select(['race_f']).to_numpy()
  #Might not need this as this is because we dont know these values.
  x = MyList.select(pl.all().exclude(['final_race_pos','Finished_Race','resultId','points','raceId','driverId','qualifyId', 'date', 'race_f', 'Result', 'Finished Race','race_time_hr'])).to_numpy()

  #For now lets replicate example with four classes instead of 20

  x = torch.from_numpy(x)
  print(len(MyList))
  #------ NEED TO ADD 3 EXTRA DIMENSIONS TO THE TENSOR AND PUSH THESE  -------

  #Embedding our RaceID
  embedding = nn.Embedding(num_embeddings= 1000 + len(MyList), embedding_dim=1)
  #input shape from numpy is [5810,1] so with embedding_dim=1 makes it [5810,1,1]
  embed = embedding(torch.from_numpy(MyList.select(['raceId']).to_numpy())).squeeze(1)

  #Adds the shape of the tensors together dim=1 is to specify to add as columns not rows
  x = torch.cat((x, embed), dim=1)
  #Embedding our DriverID
  embedding = nn.Embedding(num_embeddings=1000 + len(MyList), embedding_dim=1)
  embed = embedding(torch.from_numpy(MyList.select(['driverId']).to_numpy())).squeeze(1)

  #Adds the shape of the tensors together dim=1 is to specify to add as columns not rows
  x = torch.cat((x, embed), dim=1)

  #Now we need these in seperate tensors

  #We need to make this dynamic
  model = F1_Race_Prediction()
  scaler = joblib.load("scaler.pkl")
  model.load_state_dict(torch.load("model.pth"))

  
  #We can get rid of this because no training and testing split
  #row_split_check_x = torch.split(x,[Train,Test],dim=0)
  #test_x, validate_x = row_split_check_x

  #row_split_check_y = torch.split(y,[Train,Test],dim=0)
  #test_y, validate_y = row_split_check_y

  #test_y, validate_y = row_split_check_y

  #test_x = test_x.to(torch.float32)
  #validate_x = validate_x.to(torch.float32)
  #For some reason these are 2D but want it to be 1D
  #test_y = test_y.to(torch.long).squeeze(1)
  #validate_y = validate_y.to(torch.long).squeeze(1)

  x = x.detach().numpy()

  x = scaler.transform(x)
  x = torch.from_numpy(x)
  x = x.to(torch.float32)
  #validate_x = validate_x.detach().numpy()
  #temp2 = scaler.fit(validate_x)
  #validate_x = temp2.transform(validate_x)
  #validate_x = torch.from_numpy(validate_x)

  #validate_x = validate_x.detach()
  #device = torch.accelerator.current_accelerator().type
  #converting our data to tensors from numpy once we have split the data
"""
  with torch.no_grad():
    prediction = model(x)

  

  print(prediction.shape)
  """
  #Adding our differnet layers however may change this because we dont really need to do it like that - also sending this to the GPU
  #torch.save(model.state_dict(), "model.pth")
  #joblib.dump(scaler, "scaler.pkl")


app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://localhost:8001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )


#Web sever code to get ML model data
@app.post("/MLModelPerformance")
async def root(QualiData: List[QualifyingData]):

  #We need to get the qualifying results for the AustralianGP 
  #we need to recive input here

  print("Hello World!!!")
  DataPrepANDRunModel(QualiData)
  #we return ML results
  return "Hello World!! + We have queried the oher model/webserver correctly!!!"

#Data needs to have some pre-processing done to it


# we need a training loop and a validation loop for our models