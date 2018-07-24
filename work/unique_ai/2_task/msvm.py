import numpy as np
import pandas as pd
import svm_1 as svm

# 初始化超参数
C = 500
sigma = 0.9
# 本来想指定分类次数的，但是考虑到处理标签，认为多分类改变类数还是需要定制

# 多分类SVM类将继承SVM的所有功能
class MultiSupportVectorMachine(svm.SupportVectorMachine):
    def __init__(C, sigma):
        self.C = C
        self.sigma = sigma
        self.k = self.rbf_kernel
        # 存储多个超平面的参数和训练数据分布
        self.all_alpha = []
        self.all_b = []
        self.all_x = []
        self.all_y = []

    # iris的数据预处理
    def iris_preprocessing(self):
        data = []
        with open('iris.data','r') as f1:
            content = f1.read()
            content = content.split('\n')
            data = [content[i].split(',') for i in range(0, len(content)-2)]
            for i in range(0, len(data)):
                # 为了区分三种花，用0-2编号
                if data[i][4] == 'Iris-setosa':
                    data[i][4] = 0
                elif data[i][4] =='Iris-versicolor':
                    data[i][4] = 1
                else:
                    data[i][4] = 2
                for j in range(0,4):
                    data[i][j] = float(data[i][j])
        data = np.array(data)
        # 对除结果列外的数据标准化
        mean_data = np.mean(data[:,:-1], axis=0)
        std_data = np.std(data[:,:-1], axis=0, ddof=1)
        data[:,:-1] = (data[:,:-1] - mean_data)/std_data
        # 训练集：验证集：测试集=3：1：1
        train_data, other = self.boostraping(data, 0.6)
        validate_data, test_data = self.boostraping(data, 0.5)
        # 实例绑定数据，此处的train_data只是原始训练数据
        self.train_data = train_data
        self.validate_data = validate_data
        self.test_data = test_data

    # 多分类训练函数
    def multi_train(self):
        # 进行等同类数目的分类，对每个样本给出分类结果，最后统计最终分类
        result = np.zeros(len(train_data),3)
        # 对每个类进行一次正反类训练
        for label in range(0,2):
            # 包含有单次训练和自适应过程
            self.sub_train(label)
    
    # 单分类函数，进行单次分类训练，指定要分为一类的标签
    def sub_train(self, label):
        # 准备第一次分类的数据
        x = self.train_data[:,:-1]
        y = self.train[:,-1]
        for i in range(0,len(y)):
            if y[i] == label:
                y[i] = 1.0
            else:
                y[i] = -1.0
        # 绑定第一次分类数据，开始第一次分类
        print("start first classifying:")
        self.x = x
        self.y = y
        self.train()
        self.validate(self.validate_data)
        # 把第一次分类的超平面参数存存储在列表中
        self.all_alpha.append(self.alpha)
        self.all_b.append(self.b)
    
    # 测试函数
    def multi_test(self):
        result = np.zeros((len(self.test_data),3))
        for i in range(0, len(self.all_alpha)):
            for j in range(0,len(test_data)):
                x_y = list(test_data[j])
                y = x_y.pop()
                x = np.array(x_y)
                r = sum([self.all_alpha[i][j]*self.all_y[i][j]*k(self.all_x[i][j],x)
                    for j in range(0,len(x))]) + self.all_b[i]
            if r > 0 and result[j][0]!=1:
                result[j][i] = 1
        acc = np.zeros((3,3))
        for i in range(0,len(self.test_data)):
            if result[i][0] == 1:
                acc[0][y] = acc[0][y] + 1
            elif result[i][1] == 1:
                acc[1][y] = acc[1][y] + 1
            else:
                acc[2][y] = acc[2][y] + 1
        print("result of class 1: %d %d %d" % (acc[0][0],acc[0][1],acc[0][2]))
        print("result of class 2: %d %d %d" % (acc[1][0],acc[1][1],acc[1][2]))
        print("result of class 3: %d %d %d" % (acc[2][0],acc[2][1],acc[2][2]))

def main():
    # 创建多分类SVM实例
    msvm = MultiSupportVectorMachine(C,sigma)
    msvm.iris_preprocessing()
    msvm.multi_train()
    msvm.multi_test()
if __name__ == "__main__":
    main()
