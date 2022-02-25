import torch
import torch.nn.functional as F
from model import LeNet5
import loader
# net = LeNet5()
# y = torch.randint(5,10,[1,1,28,28])
# y = torch.Tensor(y.numpy())
# y_ = net(y)
# print(y_)
# 1. 加载数据集
train_x = loader.load_image("./APP/data/train-images.idx3-ubyte")
train_y = loader.load_label("./APP/data/train-labels.idx1-ubyte")
test_x = loader.load_image("./APP/data/t10k-images.idx3-ubyte")
test_y = loader.load_label("./APP/data/t10k-labels.idx1-ubyte")
# print(train_x.shape)
# print(train_y.shape)
# print(test_x.shape)
# print(test_y.shape)
# 2. 数据处理
train_x = torch.Tensor(train_x).view(train_x.shape[0],1,train_x.shape[1],train_x.shape[2])#N,C,H,W
train_y = torch.LongTensor(train_y)
test_x = torch.Tensor(test_x).view(test_x.shape[0],1,test_x.shape[1],test_x.shape[2])#N,C,H,W
test_y = torch.LongTensor(test_y)
# print(train_x.shape)
# print(train_y.shape)
# print(test_x.shape)
# print(test_y.shape)
# 实例化模型
net = LeNet5()

# 3. 模型训练

# 3.1 定义一个学习率
learn_rate = 0.001
# 3.2 定义学习规则
@torch.enable_grad()
def loss_model(out,target):
    loss_ = F.cross_entropy(out,target)
    return loss_
    
# 3.3 定义一个迭代轮数
epochs = 10
# 3.4 迭代训练
for epoch in range(epochs):
    # 模型预测
    output = net(train_x)
    # 计算损失值
    loss = loss_model(output,train_y)
    # 计算梯度
    loss.backward()
    # 梯度更新
    with torch.autograd.no_grad():

        net.w_6_5_5 -= learn_rate*net.w_6_5_5.grad
        net.b_6_5_5 -= learn_rate* net.b_6_5_5.grad

        net.w_16_5_5 -= learn_rate * net.w_16_5_5.grad
        net.b_16_5_5 -= learn_rate* net.b_16_5_5.grad

        net.w_120_5_5 -= learn_rate * net.w_120_5_5.grad
        net.b_120_5_5 -= learn_rate* net.b_120_5_5.grad

        net.w_120_84 -= learn_rate * net.w_120_84.grad
        net.b_120_84 -= learn_rate* net.b_120_84.grad

        net.w_84_10 -= learn_rate * net.w_84_10.grad
        net.w_84_10 -= learn_rate* net.w_84_10.grad
        # 复原梯度，即梯度置零
        net.w_6_5_5.grad.zero_()
        net.b_6_5_5.grad.zero_()
        net.w_16_5_5.grad.zero_()
        net.b_16_5_5.grad.zero_()
        net.w_120_5_5.grad.zero_()
        net.b_120_5_5.grad.zero_()
        net.w_120_84.grad.zero_()
        net.b_120_84.grad.zero_()
        net.w_84_10.grad.zero_()
        net.b_84_10.grad.zero_()


    # 打印损失值，观察收敛的情况
    print(F"第{epoch:03d}轮：")
    print(F"\t损失值：{loss:8.6f}",end = "")
    # 测试数据集
    with torch.autograd.no_grad():
        pre = net(test_x)
        # 计算准确率
        t_y_ = pre.argmax(dim=1)
        right_rate = (t_y_ == test_y).float().mean()
        print(F"\t测试集准确率：{right_rate*100:6.2f}%")
    
print("******训练完毕******")
# 4. 保存模型
torch.save(net.state_dict(),"lenet.pth")