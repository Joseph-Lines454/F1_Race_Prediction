import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor



""""
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

model = NeuralNetwork().to(device)
print(model)

#Creating a dummy image
X = torch.rand(1,28,28, device=device)
#pass image into our model
logits = model(X)
print(str(logits))
#convert the logits for each class into a probability using the Softmax function
pred_probab = nn.Softmax(dim=1)(logits)
print("How confident model is for each class:" + str(pred_probab))
#Picks maximum probability
y_pred = pred_probab.argmax(1)
print("Prediction: " + str(y_pred))

