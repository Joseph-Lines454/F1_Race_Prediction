import polars as pl
import numpy as np
import torch
from torch import nn


#We still need to do some pre-proccessing to the data - For qualifying data we need to use an arbitary value with out binary indicator flag (Reached Q2 ect)
#Values also need to be encoded because some are in string formats which ML models do not like

GetData = pl.read_csv("F1_Data/Prerace_Prediction.csv", separator=",", encoding="latin1",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)
GetData = GetData.cast({"raceId": pl.Int64, "driverId" : pl.Int64, "qualifyId" : pl.Int64, "constructorId" : pl.Float64, "Result": pl.Int64,"resultId": pl.Int64, "grid": pl.Int64, "final_race_pos": pl.Int64,"points": pl.Int64, "year": pl.Int64, "Race_round": pl.Int64, "circuitId" : pl.Int64, "lat": pl.Float64, "lng": pl.Float64, "tempmax": pl.Float64,"tempmin": pl.Float64, "temp": pl.Float64, "dew": pl.Float64, "humidity": pl.Float64, "precip": pl.Float64, "snow": pl.Float64, "snowdepth": pl.Float64, "windspeed": pl.Float64, "cloudcover": pl.Float64, "ReachedQ2": pl.Int32, "ReachedQ3": pl.Int32,"SetQ1Time": pl.Int32, "Finished_Race": pl.Int32, "Q2_Millsec": pl.Int64,"Q3_Millsec": pl.Int64,"Q1_Millsec": pl.Int64,"race_time_hr": pl.Int64})
#Splitting values between expected outcome as well as the data which is used to predict the race.
y = GetData.select(['final_race_pos','Finished_Race']).to_numpy()
x = GetData.select(pl.all().exclude(['final_race_pos','Finished_Race','resultId','points','raceId','driverId','qualifyId', 'date'])).to_numpy()

#Have split data for training and testing

y = torch.from_numpy(y)
x = torch.from_numpy(x)

#------ NEED TO ADD 3 EXTRA DIMENSIONS TO THE TENSOR AND PUSH THESE  -------

#Embedding our RaceID
embedding = nn.Embedding(num_embeddings=5810, embedding_dim=1)
#input shape from numpy is [5810,1] so with embedding_dim=1 makes it [5810,1,1]
embed = embedding(torch.from_numpy(GetData.select(['raceId']).to_numpy())).squeeze(1)

#Adds the shape of the tensors together dim=1 is to specify to add as columns not rows
x = torch.cat((x, embed), dim=1)



#Embedding our DriverID
embedding = nn.Embedding(num_embeddings=5810, embedding_dim=1)
embed = embedding(torch.from_numpy(GetData.select(['driverId']).to_numpy())).squeeze(1)


#Adds the shape of the tensors together dim=1 is to specify to add as columns not rows
x = torch.cat((x, embed), dim=1)

#Now we need these in seperate tensors
row_split_check_x = torch.split(x,[4066,1743],dim=0)
test_x, validate_x = row_split_check_x

row_split_check_y = torch.split(x,[4066,1743],dim=0)
test_y, validate_y = row_split_check_y

test_y, validate_y = row_split_check_y

test_x = test_x.to(torch.float32)
validate_x = validate_x.to(torch.float32)
test_y = test_y.to(torch.float32)
validate_y = validate_y.to(torch.float32)

print(test_y.shape)
print(validate_y.shape)



device = torch.accelerator.current_accelerator().type
#converting our data to tensors from numpy once we have split the data


#THIS NEEDS FIXING
#x_train = torch.from_numpy(x_train)
#x_test = torch.from_numpy(x_test)
#y_train = torch.from_numpy(y_train)
#y_test = torch.from_numpy(y_test)




#Trainning model for our data
def TrainModel(epochs, optimizer, model, loss_fn, x_train, y_train):
  for epoch in range (1, epochs + 1):
    x_trained = model(x_train)
    loss = loss_fn(x_trained,y_train)

    #Reset gradiant back to zero so gradient does not accumulate
    #Backpropagation
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
  if epoch % 50 == 0:
    print("Epoch: " + str(epoch) + " Training Loss: " + str(loss))


def ValidateModel(epochs, model, loss_fn,x_val, y_val):
  #We dont want to calculate gradiant becuase we are not improving the model, we are validating our data
  with torch.zero_grad():
    for epoch in range (1, epochs + 1):
      x_validate = model(x_val)
      #Checking loss on out data
      loss = loss_fn(x_validate,y_val)
      
      #print The loss if epoch is equal to 50
      if epoch % 50 == 0:
        print("Epoch: " + str(epoch) + " Training Loss: " + str(loss))



class F1_Race_Prediction(nn.Module):
  def __init__(self):
    super(F1_Race_Prediction, self).__init__()
    self.Input1 = nn.Linear(29, 130)
    self.relu = nn.Tanh()
    # its because we are returning an output
    self.Input2 = nn.Linear(130,29)

  def forward(self,x):
    out = self.Input1(x)
    out = self.relu(out)
    out = self.Input2(out)
    return out


#Adding our differnet layers however may change this because we dont really need to do it like that - also sending this to the GPU
model = F1_Race_Prediction()
print(model)

#Need to define our loss functions as well as optimizers - This will change as we will need an appropriate loss function
loss_fn = torch.nn.MSELoss()

#Leaning Rate - size of the steps the optimizer takes
#Momentum nudges the optimizer in the direction of the strongest gradiant over multiple steps.
optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

#Training and Validating our model
TrainModel(6000,optimizer=optimizer,model=model,loss_fn=loss_fn,x_train=test_x, y_train=test_y)
#ValidateModel()

#Data needs to have some pre-processing done to it


# we need a training loop and a validation loop for our models