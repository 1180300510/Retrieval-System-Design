import  struct
import numpy as np
import matplotlib.pyplot as plt
# 设置可以显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']# 用来显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示符号
def load_image(filename):
    with open(filename,"rb") as fd:
        # 读取图像信息
        header_buf = fd.read(16) # 16个字节，4 个int值
        # 解析数据
        magic_,num_,rows_,cols_ = struct.unpack('>iiii',header_buf)
        # 获取图像像素的信息
        imgs_ = np.fromfile(fd, dtype = np.uint8)
        imgs_ = imgs_.reshape(num_,rows_,cols_)
        print(num_)
    return imgs_
def load_label(filename):
     with open(filename,"rb") as fd:
        # 读取标签头的信息
        header_buf = fd.read(8) # 8个字节，2个int值
        # 解析数据
        magic_,num_= struct.unpack('>ii',header_buf)
        # 获取标签值的信息
        labels_ = np.fromfile(fd, dtype = np.uint8)
        return labels_


if __name__ == "__main__":
    # 读取训练数据集和测试数据集
    train_x = load_image("./APP/data/train-images.idx3-ubyte")
    train_y = load_label("./APP/data/train-labels.idx1-ubyte")
    test_x = load_image("./APP/data/t10k-images.idx3-ubyte")
    test_y = load_label("./APP/data/t10k-labels.idx1-ubyte")
    # print(train_x[0])
    # print(train_y[0])
    for i in range(2):
        ax1 = plt.subplot(121,title=F"训练数据集，标签：{train_y[i]}" )
        ax1.imshow(train_x[i],cmap="gray")
        ax1 = plt.subplot(122,title=F"测试数据集，标签：{test_y[i]}" )
        ax1.imshow(test_x[i],cmap="gray")
        plt.show()