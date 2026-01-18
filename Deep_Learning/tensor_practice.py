import torch
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
import numpy as np



#Tensor is a data structure

#data = [[1,2],[3,4]]
#x_data = torch.tensor(data)



#tensor = torch.ones(4,4)
#print(tensor)
#print("//////////////")
#print("First row: " + str(tensor[0]))
#print("//////////////")
#tensor[:,1] = 0
#tensor = tensor.to(torch.accelerator.current_accelerator())
#print(tensor)

training_data_example = datasets.FashionMNIST(
  root="data",
  train=True,
  download=True,
  transform=ToTensor()
)

test_data = datasets.FashionMNIST(
  root="data",
  train=False,
  download=True,
  transform=ToTensor()
)

#Visualising datasets

labels_map = {
    0: "T-Shirt",
    1: "Trouser",
    2: "Pullover",
    3: "Dress",
    4: "Coat",
    5: "Sandal",
    6: "Shirt",
    7: "Sneaker",
    8: "Bag",
    9: "Ankle Boot",
}

figure = plt.figure(figsize=(8,8))
cols = 3
rows = 3
for i in range(1, cols * rows + 1):
  #Finding amounrt of elements, generating random inr and return a single tensor then convert to float
  sample_idx = torch.randint(len(training_data_example), size = (1,)).item()
  img,label = training_data_example[sample_idx]
  figure.add_subplot(rows,cols,i)
  plt.title(labels_map[label])
  plt.axis("off")
  plt.imshow(img.squeeze(),cmap="gray")
plt.show()





