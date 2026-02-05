import polars as pl
import numpy as np
from sklearn.model_selection import train_test_split


#We still need to do some pre-proccessing to the data - For qualifying data we need to use an arbitary value with out binary indicator flag (Reached Q2 ect)
#Values also need to be encoded because some are in string formats which ML models do not like




#If we get low scores, we can look at potentially adding more features ect.



GetData = pl.read_csv("F1_Data/Prerace_Prediction.csv", separator=",", encoding="latin1",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)

#Splitting values between expected outcome.
y = GetData.select(['final_race_pos','Finished_Race']).to_numpy()
x = GetData.select(pl.all().exclude(['final_race_pos','Finished_Race']))

#Have split data for training and testing
x_train,x_test, y_train, y_test  = train_test_split(x,y, test_size=0.7, random_state=4)

print(y_train)
print("///////////")
print(y_test)