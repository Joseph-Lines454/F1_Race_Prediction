import polars as pl
import numpy as numpy
#We have missing values for races finish position as well as qualifying. we want to use Binary categorical variable

def ConvertToMilliseconds(array):
  print("We are converting to milliseconds")
  newvalues = []
  for value in array:
    if value != "-9999":
      values = value.split(":")
      values = (float(values[0]) * 60000) + (float(values[1]) * 1000)
      newvalues.append(values)
    else:
      newvalues.append(-9999.0)

  
  return newvalues


def ConvertToHour(array):
  print("We are converting to Hour")
  newvalues = []
  for value in array:
    if value != "-9999":
      values = value.split(":")
      values = int(values[0])
      newvalues.append(values)
    

  
  return newvalues




  #convert data to milliseconds

def Pre_Processing():
  Get_CSV_Data = pl.read_csv("F1_Data/Prerace_Prediction.csv", separator=",", encoding="latin1",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)

  """
  #We need to convert our data into a float format and feed it into a tensor - so our time data needs to be converted

  Get_CSV_Data = Get_CSV_Data.with_columns(pl.col("q2").alias("q2_milll"))
  
  array = Get_CSV_Data["q2_milll"].to_numpy()
  #ConvertToMilliseconds(array)

  
  Q2Data = ConvertToMilliseconds(array)
  #Add a new column here for milliseconds
  Get_CSV_Data = Get_CSV_Data.with_columns(pl.Series("Q2_Millsec",Q2Data))

  Get_CSV_Data = Get_CSV_Data.with_columns(pl.col("q1").alias("q1_milll"))
  
  array = Get_CSV_Data["q1_milll"].to_numpy()
  Q1Data = ConvertToMilliseconds(array)
  #Add a new column here for milliseconds
  Get_CSV_Data = Get_CSV_Data.with_columns(pl.Series("Q1_Millsec",Q1Data))

  Get_CSV_Data = Get_CSV_Data.with_columns(pl.col("q3").alias("q3_milll"))
  
  array = Get_CSV_Data["q3_milll"].to_numpy()
  Q3Data = ConvertToMilliseconds(array)
  #Add a new column here for milliseconds
  Get_CSV_Data = Get_CSV_Data.with_columns(pl.Series("Q3_Millsec",Q3Data))
  Get_CSV_Data = Get_CSV_Data.drop("q2_milll")
  Get_CSV_Data = Get_CSV_Data.drop("q1_milll")
  Get_CSV_Data = Get_CSV_Data.drop("q3_milll")
  Get_CSV_Data = Get_CSV_Data.drop("q2")
  Get_CSV_Data = Get_CSV_Data.drop("q1")
  Get_CSV_Data = Get_CSV_Data.drop("q3")

  """
  
  #We also need to convert the race time to just the hour

  Get_CSV_Data = Get_CSV_Data.with_columns(pl.col("race_time").alias("race_time_h"))
  
  array = Get_CSV_Data["race_time_h"].to_numpy()
  #ConvertToMilliseconds(array)

  
  RaceData = ConvertToHour(array)
  #Add a new column here for milliseconds
  Get_CSV_Data = Get_CSV_Data.with_columns(pl.Series("race_time_hr",RaceData))

  Get_CSV_Data = Get_CSV_Data.drop("race_time_h")
  Get_CSV_Data = Get_CSV_Data.drop("race_time")
  Get_CSV_Data.write_csv("F1_Data/Prerace_Prediction.csv", separator=",")

Pre_Processing()