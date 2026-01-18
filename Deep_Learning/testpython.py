import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor




training_data = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor(),
)

test_data = datasets.FashionMNIST(
    root="data",
    train=False,
    download=True,
    transform=ToTensor(),
)

batch_size = 64
train_dataloader = DataLoader(training_data, batch_size=batch_size)
test_dataloader = DataLoader(test_data, batch_size=batch_size)



"""
for X,y in test_dataloader:
  print("Shape of X: " + str(X.shape))
  print("Shape of Y: " + str(y.shape) + "and y data type: " + str(y.dtype))
  break
"""



device = torch.accelerator.current_accelerator().type
print("Device: " + device)



#We are doing this so we can inhert the base classes features
class NeuralNetwork(nn.Module):
  def __init__(self):
    #Initialises nn.Module paramater
    super().__init__()
    #Flatten converts image tensors into vectors
    self.flatten = nn.Flatten()
    #Sequential is becuase the layers stack ontop of eachother
    self.linear_relu_stack = nn.Sequential(
      #748 pixel values and 512 features - 
      nn.Linear(28 * 28, 512),
      #Takes away negative values and adds non-linearity
      nn.ReLU(),
      #512 learnt features and outputs 512 refined features
      nn.Linear(512,512),
      #same as previous
      nn.ReLU(),
      nn.Linear(512,10),
    )
  def forward(self,x):
    x = self.flatten(x)
    logits = self.linear_relu_stack(x)
    return logits

  



def train(dataloader, model, loss_fn, optmizer):
    #size of data set
    size = len(dataloader.dataset)
    #train model paramater - we are actually trainning our model
    model.train()
    #for each batch
    for batch, (X,y) in enumerate(dataloader):
      #pass to the GPU cuda - X is batch input data and y is the corresponding labels
      X,y = X.to(device), y.to(device)
      #actually trainning the model on out batch data
      pred = model(X)
      #finding the loss from the pred that we did on the X batch data and comparing it with the y label to calculate loss
      loss = loss_fn(pred,y)
      #Linked to line above, computing gradient which is inaccurate.
      loss.backward()
      # Updates model paramaters to allow for higher accuracy
      optmizer.step()
      #Sets gradients value to zero for next batch of data
      optmizer.zero_grad()
      #
      if batch % 50 == 0:
        # get loss and how many batches have been passed through, we are looking at how the model optmizes throughout the run through epoch (one whole pass of data)
        loss, current = loss.item(), (batch + 1) * len(X)
        print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")
  
def test(dataloader, model, loss_fn):
  #samples in dataset
  size = len(dataloader.dataset)
  #batches in dataset
  num_bratches = len(dataloader)
  #evaluationj mode
  model.eval()
  test_loss = 0
  correct = 0
  # we are not using the gradient becuase we do not need it when testing data - we are not optmising the model - hench why we haven't passed the optmizer into the test function
  with torch.no_grad():
    for X, y in dataloader:
      #Sending to GPU
      X,y = X.to(device), y.to(device)
      #Passing data to the model
      pred = model(X)
      # accumiulating test loss, item()is a convertion to float
      test_loss +=  loss_fn(pred,y).item()
      #argmax selects class with highest score for each sample, also compares predictions to true labels (y).
      #.type() is used to convert bool to float. The .sum() and .item() gets the predictions which are correct (because type is either 1 or 0)
      correct += (pred.argmax(1) == y).type(torch.float).sum().item()
  #avarage loss per batch
  test_loss = test_loss / num_bratches
  #accuracy
  correct = correct / size
  print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

model = NeuralNetwork().to(device)
print(model)
loss_fn = nn.CrossEntropyLoss()
optmizer = torch.optim.SGD(model.parameters(), lr=1e-3)
#Creating a dummy image
X = torch.rand(1,28,28, device=device)

#we want to pass through this data five times

epoch = 5

for i in range(epoch):
  print("Epoch: " + str(i + 1))
  train(train_dataloader,model,loss_fn,optmizer)
  test(test_dataloader, model, loss_fn)


#pass image into our model
#logits = model(X)
#print(str(logits))
#convert the logits for each class into a probability using the Softmax function
#pred_probab = nn.Softmax(dim=1)(logits)
#print("How confident model is for each class:" + str(pred_probab))
#Picks maximum probability
#y_pred = pred_probab.argmax(1)
#print("Prediction: " + str(y_pred))

torch.save(model.state_dict(), "model.pth")
print("Saved???")