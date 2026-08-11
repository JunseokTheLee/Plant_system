import os                       # for working with files
import numpy as np              # for numerical computationss
import pandas as pd             # for working with dataframes
import torch                    # Pytorch module 
import matplotlib.pyplot as plt # for plotting informations on graph and images using tensors
import torch.nn as nn           # for creating  neural networks
from torch.utils.data import DataLoader # for dataloaders 
from PIL import Image           # for checking images
import torch.nn.functional as F # for functions for calculating loss
import torchvision.transforms as transforms   # for transforming images into tensors 
from torchvision.utils import make_grid       # for data checking
from torchvision.datasets import ImageFolder  # for working with classes and images
from torchsummary import summary   
class_count = 38

def show_image(image, label):
    print("Label :" + train.classes[label] + "(" + str(label) + ")")
    plt.imshow(image.permute(1, 2, 0))
    plt.show()
data_dir = "../new-plant-diseases-dataset/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)"
train_dir = data_dir + "/train"
valid_dir = data_dir + "/valid"
diseases = os.listdir(train_dir)
print(diseases)

train  = ImageFolder(train_dir, transform = transforms.ToTensor())

valid  = ImageFolder(valid_dir, transform = transforms.ToTensor())


img, label = train[0]
print(img.shape, label)

random_seed = 10
torch.manual_seed(random_seed)
batch_size = 32


train_dl = DataLoader(train, batch_size, shuffle = True, num_workers = 1, pin_memory = True)
test_dl = DataLoader(valid, batch_size, num_workers = 1, pin_memory = True)

#-------

def get_default_device():
    if torch.cuda.is_available:
        return torch.device("cuda")
    else:
        return torch.device("cpu")
def to_device(data, device):
    if isinstance(data, (list, tuple)):
        return [to_device(x,device) for x in data]
    return data.to(device, non_blocking = True  )
class DeviceDataLoader():
    def __init__(self, dl, device):
        self.dl = dl
        self.device = device
    def __iter__(self):
        for b in self.dl:
            yield to_device(b, self.device)  

  

device = get_default_device()ccx                                                                                                                                                    x                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  x
print(device)
train_dl = DeviceDataLoader(train_dl, device)
test_dl = DeviceDataLoader(test_dl, device)


