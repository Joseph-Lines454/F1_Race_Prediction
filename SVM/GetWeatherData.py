#Creating the API to get the correct historical weather data for each race.
import requests
import polars as pl
import numpy as np
import datetime
import json
#This program gets the race date and location, quiries the weather API for data
#Point of this is so we only make 291 requests not millions of requests which is not sustainable
#Not sure if we can get the weather lap by lap, so for now just getting the forcast at the
#start of the race

def OpenCSV():
   #Open the csv of our data and returning it
   WriteToDataSet = pl.read_csv("F1_Data/TestFormat.csv", separator=",", encoding="latin1",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)
   return WriteToDataSet

def GetCircuitsAndDates():
  #Get all of the races, we only need to loop through 291 values no more
  WriteToDataSet = OpenCSV()
  NewData = WriteToDataSet['raceId','date','lat','lng','race_time'].unique()
  return NewData


def WriteWeatherDatatoCSV(WeatherData):
  print("This is the weather data CSV")

  #Add headers here
  DataFrame = pl.DataFrame(WeatherData, schema= {"raceId": pl.Int64, "tempmax": pl.Float64,"tempmin": pl.Float64,"temp": pl.Float64,"dew": pl.Float64,"humidity": pl.Float64,"precip" :pl.Float64
  ,"snow" :pl.Float64,"snowdepth" :pl.Float64, "windspeed": pl.Float64, "winddir" : pl.Float64, "winddir": pl.Float64, "pressure": pl.Float64, "cloudcover": pl.Float64, "visibility": pl.Float64})
  DataFrame.columns = [
    "raceId",
    "tempmax",
    "tempmin",
    "temp",
    "dew",
    "humidity",
    "precip",
    "snow",
    "snowdepth",
    "windspeed",
    "winddir",
    "pressure",
    "cloudcover",
    "visibility"
  ]
  #Fill new values for binary categorical value


  DataFrame.write_csv("F1_Data/WeatherData.csv", separator=",")

def JoinData():
  WriteToDataSet = pl.read_csv("F1_Data/TestFormat.csv", separator=",", encoding="latin1",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)
  WeatherData = pl.read_csv("F1_Data/WeatherData.csv", separator=",", null_values="\\N", ignore_errors=True)
  WriteToDataSet = WriteToDataSet.join(WeatherData, on =["raceId"], suffix ="_k")
  WriteToDataSet.write_csv("F1_Data/TestFormat.csv", separator=",")

def GetWeatherForcast(FindWeather):
   
    #WriteToDataSet = OpenCSV()
    WeatherDataArray = []
    for row in FindWeather.rows(named=True):
       #we need to convert the date format from dd/mm/yyyy to yyyy-mm-dd because thats the only format that the API suppports
      
      newdate = datetime.datetime.strptime(row['date'],"%d/%m/%Y").strftime("%Y-%m-%d")
      
      WeatherData = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline" + "/" + str(row['lat']) + "," + str(row['lng']) + "/" + str(newdate) + "T" + str(row['race_time']) + "?key=HAWRLDPJJULW8C79XWHQGZP2F&include=current")
      #print(WeatherData)
        #We can make it so that the query is added to the correct data based on 
        #WeatherData = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/-37.8497,144.968/2012-03-18T6:00:00?key=HAWRLDPJJULW8C79XWHQGZP2F&include=current")
        #print(WeatherData)
      WeatherData = json.loads(WeatherData.text)
        #Do we join data here?
        #np.append(WeatherData, FindWeather[0])
        
      

        #Pull the values we need from the JSON data - DONT Join JSON data make a new array ready to join
      WeatherDataArray.append([row['raceId'],WeatherData['days'][0]['tempmax'], WeatherData['days'][0]['tempmin'], WeatherData['days'][0]['temp'],WeatherData['days'][0]['dew'],WeatherData['days'][0]['humidity'], WeatherData['days'][0]['precip'], WeatherData['days'][0]['snow'],WeatherData['days'][0]['snowdepth'],WeatherData['days'][0]['windspeed'],WeatherData['days'][0]['winddir'], WeatherData['days'][0]['pressure'],WeatherData['days'][0]['cloudcover'],WeatherData['days'][0]['visibility']])
      
      
      #WeatherDataArray = FillInMissingValues(WeatherDataArray)
      #WeatherDataArray = WeatherDataArray.astype(str)
     
    #Add this data to a csv file so we can join it
    WriteWeatherDatatoCSV(WeatherDataArray)

#Function that gets the data

GetWeatherForcast(GetCircuitsAndDates())

JoinData()

#WeatherData = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline" + "/" + str("-37.8497") + "," + str("144.968") + "/" + str("2026-03-08") + "T" + str("05:00:00") + "?key=HAWRLDPJJULW8C79XWHQGZP2F&include=current")
#WeatherData = json.loads(WeatherData.text)
#print(WeatherData.text)
