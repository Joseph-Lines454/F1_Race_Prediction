import os
import torch
from torch import nnn
from torch.utils.data import Dataloader
from torchvision import datasets, transforms
from torchvision.transforms import ToTensor, Lambda

ds = datasets.FashionMNIST(
  root = "data",
  train = True,
  download = True,
  #converting image from image or numpy array to pytorch tensor
  transform = ToTensor(),
  #label - takes y label. creates a vector of zeros of length 10 and scatter places 1 at the index of the label - Lamdba function
  target_transform = Lambda(lambda y: torch.zeros(10,dtype=torch.float).scatter_(0,torch.tensor(y), value = 1))
)


device = torch.accelerator.current_accelerator().type

