import torch
import torch.nn.functional as F
import loader#读取数据

train_x = loader.load_image("./APP/data/train-images.idx3-ubyte")
train_y = loader.load_label("./APP/data/train-labels.idx1-ubyte")
test_x = loader.load_image("./APP/data/t10k-images.idx3-ubyte")
test_y = loader.load_label("./APP/data/t10k-labels.idx1-ubyte")
print(train_x.shape)
print(train_y.shape)
print(test_x.shape)
print(test_y.shape)