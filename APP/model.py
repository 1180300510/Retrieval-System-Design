import torch
import torch.nn as nn
from torch.nn import Module
import math
class LeNet5(Module):
    def __init__(self):
        super(LeNet5,self).__init__()
        # 1. 初始化参数，即权重和偏置,sigmoid函数的w和b
        # 1.1 
        self.w_6_5_5 = torch.Tensor(6,1,5,5)# (C_out,C_in,H_k,W_k)
        self.b_6_5_5 = torch.Tensor(6)
        stdv = 1.0/math.sqrt(1*5*5)
        self.w_6_5_5.data.uniform_(-stdv,stdv)
        self.b_6_5_5.data.uniform_(-stdv,stdv)
        # 1.2 
        self.w_16_5_5 = torch.Tensor(16,6,5,5)# (C_out,C_in,H_k,W_k)
        self.b_16_5_5 = torch.Tensor(16)
        stdv = 1.0/math.sqrt(6*5*5)
        self.w_16_5_5.data.uniform_(-stdv,stdv)
        self.b_16_5_5.data.uniform_(-stdv,stdv)
        # 1.3
        self.w_120_5_5 = torch.Tensor(120,16,5,5)# (C_out,C_in,H_k,W_k)
        self.b_120_5_5 = torch.Tensor(120)
        stdv = 1.0/math.sqrt(16*5*5)
        self.w_120_5_5.data.uniform_(-stdv,stdv)
        self.b_120_5_5.data.uniform_(-stdv,stdv)
        # 1.4 
        self.w_120_84 = torch.Tensor(84,120)# (C_out,C_in,H_k,W_k)
        self.b_120_84 = torch.Tensor(84)
        stdv = 1.0/math.sqrt(120)
        self.w_120_84.data.uniform_(-stdv,stdv)
        self.b_120_84.data.uniform_(-stdv,stdv)
        #1.5
        self.w_84_10 = torch.Tensor(10,84)# (C_out,C_in,H_k,W_k)
        self.b_84_10 = torch.Tensor(10)
        stdv = 1.0/math.sqrt(84)
        self.w_84_10.data.uniform_(-stdv,stdv)
        self.b_84_10.data.uniform_(-stdv,stdv)
        # 2.将初始化参数设置为可求导
        self.w_6_5_5.requires_grad = True
        self.b_6_5_5.requires_grad = True
        self.w_16_5_5.requires_grad = True
        self.b_16_5_5.requires_grad = True
        self.w_120_5_5.requires_grad = True
        self.b_120_5_5.requires_grad = True
        self.w_120_84.requires_grad = True
        self.b_120_84.requires_grad = True
        self.w_84_10.requires_grad = True
        self.b_84_10.requires_grad = True
    # 2. 定义forward 实现卷积池化全连接的操作，提取特征进行预测
    def forward(self,inputs):
        # 1.layer1 进行卷积池化操作C1和S2
        x = nn.functional.conv2d(input = inputs,weight = self.w_6_5_5,bias=self.b_6_5_5,padding=2)
        x = nn.functional.relu(x)
        x = nn.functional.max_pool2d(input = x,kernel_size=(2,2))
        # 2.layer2 进行卷积池化操作C3和S4
        x = nn.functional.conv2d(input = x,weight = self.w_16_5_5,bias=self.b_16_5_5)
        x = nn.functional.relu(x)
        x = nn.functional.max_pool2d(input = x,kernel_size=(2,2))
        # 3.layer3 进行卷积操作C5
        x = nn.functional.conv2d(input = x,weight = self.w_120_5_5,bias=self.b_120_5_5)
        x = nn.functional.relu(x)
        # 进行维度的转换
        x = x.view(x.shape[0],x.shape[1])
        # 4. layers4 全连接层
        x = nn.functional.linear(x,self.w_120_84,self.b_120_84)
        x = nn.functional.relu(x)
        # 5. layers5 全连接层
        x = nn.functional.linear(x,self.w_84_10,self.b_84_10)
        x = nn.functional.softmax(x,dim=1)
        # x = nn.functional.log_softmax(x,dim=1)
        return x
