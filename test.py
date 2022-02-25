import torch
import cv2

y = torch.randint(5,10,[2,1,1])
y = torch.Tensor(y.numpy())
print(y)