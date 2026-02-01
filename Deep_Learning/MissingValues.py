import polars as pl


#We have missing values for races finish position as well as qualifying. we want to use Binary categorical variable

def BinaryCategoricalValues():
  Get_CSV_Data = pl.read_csv("F1_Data/TestFormat.csv", separator=",", encoding="latin1",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)

  Get_CSV_Data = Get_CSV_Data.with_columns(pl.when(pl.col("q2").is_null()).then(0).otherwise(1).alias("ReachedQ2"))
  Get_CSV_Data = Get_CSV_Data.with_columns(pl.when(pl.col("q3").is_null()).then(0).otherwise(1).alias("ReachedQ3"))
  Get_CSV_Data = Get_CSV_Data.with_columns(pl.when(pl.col("final_race_pos").is_null()).then(0).otherwise(1).alias("Finished Race"))
  print(Get_CSV_Data.head())
  Get_CSV_Data.write_csv("F1_Data/TestFormat.csv", separator=",")

BinaryCategoricalValues()