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
   WriteToDataSet = pl.read_csv("F1_Data/FinalDataFormat.csv", separator=",", encoding="latin1",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)
   return WriteToDataSet

def GetCircuitsAndDates():
  #Creating the shape of our array
  arrayWeather = np.empty((0,5))
  #Get CV data
  WriteToDataSet = OpenCSV()
  #Look through the rows in out csv
  for row in WriteToDataSet.rows(named=True):
    #If the current row is not already in our array we add it
    if np.any(np.all(arrayWeather ==  [row['raceId'], row['date'],row['lat'],row['lng'],row['race_time']],axis=1)) == False:
      #Adding data to array
      arrayWeather = np.append(arrayWeather, [[row['raceId'], row['date'],row['lat'],row['lng'],row['race_time']]], axis = 0)
    
  #print(len(arrayWeather))
  #for i in arrayWeather:
  #   print(i)
  return arrayWeather

def WriteWeatherDatatoCSV(WeatherData):
  print("This is the weather data CSV")
  #open csv file then write the data to it
  #OpenWeatherCSV = pl.read_csv("F1_Data/WeatherData.csv", separator=",", encoding="latin1", ignore_errors=True)



  #Add headers here
  

  DataFrame = pl.DataFrame(WeatherData, schema=None,infer_schema_length = 0)
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
  DataFrame.write_csv("F1_Data/WeatherData.csv", separator=",")

def FillInMissingValues(WeatherData):
  for row in WeatherData:
    for value in row:
      if value == None or isinstance(value,str) == False:
        value = " "
      
  return WeatherData

def JoinData():
  WriteToDataSet = pl.read_csv("F1_Data/FinalDataFormat.csv", separator=",", encoding="latin1",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)
  WeatherData = pl.read_csv("F1_Data/WeatherData.csv", separator=",", null_values="\\N", ignore_errors=True)
  WriteToDataSet = WriteToDataSet.join(WeatherData, on =["raceId"], suffix ="_k")
  WriteToDataSet.write_csv("F1_Data/FinalDataFormat.csv", separator=",")

def GetWeatherForcast(FindWeather):
    i = 0
    #WriteToDataSet = OpenCSV()
    WeatherDataArray = np.empty((0,14),dtype=object)
    for row in FindWeather:
       #we need to convert the date format from dd/mm/yyyy to yyyy-mm-dd because thats the only format that the API suppports
      newdate = datetime.datetime.strptime(str(row[1]),"%d/%m/%Y").strftime("%Y-%m-%d")
      
      WeatherData = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline" + "/" + str(row[2]) + "," + str(row[3]) + "/" + str(newdate) + "T" + str(row[4]) + "?key=HAWRLDPJJULW8C79XWHQGZP2F&include=current")
      #print(WeatherData)
        #We can make it so that the query is added to the correct data based on 
        #WeatherData = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/-37.8497,144.968/2012-03-18T6:00:00?key=HAWRLDPJJULW8C79XWHQGZP2F&include=current")
        #print(WeatherData)
      WeatherData = json.loads(WeatherData.text)
        #Do we join data here?
        #np.append(WeatherData, FindWeather[0])
        
      

        #Pull the values we need from the JSON data - DONT Join JSON data make a new array ready to join
      WeatherDataArray = np.vstack([WeatherDataArray,[row[0],WeatherData['days'][0]['tempmax'], WeatherData['days'][0]['tempmin'], WeatherData['days'][0]['temp'],WeatherData['days'][0]['dew'],WeatherData['days'][0]['humidity'], WeatherData['days'][0]['precip'], WeatherData['days'][0]['snow'],WeatherData['days'][0]['snowdepth'],WeatherData['days'][0]['windspeed'],WeatherData['days'][0]['winddir'], WeatherData['days'][0]['pressure'],WeatherData['days'][0]['cloudcover'],WeatherData['days'][0]['visibility']]])
      FillInMissingValues(WeatherDataArray)
      
      WeatherDataArray = FillInMissingValues(WeatherDataArray)
      WeatherDataArray = WeatherDataArray.astype(str)
      i = i + 1
      #if i == 80:
      #  break
    #Add this data to a csv file so we can join it
    WriteWeatherDatatoCSV(WeatherDataArray)

#Function that gets the data
GetWeatherForcast(GetCircuitsAndDates())
JoinData()


