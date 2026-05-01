import polars as pl
import numpy as np
import torch
from torch import nn
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_class_weight
import requests
import joblib
#We still need to do some pre-proccessing to the data - For qualifying data we need to use an arbitary value with out binary indicator flag (Reached Q2 ect)
#Values also need to be encoded because some are in string formats which ML models do not like
epochIn = 325
#Trainning model for our data
y_true = []
y_pred = []
def TrainModel(epochs, optimizer, model, loss_fn, x_train, y_train, x_val,y_val):
  for epoch in range (1, epochs + 1):
    model.train()
    optimizer.zero_grad()
    x_trained = model(x_train)
    loss = loss_fn(x_trained,y_train)
    
    #Reset gradiant back to zero so gradient does not accumulate
    #Backpropagation
    loss.backward()


    #print(optimizer.grad.norm())
    optimizer.step()
   
    
    if epoch % 50 == 0 or epoch == epochIn:
      print("Epoch " + str(epoch) + " Training Loss " + str(loss.item()))



     
    #We dont want to calculate gradiant becuase we are not improving the model, we are validating our data
    with torch.no_grad():
      model.eval()
      x_validate = model(x_val)
      #Checking loss on out data
     
      loss = loss_fn(x_validate,y_val)
      #print The loss if epoch is equal to 50
      if epoch % 50 == 0 or epoch == epochIn:
        print("Epoch " + str(epoch) + " Validation Loss " + str(loss.item()))


  model.eval()
  with torch.no_grad():
    preds = model(x_val)
    y_pred = torch.argmax(preds, dim=1).cpu().numpy()
    y_true = y_val.cpu().numpy()

    print(classification_report(y_true, y_pred))
    print(f1_score(y_true, y_pred, average="macro"))

class F1_Race_Prediction(nn.Module):
  def __init__(self):
    super(F1_Race_Prediction, self).__init__()
    self.Input1 = nn.Linear(26, 120)
    self.Tanh = nn.Tanh()
    self.Drop1 = nn.Dropout(0.5)
    self.Input2 = nn.Linear(120, 120)
    self.Tanh = nn.Tanh()
    self.Drop2 = nn.Dropout(0.5)
    # its because we are returning an output
    self.Input4 = nn.Linear(120,4)
    # its because we are returning an output
   
    
    #Our 4 classes currently are outputed and given a probability via softmax - dim1 makes sure its applied across the class scores.
   

  def forward(self,x):
    out = self.Input1(x)
    out = self.Tanh(out)
    out = self.Drop1(out)
    out = self.Input2(out)
    out = self.Tanh(out)
    out = self.Drop2(out)
    out = self.Input4(out)
    
    #out = self.activitation(out)
    return out



def DataPrepANDRunModel():
  GetData = pl.read_csv("F1_Data/Prerace_Prediction.csv", separator=",", encoding="latin1",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)



  GetData = GetData.cast({"raceId": pl.Int64, "driverId" : pl.Int64, "qualifyId" : pl.Int64, "constructorId" : pl.Int64, "Result": pl.Int64,"resultId": pl.Int64, "grid": pl.Int64, "final_race_pos": pl.Int64,"points": pl.Int64, "year": pl.Int64, "Race_round": pl.Int64, "circuitId" : pl.Int64, "lat": pl.Float64, "lng": pl.Float64, "tempmax": pl.Float64,"tempmin": pl.Float64, "temp": pl.Float64, "dew": pl.Float64, "humidity": pl.Float64, "precip": pl.Float64, "snow": pl.Float64, "snowdepth": pl.Float64, "windspeed": pl.Float64, "cloudcover": pl.Float64, "ReachedQ2": pl.Int32, "ReachedQ3": pl.Int32,"SetQ1Time": pl.Int32, "Finished_Race": pl.Int32, "Q2_Millsec": pl.Int64,"Q3_Millsec": pl.Int64,"Q1_Millsec": pl.Int64,"race_time_hr": pl.Int64})
  #Splitting values between expected outcome as well as the data which is used to predict the race.

  #Exclude DNF's for now

  #This needs to be changed so any values after 2026 are classed differently
  GetData = GetData.filter(pl.col('final_race_pos') != 0)
  GetData = GetData.with_columns(pl.when(pl.col("final_race_pos") <= 3).then(0).when((pl.col("final_race_pos") > 3) & (pl.col("final_race_pos") <= 10) ).then(1).when((pl.col("final_race_pos") > 10) & (pl.col("final_race_pos") <= 15)).then(2).when((pl.col("final_race_pos") > 15) & (pl.col("final_race_pos") <= 24 )).then(3).alias('race_f'))

  print(GetData.select(
    (pl.col("final_race_pos") == 1).sum()
))
  print("//////")
  print(GetData.filter(pl.col("race_f") == 0).height)
  print("//////")
  print(GetData.filter(pl.col("race_f") == 1).height)
  print("//////")
  print(GetData.filter(pl.col("race_f") == 2).height)
  print("//////")
  print(GetData.filter(pl.col("race_f") == 3).height)
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
  

  model = F1_Race_Prediction()
  print(model)
  
  #Need to define our loss functions as well as optimizers - This will change as we will need an appropriate loss function
  loss_fn = torch.nn.CrossEntropyLoss(weight=torch.tensor([1,1,2,2.9]))

  #Leaning Rate - size of the steps the optimizer takes
  #Momentum nudges the optimizer in the direction of the strongest gradiant over multiple steps.
  optimizer = torch.optim.Adam(model.parameters(), lr=0.001)


  
  #Training and Validating our model
  TrainModel(epochIn,optimizer=optimizer,model=model,loss_fn=loss_fn,x_train=test_x, y_train=test_y,x_val=validate_x, y_val=validate_y)
  #Adding our differnet layers however may change this because we dont really need to do it like that - also sending this to the GPU
  torch.save(model.state_dict(), "model.pth")
  joblib.dump(scaler, "scaler.pkl")

DataPrepANDRunModel()


#Data needs to have some pre-processing done to it


# we need a training loop and a validation loop for our models