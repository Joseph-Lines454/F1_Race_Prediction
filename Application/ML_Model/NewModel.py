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
    self.Input1 = nn.Linear(26, 120)
    self.relu1 = nn.Tanh()
    self.Drop1 = nn.Dropout(0.5)
    self.Input2 = nn.Linear(120, 120)
    self.relu2 = nn.Tanh()
    self.Drop2 = nn.Dropout(0.5)
    # its because we are returning an output
    self.Input4 = nn.Linear(120,4)
    
   

  def forward(self,x):
    out = self.Input1(x)
    out = self.relu1(out)
    out = self.Drop1(out)
    out = self.Input2(out)
    out = self.relu2(out)
    out = self.Drop2(out)
    out = self.Input4(out)
   
    #out = self.activitation(out)
    #return torch.argmax(out, dim=1)
    return out

def ConvertToMilliSeconds(time):

  
  minutes, seconds = time.split(":")
  total_time_in_ms = ((float(minutes) * 60) + float(seconds)) * 1000
  return int(total_time_in_ms)

def WeatherDataRes(lat,lng,date):
  WeatherData = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline" + "/" + str(lat) + "," + str(lng) + "/" + date + "?key=HAWRLDPJJULW8C79XWHQGZP2F&include=current")

  
  WeatherData = json.loads(WeatherData.text)
  #We now need to get weather data
  return WeatherData

def CompareCircuits(CircuitID):

  Circuits = pl.read_csv("F1_Data/Circuit_Conversion.csv", separator=",", encoding="latin1",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)
  Data = Circuits.filter(pl.col('UUID') == str(CircuitID))
  return Data

def ConstructorID(ConstructorID):
  Constructor = pl.read_csv("F1_Data/Team_Conversion.csv", separator=",", encoding="utf-8-sig",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)
  Data = Constructor.filter(pl.col('UUID') == str(ConstructorID))
  return Data["Number_trainning_Team"].item()

def DriverIDFunc(DriverID):
  Driver = pl.read_csv("F1_Data/Driver_Conversion.csv", separator=",", encoding="utf-8-sig",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)
  Data = Driver.filter(pl.col('UUID') == str(DriverID))
  return Data["Number_trainning"].item()

