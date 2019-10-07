import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()

        self.fc1 = nn.Linear(10,20) 
        self.fc2 = nn.Linear(20, 20)
        self.fc3 = nn.Linear(20, 20)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.softmax(self.fc3(x))
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features


net = Net()
print(net)

input = torch.randn(10)
out = net(input)
print(out)


input = torch.randn(10)
out = net(input)
print(out)

l=[]

model_parameters = filter(lambda p: p.requires_grad, net.parameters())
params = sum([np.prod(p.size()) for p in model_parameters])
print(params)

newparams = [i for i in range(params)]
# print(newparams)

index = 0
numparams = 0
for p in net.parameters():
    start = index
    layersize = np.prod(p.size())
    new_layer_params = [(newparams[start+j])/params for j in range(layersize)]
    print(new_layer_params)
    index+=layersize
    numparams+=layersize
    print(p)
    p = Parameter(torch.tensor(new_layer_params))
    print(p)

print(numparams)
print(params)


    # layerparams=1
    # print(p.shape)
    # s = p.shape
    # for dim in s:
    #     layerparams*=dim
    # i = 0
    # t = torch.ones(p.shape)
    # for v in t:
    #     v = i
    #     i = i+1
    #     p = Parameter(t)
    # print(p)
  # see tuple

# print("Printing parameters")
# numparams = 0
# for p in net.parameters():
#     layerparams=1
#     print(p.shape)
#     s = p.shape
#     for dim in s:
#         layerparams*=dim
#     i = 0
#     t = torch.ones(p.shape)
#     for v in t:
#         v = i
#         i = i+1
#         p = Parameter(t)
#     print(p)
#     numparams+=layerparams
# 	# see tuple

# print(numparams)






print(l)

