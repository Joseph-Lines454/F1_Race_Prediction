import polars as pl

#We have missing values for races finish position as well as qualifying. we want to use Binary categorical variable

def BinaryCategoricalValues():
  Get_CSV_Data = pl.read_csv("F1_Data/Prerace_Prediction.csv", separator=",", encoding="latin1",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)

  Get_CSV_Data = Get_CSV_Data.with_columns(pl.when(pl.col("q2").is_null()).then(0).otherwise(1).alias("ReachedQ2"))
  Get_CSV_Data = Get_CSV_Data.with_columns(pl.when(pl.col("q3").is_null()).then(0).otherwise(1).alias("ReachedQ3"))
  Get_CSV_Data = Get_CSV_Data.with_columns(pl.when(pl.col("q1").is_null()).then(0).otherwise(1).alias("SetQ1Time"))
  Get_CSV_Data = Get_CSV_Data.with_columns(pl.when(pl.col("final_race_pos").is_null()).then(0).otherwise(1).alias("Finished_Race"))
  Get_CSV_Data = Get_CSV_Data.with_columns(pl.when(pl.col("grid").is_null()).then(0).otherwise(1).alias("OnGrid"))
  #Get_CSV_Data = Get_CSV_Data.with_columns(pl.when(pl.col("final_race_pos").is_null()).then(0).otherwise(1).alias("Finished Race"))

  #Here we want to fill columns with null with  -99999 -Because the value is suppost to be null
  Get_CSV_Data = Get_CSV_Data.with_columns(pl.col("q1").fill_null(-9999))
  Get_CSV_Data = Get_CSV_Data.with_columns(pl.col("q2").fill_null(-9999))
  Get_CSV_Data = Get_CSV_Data.with_columns(pl.col("q3").fill_null(-9999))
  Get_CSV_Data = Get_CSV_Data.with_columns(pl.col("final_race_pos").fill_null(0))
  Get_CSV_Data = Get_CSV_Data.with_columns(pl.col("grid").fill_null(0))
  
  Get_CSV_Data.write_csv("F1_Data/Prerace_Prediction.csv", separator=",")

BinaryCategoricalValues()