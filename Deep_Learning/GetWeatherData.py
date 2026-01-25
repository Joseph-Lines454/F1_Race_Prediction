#Creating the API to get the correct historical weather data for each race.
import requests
import polars as pl
import numpy as np


def GetCircuitsAndDates():
  arrayWeather = np.empty((0,4))
  
  WriteToDataSet = pl.read_csv("F1_Data/FinalDataFormat.csv", separator=",", encoding="latin1",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)
  i = 0
  for row in WriteToDataSet.rows(named=True):
    #arraytemp = [row['raceId'], row['date'],row['lat'],row['lng']]
    if np.any(np.all(arrayWeather ==  [row['raceId'], row['date'],row['lat'],row['lng']],axis=1)) == False:
      arrayWeather = np.append(arrayWeather, [[row['raceId'], row['date'],row['lat'],row['lng']]], axis = 0)
      
  print(len(arrayWeather))

  #for row in arrayWeather:
  #  print(row)

#x = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/#timeline/-37.8497,144.968/2012-03-18T06:00:00?key=HAWRLDPJJULW8C79XWHQGZP2F")




GetCircuitsAndDates()


#print(x.text)