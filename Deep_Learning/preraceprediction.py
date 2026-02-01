import polars as pl
#Our data is lap by lap, we want to have a version which isnt, for pre race predictions we want to remove this
#this code will get the unique rows raceID and driverID and put it in a new excel sheet.

def GetUniqueValues():
  #Get all of the races, we only need to loop through 291 values no more
  WriteToDataSet = pl.read_csv("F1_Data/TestFormat.csv", separator=",", encoding="latin1",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)
  NewData = WriteToDataSet['raceId','driverId', 'race_position', 'constructorId', 'q1', 'q2', 'q3','grid','year','Race_round','circuitId', 'date','race_time', 'lat', 'lng',  'tempmax', 'tempmin', 'temp', 'dew', 'humidity', 'precip','snow','snowdepth','windspeed','winddir','pressure','cloudcover','visibility','ReachedQ2','ReachedQ3'].unique()
  NewData.write_csv("F1_Data/Prerace_Prediction.csv", separator=",")


GetUniqueValues()