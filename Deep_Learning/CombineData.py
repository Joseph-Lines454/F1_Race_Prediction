#Using Polars to load data into python, we are adding data onto each of the lap times
import polars as pl

#reading data and ensuring that its csv
df = pl.read_csv("F1_Data/lap_times.csv", separator=",")
otherDataSet = pl.read_csv("F1_Data/races.csv", separator=",")

print(df.head())
#iterate through rows



#df.with_columns(
#  when = df["raceId"] == otherDataSet.col.raceId & df.col.driverId == otherDataSet.col.driverId,
#  then = otherDataSet.col.driverId
#  
#).with_columns (
#  pl.when("when").then("then").alias("DriverId")
#)

#need to delete colummns which are before 841





#for row in df.iter_rows(named=True):
#  print(str(row['raceId']))
#  if (row['raceId'] == otherDataSet['raceID']) & (row['driverId'] == otherDataSet['driverID']):

#This has been used to add new data to the lap times dataset, now we know what circuit is associated with that lap time
#combinedNew = df.join(otherDataSet, on=["raceId"])

#Now new want to add the drivers name 
WriteToDataSet = pl.read_csv("F1_Data/FinalDataFormat.csv", separator=",", encoding="latin1",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)



#We want to add the qualifying position to this dataset to show where the driver started from
qualifyingDataSet = pl.read_csv("F1_Data/qualifying.csv", separator=",", null_values="\\N")
WriteToDataSet = WriteToDataSet.join(qualifyingDataSet, on=["raceId", "driverId"], suffix="_i")


resultsDataSet = pl.read_csv("F1_Data/results.csv", separator=",", null_values="\\N", ignore_errors=True)
WriteToDataSet = WriteToDataSet.join(resultsDataSet, on=["raceId", "driverId"], suffix="_r")

pitstopsDataSet = pl.read_csv("F1_Data/pit_stops.csv", separator=",", null_values="\\N", ignore_errors=True)
WriteToDataSet = WriteToDataSet.join(pitstopsDataSet, on=["raceId", "driverId", "lap"], suffix="_k", how = "full")

#We need to join the curcuit dataset so we can then add the long and lat locations to get the appropriate weather data

raceData = pl.read_csv("F1_Data/races.csv", separator=",", null_values="\\N", ignore_errors=True)
WriteToDataSet = WriteToDataSet.join(raceData, on =["raceId"], suffix ="_j")

#Now we want to join the circuit infromation regarding lat and longditude
circuitData = pl.read_csv("F1_Data/circuits.csv", separator=",", null_values="\\N", ignore_errors=True)
WriteToDataSet = WriteToDataSet.join(circuitData, on =["circuitId"], suffix ="_k")


WriteToDataSet.write_csv("F1_Data/FinalDataFormat.csv", separator=",")





print(df)
