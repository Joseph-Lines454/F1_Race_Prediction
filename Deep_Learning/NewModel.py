import polars as pl
import numpy as np
import torch
from torch import nn
from sklearn.model_selection import train_test_split


#We still need to do some pre-proccessing to the data - For qualifying data we need to use an arbitary value with out binary indicator flag (Reached Q2 ect)
#Values also need to be encoded because some are in string formats which ML models do not like

GetData = pl.read_csv("F1_Data/Prerace_Prediction.csv", separator=",", encoding="latin1",null_values=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"], ignore_errors=True)

#Splitting values between expected outcome as well as the data which is used to predict the race.
y = GetData.select(['final_race_pos','Finished_Race']).to_numpy()
x = GetData.select(pl.all().exclude(['final_race_pos','Finished_Race'])).to_numpy()

#Have split data for training and testing
x_train,x_test, y_train, y_test  = train_test_split(x,y, test_size=0.7, random_state=4)

#Still need to do some preprocessing which is important for this project
#because if it does not recognise inputs, this could be an issue

device = torch.accelerator.current_accelerator().type
#converting our data to tensors from numpy once we have split the data
x_train = torch.from_numpy(x_train)
x_test = torch.from_numpy(x_test)
y_train = torch.from_numpy(y_train)
y_test = torch.from_numpy(y_test)


def DataEncodingForModel():
  #Embeddings for raceID as well as driverID and circuitID - Higher values are not better than lower values for example.
  

  print("Data Encoding")

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
    self.Input1 = nn.Linear(33, 120)
    self.relu = nn.ReLU()
    self.Input2 = nn.Linear(64,20)

  def forward(self,x):
    out = self.Input1(x)
    out = self.relu(out)
    out - self.Input2(out)
    return out
#nn.CrossEntropyLoss is a good choice for the ML model
input_dim = 784
hidden_dim = 128
output_dim = 10

#Adding our differnet layers however may change this because we dont really need to do it like that - also sending this to the GPU
model = F1_Race_Prediction().to(device)
print(model)

#Need to define our loss functions as well as optimizers - This will change as we will need an appropriate loss function
loss_fn = torch.nn.CrossEntropyLoss()

#Leaning Rate - size of the steps the optimizer takes
#Momentum nudges the optimizer in the direction of the strongest gradiant over multiple steps.
optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

#Training and Validating our model
TrainModel()
ValidateModel()




# we need a training loop and a validation loop for our models