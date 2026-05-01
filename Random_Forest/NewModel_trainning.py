import polars as pl
import numpy as np
import torch
from torch import nn
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
import joblib
from sklearn.metrics import classification_report
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV
#We still need to do some pre-proccessing to the data - For qualifying data we need to use an arbitary value with out binary indicator flag (Reached Q2 ect)
#Values also need to be encoded because some are in string formats which ML models do not like
epochIn = 300
#Trainning model for our data

     




def DataPrepANDRunModel():
  GetData = pl.read_csv("F1_Data/Prerace_Prediction.csv", separator=",", encoding="latin1",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)



  GetData = GetData.cast({"raceId": pl.Int64, "driverId" : pl.Int64, "qualifyId" : pl.Int64, "constructorId" : pl.Int64, "Result": pl.Int64,"resultId": pl.Int64, "grid": pl.Int64, "final_race_pos": pl.Int64,"points": pl.Int64, "year": pl.Int64, "Race_round": pl.Int64, "circuitId" : pl.Int64, "lat": pl.Float64, "lng": pl.Float64, "tempmax": pl.Float64,"tempmin": pl.Float64, "temp": pl.Float64, "dew": pl.Float64, "humidity": pl.Float64, "precip": pl.Float64, "snow": pl.Float64, "snowdepth": pl.Float64, "windspeed": pl.Float64, "cloudcover": pl.Float64, "ReachedQ2": pl.Int32, "ReachedQ3": pl.Int32,"SetQ1Time": pl.Int32, "Finished_Race": pl.Int32, "Q2_Millsec": pl.Int64,"Q3_Millsec": pl.Int64,"Q1_Millsec": pl.Int64,"race_time_hr": pl.Int64})
  #Splitting values between expected outcome as well as the data which is used to predict the race.

  #Exclude DNF's for now

  #This needs to be changed so any values after 2026 are classed differently
  GetData = GetData.filter(pl.col('final_race_pos') != 0)
  GetData = GetData.with_columns(pl.when(pl.col("final_race_pos") <= 3).then(0).when((pl.col("final_race_pos") > 3) & (pl.col("final_race_pos") <= 10) ).then(1).when((pl.col("final_race_pos") > 10) & (pl.col("final_race_pos") <= 15)).then(2).when((pl.col("final_race_pos") > 15) & (pl.col("final_race_pos") <= 24 )).then(3).alias('race_f'))


  #GetData = GetData.filter(pl.col('final_race_pos') <= 20)
  print(len(GetData))
  dataLen = len(GetData)

  Train = int(int(dataLen) * 0.7)
  Test = dataLen - Train
  print("Train",Train)
  print("Test",Test)
  y = GetData.select(['race_f']).to_numpy()
  x = GetData.select(pl.all().exclude(['final_race_pos','Finished_Race','resultId','points','qualifyId', 'date', 'race_f', 'Result', 'Finished Race','race_time_hr'])).to_numpy()

  #For now lets replicate example with four classes instead of 20
  y = torch.from_numpy(y)
  x = torch.from_numpy(x)

  #------ NEED TO ADD 3 EXTRA DIMENSIONS TO THE TENSOR AND PUSH THESE  -------

  

  #Now we need these in seperate tensors

  #We need to make this dynamic
  scaler = StandardScaler()

  row_split_check_x = torch.split(x,[Train,Test],dim=0)
  test_x, validate_x = row_split_check_x

  row_split_check_y = torch.split(y,[Train,Test],dim=0)
  test_y, validate_y = row_split_check_y

  test_y, validate_y = row_split_check_y
  

  test_x = test_x.to(torch.float32)
  validate_x = validate_x.to(torch.float32)
  #For some reason these are 2D but want it to be 1D
  test_y = test_y.to(torch.long).squeeze(1)
  validate_y = validate_y.to(torch.long).squeeze(1)

  test_x = test_x.detach().numpy()
  temp1 = scaler.fit(test_x)
  test_x = temp1.transform(test_x)
  test_x = torch.from_numpy(test_x)

  test_x = test_x.detach()

  validate_x = validate_x.detach().numpy()
  temp2 = scaler.fit(validate_x)
  validate_x = temp2.transform(validate_x)
  validate_x = torch.from_numpy(validate_x)

  validate_x = validate_x.detach()
  #device = torch.accelerator.current_accelerator().type
  #converting our data to tensors from numpy once we have split the data

  

  #Need to define our loss functions as well as optimizers - This will change as we will need an appropriate loss function
 
  #Number of trees
  classifier = RandomForestClassifier(n_estimators=300,
                                 
                                 random_state=150,
                                 max_features=22, max_depth=10 )
  classifier.fit(test_x, test_y)
  y_pred = classifier.predict(validate_x)
  #53.68%



  print(classification_report(validate_y, y_pred))
  print(f1_score(validate_y,y_pred, average='macro'))
  #Get the accuracy of each
  titles_options = [
    ("Gradient Bossting Classifier Matrix", None),
    ("Normalized confusion matrix", "true"),
    ]
  for title, normalize in titles_options:
    disp = ConfusionMatrixDisplay.from_estimator(
      classifier,
      validate_x,
      validate_y,
      display_labels=[0,1,2,3],
      cmap=plt.cm.Blues,
      normalize="true",
      )
    disp.ax_.set_title(title)
    print(title)
    print(disp.confusion_matrix)
    plt.show()
  #Adding our differnet layers however may change this because we dont really need to do it like that - also sending this to the GPU
  #torch.save(model.state_dict(), "model.pth")
  #joblib.dump(scaler, "scaler.pkl")


DataPrepANDRunModel()

#Data needs to have some pre-processing done to it


# we need a training loop and a validation loop for our models