def DataPrepANDRunModel(QualiData):
  #we are getting the circuit that has been raced on
  

  GetData = pl.read_csv("F1_Data/Prerace_Prediction.csv", separator=",", encoding="latin1",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)

  
  #GetData = GetData.with_columns(pl.when(pl.col("Q1_Millsec") == -9999).then(0).otherwise(pl.col("SetQ1Time")).alias("SetQ1Time"))
  #GetData = GetData.with_columns(pl.when(pl.col("Q2_Millsec") == -9999).then(0).otherwise(pl.col("ReachedQ2")).alias("ReachedQ2"))
  #GetData = GetData.with_columns(pl.when(pl.col("Q3_Millsec") == -9999).then(0).otherwise(pl.col("ReachedQ3")).alias("ReachedQ3"))


  #GetData.write_csv("F1_Data/Prerace_Prediction.csv", separator=",")
  
  Data = CompareCircuits(QualiData[0].circuitId)

  #ConstructorID(QualiData[0].teamId)

  #Data = GetData.filter(pl.col('circuitId').cast(pl.Utf8) == QualiData[0].circuitId)
  #print(Data)
  lng = float(Data['lng'][0])
  lat = float(Data['lat'][0])
  CircuitID = str(Data["Cicruit_Number_trainning"][0])
  WeatherData = WeatherDataRes(Data['lat'][0],Data['lng'][0],QualiData[0].date)
  #now manipulation needs to be done on oter data
  



  WeatherData = {"tempmax": WeatherData['days'][0]['tempmax'], "tempmin": WeatherData['days'][0]['tempmin'], "temp":WeatherData['days'][0]['temp'], "dew" : WeatherData['days'][0]['dew'], "humidity": WeatherData['days'][0]['humidity'], "precip": WeatherData['days'][0]['precip'], "snow": WeatherData['days'][0]['snow'], "snowdepth": WeatherData['days'][0]['snowdepth'], "windspeed":WeatherData['days'][0]['windspeed'], "winddir": WeatherData['days'][0]['winddir'], "cloudcover": WeatherData['days'][0]['cloudcover']}


  #Then we need to get the data - we need to get year out of that fuuck...


  #Get Qualifying ID
  QualifyingId = int(GetData["qualifyId"].max())

  RaceId = int(GetData["raceId"].max() + 1)
  print(RaceId)
  RaceRound = int(GetData["Race_round"][-1] + 1)

  MyList = []

  for item in QualiData:

    #We need to convert each DriverID in this bit!
    
    ConstructorIDIn = str(ConstructorID(item.teamId))
    DriverIDIn =  str(DriverIDFunc(item.driverId))
    #convert each qualitime into a milliseconds then get assign a onehot encoding value for each column
    QualifyingId = QualifyingId + 1
    #format date
    #split the string into date and year, then with the date part [0] split it in year,month and date then reassemble using the other date format
    year, month, day = item.date.split("T")[0].split("-")
    finalDate = f"{year}"
    # Have to get race time hr - Missing vairable
    item = item.dict()

    if item.get("q1") is not None:
      q1 = ConvertToMilliSeconds(str(item.get("q1")))
      #Q2 needs to be inputted as -9999

      items = {"driverId" : str(DriverIDIn),"constructorId": str(ConstructorIDIn), "Q1_Millsec" : ConvertToMilliSeconds(item.get("q1")), "Q2_Millsec" : -9999, "Q3_Millsec" : -9999, "grid": item.get("gridposition"),"circuitId": CircuitID,"year": str(finalDate), "ReachedQ3" : "0", "ReachedQ2": "0", "SetQ1Time": "1", "raceId": str(RaceId), "qualifyId" : str(QualifyingId),"lat": str(lat), "lng" :str(lng),"Race_round": str(RaceRound)}
      #MyList.append(items)
      items = items | WeatherData

    if item.get("q2") is not None:
      
      items = {"driverId" : str(DriverIDIn),"constructorId": str(ConstructorIDIn), "Q1_Millsec" : ConvertToMilliSeconds(item.get("q1")), "Q2_Millsec" :  ConvertToMilliSeconds(item.get("q2")), "Q3_Millsec" : -9999, "grid": item.get("gridposition"), "circuitId": CircuitID,"year": str(finalDate), "ReachedQ3" : "0", "ReachedQ2": "1", "SetQ1Time": "1", "raceId": str(RaceId), "qualifyId" : str(QualifyingId),"lat": str(lat), "lng" :str(lng),"Race_round": str(RaceRound)}
      items = items | WeatherData

    if item.get("q3") is not None:
      items = {"driverId" : str(DriverIDIn),"constructorId": str(ConstructorIDIn), "Q1_Millsec" : ConvertToMilliSeconds(item.get("q1")), "Q2_Millsec" : ConvertToMilliSeconds(item.get("q2")), "Q3_Millsec": ConvertToMilliSeconds(item.get("q3")), "grid": item.get("gridposition"), "circuitId": CircuitID,"year": str(finalDate),"ReachedQ3" : "1", "ReachedQ2": "1", "SetQ1Time": "1", "raceId": str(RaceId), "qualifyId" : str(QualifyingId), "lat": str(lat), "lng" :str(lng), "Race_round": str(RaceRound) }
      items = items | WeatherData
    #print(items)
    items = items | {'final_race_pos': 0,'Finished_Race': 1,'resultId': 1,'points': 1,'qualifyId': 1, 'date': '2026',  'Result': 1, 'Finished Race': 1,'race_time_hr': 1}
    MyList.append(items)
    #print(items)
    #print(items)
    
      #MyList.append(items)
    
    #print(items)

    
  
  #We need to fix a bunch of columns

  orderForVairables = ["raceId","driverId","qualifyId","constructorId","Result","resultId","grid","final_race_pos","points","year","Race_round","circuitId","date","lat","lng","tempmax","tempmin","temp","dew","humidity",	"precip","snow","snowdepth","windspeed","winddir","cloudcover","ReachedQ2","ReachedQ3","Finished Race","SetQ1Time","Finished_Race","Q2_Millsec","Q3_Millsec","Q1_Millsec","race_time_hr"
]
  MyList = pl.DataFrame(MyList)
  
  #to_physical opperates my converted the UUID's into a scale from zero, adding 1000 means it does not get misinterpreted as another drivers id
  #MyList = MyList.with_columns(pl.col('driverId').cast(pl.Categorical).to_physical())
  #MyList = MyList.with_columns(pl.col('constructorId').cast(pl.Categorical).to_physical())
  #MyList = MyList.with_columns(pl.col('circuitId').cast(pl.Categorical).to_physical())
  
  MyList = MyList.cast({"raceId": pl.Int64, "driverId" : pl.Int64, "qualifyId" : pl.Int64, "constructorId" : pl.Int64, 'Result': pl.Int64,'resultId':pl.Int64, "grid": pl.Int64,'final_race_pos': pl.Int64, 'points': pl.Int64,"year": pl.Int64, "Race_round": pl.Int64, "circuitId" : pl.Int64,'date': pl.Int64, "lat": pl.Float64, "lng": pl.Float64, "tempmax": pl.Float64,"tempmin": pl.Float64, "temp": pl.Float64, "dew": pl.Float64, "humidity": pl.Float64, "precip": pl.Float64, "snow": pl.Float64, "snowdepth": pl.Float64, "windspeed": pl.Float64, "winddir": pl.Float64, "cloudcover": pl.Float64, "ReachedQ2": pl.Int32, "ReachedQ3": pl.Int32,'Finished Race':pl.Int64,"SetQ1Time": pl.Int32, 'Finished Race': pl.Int64, "Q2_Millsec": pl.Int64,"Q3_Millsec": pl.Int64,"Q1_Millsec": pl.Int64,'race_time_hr': pl.Int64})
  #Splitting values between expected outcome as well as the data which is used to predict the race.

  #This should be ready for ML model now 
  MyList = MyList.select(orderForVairables)

  for row in MyList.iter_rows(named=True):
    print(row)

  #Write the values of the australianGP to the csv file, nice!
  #GetData = pl.concat([GetData.cast(pl.Utf8),MyList.cast(pl.Utf8)])
  #GetData.write_csv("F1_Data/Prerace_Prediction.csv", separator=",")
  
  #So we can query the dataset and get the appropriate longditude and lat stuff for our data


  #Exclude DNF's for now

  #This needs to be changed so any values after 2026 are classed differently
  #GetData = GetData.filter(pl.col('final_race_pos') != 0)
  #GetData = GetData.with_columns(pl.when(pl.col("final_race_pos") <= 3).then(0).when((pl.col("final_race_pos") > 3) & (pl.col("final_race_pos") <= 10) ).then(1).when((pl.col("final_race_pos") > 10) & (pl.col("final_race_pos") <= 15)).then(2).when((pl.col("final_race_pos") > 15) & (pl.col("final_race_pos") <= 24 )).then(3).alias('race_f'))


  #Need to get the time as well as correct circuit from the data


  #GetData = GetData.filter(pl.col('final_race_pos') <= 20)


  #Train = int(int(dataLen) * 0.7)
  #Test = dataLen - Train
  #print("Train",Train)
  #print("Test",Test)
  #y = GetData.select(['race_f']).to_numpy()
  #Might not need this as this is because we dont know these values.
  
  x = MyList.select(pl.all().exclude(['final_race_pos','Finished_Race','resultId','points','qualifyId', 'date', 'race_f', 'Result', 'Finished Race','race_time_hr'])).to_numpy()

  #For now lets replicate example with four classes instead of 20

  x = torch.from_numpy(x)
  

  

  #------ NEED TO ADD 3 EXTRA DIMENSIONS TO THE TENSOR AND PUSH THESE  -------

  DriverID = torch.from_numpy(MyList.select(['driverId']).to_numpy()).long()
  RaceID = torch.from_numpy(MyList.select(['raceId']).to_numpy()).long()
  driver_number = int(DriverID.max()) + 1
  race_id = int(RaceID.max()) + 1





  #Now we need these in seperate tensors

  #We need to make this dynamic
  model = F1_Race_Prediction()
  scaler = joblib.load("scaler.pkl")
  model.load_state_dict(torch.load("model.pth"))


  x = x.detach().numpy()

  x = scaler.transform(x)
  x = torch.from_numpy(x)
  x = x.to(torch.float32)

  #print(x)
  
  print(x.shape)
  #single_sample = x[1].unsqueeze(0)
  
  with torch.no_grad():
    prediction = model(x)
    print(prediction)
  

  #We need to loop through the prediction and assign the predictiont to the appropriate driver
  
  newData = []
  print("tensorShape:", prediction.shape)
  count = 0
  for item in QualiData:
    newData.append({"DriverName": item.driverId, "DriverPositon": torch.argmax(prediction[count]).item()})
    print(newData[count])
    count = count + 1

  #Adding our differnet layers however may change this because we dont really need to do it like that - also sending this to the GPU
  #torch.save(model.state_dict(), "model.pth")
  #joblib.dump(scaler, "scaler.pkl")
  return newData
  
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

  
  #we return ML results
  return DataPrepANDRunModel(QualiData)

#Data needs to have some pre-processing done to it


# we need a training loop and a validation loop for our modelsH