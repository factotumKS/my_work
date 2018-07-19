import numpy as np
import pandas as pd
import randome as rd

# 初始化超参数
K = 4

# ------------------------------预处理组件---------------------------------
# 预处理函数，对数据集进行预处理和划分，随机选择数据-----------------------
def preprocessing(t_o_rate, v_t_rate):
    dataSet = pd.read_csv("diabetes.csv", header=0)
    # 2号列“血压”存在0值，属于缺失属性，使用KNN算法进行修复
    data = knn_revover(dataSet, 2)
    # 按照训练：其他，验证：测试的比例划分数据集
    train_data, others = boostraping(data, t_o_rate)
    test_data, validate_data = boostraping(others, v_t_rate)
    return train_data, validate_data, test_data

# 修复函数：对缺失数据集的re_col列进行修复，完成后直接传回array------------
def knn_revover(dataSet, re_col):
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
    for i in number：
        distances = []
        values = [[] for i in range(0,K)]
        # 计算到每个不需恢复点的L1距离，更新或取距离最小的相应位置
        for j in range(0, len(data)) and j not in number:
            point_i = list(data[i][:])
            point_j = list(data[j][:])
            # 计算距离时不考虑恢复需属性和标记
            value = point_i.pop(-1).pop(re_col)
            point_j.pop(-1).pop(re_col)
            point_i = np.array(point_i)
            point_j = np.array(point_j)
            distance = sum(np.square(point_i - point_j))
            # 判断是否比distances每个值都小
            for dis in distances:
                if dis < distances:
                    value = -1
                    break
            if value >= 0:
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
        revover = [sum(v)/len(v) for v in values]
        revover = sum(revover)/len(recover)
        data[i,re_col] = recover
    # 修复完毕，re_col列标准化后，返回修复后的数据集合data
    mean_re_col = np.mean(data[:,re_col], axis=0)
    std_re_col = np.std(data[:,re_col], axis=0)
    data[:,re_col] = (data[:,re_col] - mean_re_col)/std_re_col
    return data

# 自助法函数，把一个嵌套列表结构的数据按照比例分成a,b两部分----------------
def boostraping(data, rate):
    # 实现自助法选择数据，要求按照rate的比例得到数据集a
    a_numbers = []
    while len(a_numbers) < rate*len(data):
        add = random.randint(0, len(data)-1)
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
    return a_data, b_data

# -------------------------------训练组件----------------------------------
# 训练函数，根据训练数据给出模型，训练迭代---------------------------------
def train():
    w = np.random(())
    return 
# 前向传播函数，根据权重和数据计算前向传播结果----------------------------
def inference():
    return 

# -------------------------------验证组件----------------------------------
# 验证函数，根据验证数据选出最佳超参数（自适应过程）-----------------------
def validate():

# -------------------------------测试组件----------------------------------
# 导入数据，训练验证结束后进行测试-----------------------------------------
def main():
    # 训练集：验证集：测试集 = 3：1：1
    train_data, validate_data, test_data = preprocessing(0.6, 0.5)
    # 训练得到最优参数训练

    # 在最优参数基础上，自适应得到最佳超参数

    # 除了训练和测试过程中打印结果之外，最后再打印一次测试结果


__name__ == "__main__":
    main()
