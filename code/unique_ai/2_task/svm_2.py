import numpy as np
import pandas as pd
import random as rd

# 初始化超参数
K = 4
C = 500
sigma = 0.9 

class SupportVectorMachine():
    # 超参数初始化
    def __init__(self, K, C, sigma):
        self.K = K
        self.C = C
        self.sigma = sigma
        self.k = self.rbf_kernel
    
    # ------------------------------预处理组件-----------------------------
    # 预处理函数，对数据集进行预处理和划分，随机选择数据-------------------
    def preprocessing(self, t_o_rate, v_t_rate):
        dataSet = pd.read_csv("diabetes.csv", header=0)
        # 2号列“血压”存在0值，属于缺失属性，使用KNN算法进行修复
        data = self.knn_revover(dataSet, 2)
        # 按照训练：其他，验证：测试的比例划分数据集
        train_data, others = self.boostraping(data, t_o_rate)
        test_data, validate_data = self.boostraping(others, v_t_rate)
        # 训练数据直接绑定，验证数据和测试数据外流
        x = np.array(train_data[:,:-1])
        y = np.array(train_data[:,-1])
        self.x = x
        self.y = y
        return validate_data, test_data

    # 修复函数：对缺失数据集的re_col列进行修复，完成后直接传回array--------
    def knn_revover(self, dataSet, re_col):
        # 在numpy的支持下进行运算
        data = np.array(dataSet[1:])
        # 记录需修复样本的编号
        number = [i for i in range(0,len(data)) if data[i][re_col]==0]
        # 标准化,跳过结果列
        mean_data = np.mean(data[:,:-1], axis=0)
        std_data = np.std(data[:,:-1], axis=0, ddof=1)
        data[:,:-1] = (data[:,:-1] - mean_data)/std_data
        # 根据标准化后的数据计算L1距离来选点
        # 对每个恢复点
        for i in number:
            # 创建副本，应该不会被
            point_i = list(data[i][:])
            point_i.pop(-1)
            point_i.pop(re_col)
            point_i = np.array(point_i)
            distances = []
            values = [[] for i in range(0,self.K)]
            # 计算到每个不需恢复点的L1距离，更新或取距离最小的相应位置
            for j in range(0, len(data)):
                if j in number:
                    continue
                point_j = list(data[j][:])
                # 计算距离时不考虑恢复需属性和标记
                point_j.pop(-1)
                point_j.pop(re_col)
                point_j = np.array(point_j)
                distance = sum(np.square(point_i - point_j))
                # 判断是否比distances每个值都小
                for dis in distances:
                    if dis < distance:
                        distance = -1
                        break
                if distance >= 0:
                    # 选中点的相应值
                    value = point_j[re_col]
                    # 如果距离数目已经达到了要求
                    if len(distances) == K:
                        # 如果这个距离早就存在
                        if distance in distances:
                            num = distances.index(distance)
                            values[num].append(value)
                        # 否则这个距离不存在，需要替换原有最长距离
                        else:
                            num = distances.index(max(distances))
                            distances[num] = distance
                            values[num] = [value,]
                    # 缺少的话直接补上
                    else:
                        distances.append(distance)
                        values.append([value,])
            # 找完了最小距离，计算re_col平均值
            recover = [sum(v)/len(values) for v in values]
            recover = sum(recover)/len(recover)
            data[i,re_col] = recover
        # 修复完毕，re_col列标准化后，返回修复后的数据集合data
        mean_re_col = np.mean(data[:,re_col], axis=0)
        std_re_col = np.std(data[:,re_col], axis=0)
        data[:,re_col] = (data[:,re_col] - mean_re_col)/std_re_col
        # 结果列0-1元素用0.1-0.9元素
        for i in range(0, len(data)):
            if data[i][-1] == 1:
                data[i][-1] = 1.0
            if data[i][-1] == 0:
                data[i][-1] = -1.0
        return np.array(data)

    # 自助法函数，把一个嵌套列表结构的数据按照比例分成a,b两部分------------
    def boostraping(self, data, rate):
        # 实现自助法选择数据，要求按照rate的比例得到数据集a
        a_numbers = []
        while len(a_numbers) < rate*len(data):
            add = rd.randint(0, len(data)-1)
            for i in range(0,len(a_numbers)):
                if add == a_numbers[i]:
                    add = -1
                    break
            if add != -1:
                a_numbers.append(add)
        a_data = [data[i] for i in a_numbers]
        # 剩下的数据分为b类
        b_numbers = [i for i in range(0, len(data)) if i not in a_numbers]
        b_data = [data[i] for i in b_numbers]
        return np.array(a_data), np.array(b_data)

    # -------------------------------训练组件------------------------------
    # 训练函数，根据训练集，核函数训练迭代---------------------------------
    def train(self):
        k = self.k
        x = self.x
        y = self.y
        # 参数初始化:alpha和b
        alpha = np.random.rand(len(x))
        # 保证约束条件，不妨用第一个来开刀
        alpha[0] = alpha[0] - sum([alpha[j]*y[j]
            for j in range(0,len(x))])/y[0]
        b = rd.random()
        # 计算起始误差
        e = []
        for i in range(0,len(x)):
            ui = sum([alpha[j]*y[j]*k(x[j],x[i])
                for j in range(0,len(x))]) - b
            ei = ui - y[i]
            e.append(ei)
        # 准备训练数据
        step = 1
        turn = 0
        while step <= 6:
            turn = turn + 1
            # 计算罚函数大小
            # lost = np.zeros((len(x),len(x)))
            # for i in range(0,len(x)):
                # for j in range(0,i+1):
                    # lost[i][j] = y[i]*y[j]*k(x[i],x[j])*alpha[i]*alpha[j]
                    # lost[j][i] = lost[i,j]
            # loss = 0.5*np.sum(lost) - np.sum(alpha)
            # 选出违反KKT条件最严重的两个点
            distances = [abs(alpha[i]-0.5*self.C) for i in range(0,len(x))]
            if max(distances) <= 0.5*self.C:
                m = rd.randint(0,len(x)-1)
                n = rd.randint(0,len(x)-1)
            else:    
                m = distances.index(max(distances))
                n = rd.randint(0,len(x)-1)
                while m == n:
                    n = rd.randint(0,len(x)-1)
            # else:
                # m = distances.index(max(distances))
                # n = rd.randint(0,len(x)-1)
                # while m==n:
                    # n = rd.randint(0,len(x)-1)
            new_m, new_n, b, e = self.SMO(alpha, b, e, m, n)
            # print(turn,step,sum([abs(el) for el in e]))
            print(step, turn, m, n)
            print("m:",alpha[m],"->",new_m,"(",new_m-alpha[m],")")
            print("n:",alpha[n],"->",new_n,"(",new_n-alpha[n],")")
            if abs(new_m-alpha[m])+abs(new_n-alpha[n]) < 0.1:
                step = step + 1
            else:
                step = 1
            alpha[m] = new_m
            alpha[n] = new_n
        # 动态绑定必须数据
        self.alpha = alpha
        self.b = b

    # SMO优化函数，返回单次SMO结果-----------------------------------------
    def SMO(self, alpha, b, e, m, n):
        k = self.k
        x = self.x
        y = self.y
        # 1、计算上下界L和H
        if y[m] != y[n]:
            L = max([0, alpha[n]-alpha[m]])
            H = min([self.C, self.C+alpha[n]-alpha[m]])
        else:
            L = max([0, alpha[m]+alpha[n]-self.C])
            H = min([self.C, alpha[m]+alpha[n]])
        # 2、计算Ls的二阶导数
        yita = k(x[m],x[m]) + k(x[n],x[n]) - 2*k(x[m],x[2])
        # 3、计算新alpha
        new_n = alpha[n] + y[n]*(e[m] - e[n])/yita
        if new_n >= H:
            new_n = H
        elif new_n <=L:
            new_n = L
        else:
            pass
        new_m = alpha[m] + y[m]*y[n]*(alpha[n] - new_n)
        bm = b + e[m] + y[m]*(new_m-alpha[m])*k(x[m],x[m]) 
        bm = bm + y[n]*(new_n-alpha[n])*k(x[m],x[n])
        bn = b + e[n] + y[m]*(new_m-alpha[m])*k(x[m],x[n]) 
        bn = bn + y[n]*(new_n-alpha[n])*k(x[n],x[n])
        # 根据情况更新b
        situation_1 = new_m > 0 and new_m < self.C
        situation_2 = new_n > 0 and new_n < self.C
        if situation_1:
            b = bm
        elif situation_2:
            b = bn
        else:
            b = (bm + bn)/2
        # 更新e
        for i in range(0,len(x)):
            ui = sum([alpha[j]*y[j]*k(x[j],x[i])
                for j in range(0,len(x))
                if j!=m and j!=n]) - b
            ui = ui + new_m*y[m]*k(x[m],x[i]) + new_n*y[n]*k(x[n],x[i])
            ei = ui - y[i]
            e[i] = ei
        return  new_m, new_n, b, e

    # 高斯核函数-----------------------------------------------------------
    def rbf_kernel(self, xi, xj):
        sigma = self.sigma
        result = np.exp(-sum(np.square(xi - xj))/(2*sigma*sigma))
        return result
        
    # -------------------------------验证组件------------------------------
    # 验证函数，根据验证数据选出最佳超参数（自适应过程）-------------------
    def validate(self, validate_data):
        k = self.k
        # 初始化迭代轮数和最小错误率
        error = 1
        turn = 0
        # 自适应迭代
        while turn < 2:
            turn = turn + 1
            # 选择超参数
            C = rd.randint(10,1000)
            sigma = rd.random()
            # 训练模型
            alpha = self.alpha.copy()
            b = self.b
            self.train()
            # 测试结果
            accuracy = self.test(validate_data)
            # 正确率有所提高便更新参数
            if 1 - accuracy < error:
                error = 1 - accuracy
                self.C = C
                self.sigma = sigma
            else:
                self.alpha = alpha
                self.b = b
        print("the accuracy of svm in validation is: %f" % (1.0-error))

    # -------------------------------测试组件------------------------------
    def test(self, test_data):
        k = self.k
        accuracy = 0
        for x_y in test_data:
            # 对测试集拆包
            x_y = list(x_y)
            y = x_y.pop()
            x = np.array(x_y)
            result = sum([self.alpha[j]*self.y[j]*k(self.x[j],x)
                for j in range(0,len(x))]) - self.b
            # 分类与实际一致
            if y*result >= 0:
                accuracy = accuracy + 1
        # 统计出正确率
        accuracy = accuracy / len(test_data)
        return accuracy

def main():
    # 创建SVM实例
    svm = SupportVectorMachine(K, C, sigma)
    # 训练集：验证集：测试集 = 4：1：1，训练数据已经直接保留
    validate_data, test_data = svm.preprocessing(0.8, 0.5)
    # 训练得到最优参数训练
    svm.train()
    # 自适应得到最佳超参数
    svm.validate(validate_data)
    # 除了训练和测试过程中打印结果之外，最后再打印一次测试结果
    accuracy = svm.test(test_data)
    print("the supperparamenter are: C: %f; sigma: %f"
            % (svm.C, svm.sigma))
    print("the accuracy of svm in test is %f" % accuracy)

if __name__ == "__main__":
    main()
