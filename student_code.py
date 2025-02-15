# python imports
import os
from tqdm import tqdm

# torch imports
import torch
import torch.nn as nn
import torch.optim as optim

# helper functions for computer vision
import torchvision
import torchvision.transforms as transforms


class LeNet(nn.Module):
    def __init__(self, input_shape=(32, 32), num_classes=100):
        super(LeNet, self).__init__()
        # certain definitions

        #Convolutional layer followed by relu activation layer and 2D max pooling layer
        self.conv1 = nn.Conv2d(out_channels=6, kernel_size=5, stride=1, in_channels=3)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        #Second convolutional layer followed by relu activation layer and 2D max pooling layer
        self.conv2 = nn.Conv2d(out_channels=16, kernel_size=5, stride=1, in_channels = 6)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        #Flatten layer
        self.flatten = nn.Flatten()

        #Linear layer 1 followed by relu
        self.fc1 = nn.Linear(16 * 5 * 5, 256)
        self.relu3 = nn.ReLU()

        #Linear layer 2 followed by relu
        self.fc2 = nn.Linear(256, 128)
        self.relu4 = nn.ReLU()

        #Linear layer 3
        self.fc3 = nn.Linear(128, num_classes)

    def forward(self, x):
        shape_dict = {}
        x = self.pool1(self.relu1(self.conv1(x)))
        shape_dict[1] = x.size()
        x = self.pool2(self.relu2(self.conv2(x)))
        shape_dict[2] = x.size()
        x = self.flatten(x)
        shape_dict[3] = x.size()
        x = self.relu3(self.fc1(x))
        shape_dict[4] = x.size()
        x = self.relu4(self.fc2(x))
        shape_dict[5] = x.size()
        x = self.fc3(x)
        shape_dict[6] = x.size()
        out = x
        return out, shape_dict


def count_model_params():
    '''
    return the number of trainable parameters of LeNet.
    '''
    model = LeNet()
    model_params = 0.0
    for p in model.parameters():
        model_params += p.numel()
    model_params = model_params/ 1000000
    return model_params


def train_model(model, train_loader, optimizer, criterion, epoch):
    """
    model (torch.nn.module): The model created to train
    train_loader (pytorch data loader): Training data loader
    optimizer (optimizer.*): A instance of some sort of optimizer, usually SGD
    criterion (nn.CrossEntropyLoss) : Loss function used to train the network
    epoch (int): Current epoch number
    """
    model.train()
    train_loss = 0.0
    for input, target in tqdm(train_loader, total=len(train_loader)):
        ###################################
        # fill in the standard training loop of forward pass,
        # backward pass, loss computation and optimizer step
        ###################################

        # 1) zero the parameter gradients
        optimizer.zero_grad()
        # 2) forward + backward + optimize
        output, _ = model(input)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        # Update the train_loss variable
        # .item() detaches the node from the computational graph
        # Uncomment the below line after you fill block 1 and 2
        train_loss += loss.item()

    train_loss /= len(train_loader)
    print('[Training set] Epoch: {:d}, Average loss: {:.4f}'.format(epoch+1, train_loss))

    return train_loss


def test_model(model, test_loader, epoch):
    model.eval()
    correct = 0
    with torch.no_grad():
        for input, target in test_loader:
            output, _ = model(input)
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_acc = correct / len(test_loader.dataset)
    print('[Test set] Epoch: {:d}, Accuracy: {:.2f}%\n'.format(
        epoch+1, 100. * test_acc))

    return test_acc
