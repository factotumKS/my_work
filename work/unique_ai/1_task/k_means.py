import numpy as np
import random
from iris_preprocessing import iris_preprocessing

K = 3
DEMAND = 0.000001

# 实现x,与y在Data的分布中，马氏距离的计算
def maha(x, y, data):
    data_T = np.transpose(data)
    sigma = np.mat(np.cov(data_T))
    sigma_I = np.array(sigma.I)
    maha_dis = (x-y).dot(sigma_I).dot(np.transpose(x-y))
    return maha_dis

# 实现K-means++算法
def main():
    # 预处理数据，使用无教师（非监督）学习
    raw_data = iris_preprocessing(False)
    label = [point.pop() for point in raw_data]
    data = np.array(raw_data)
    # 使用K-means++选出起始中心seed
    seed_number = [random.randint(0, data.shape[0]),]
    seed = np.array([data[seed_number[0]]])
    for k in range(1,K):
        # 选出距离seed最远的点
        new_seed_number = 0
        new_seed = np.array(data[new_seed_number])
        longest_distance = 0
        for i in range(0, data.shape[0]):
            # 与最近seed的距离
            distance_to_seed = [maha(data[i],seed[j],data)
                                for j in range(0,seed.shape[0])]
            distance = min(distance_to_seed)
            # 更新最长距离的点
            if distance > longest_distance:
                new_seed_number = i
                new_seed = np.array(data[new_seed_number])
                longest_distance = distance
        # 已经选出距离最大点，该点不可能是已存seed，直接加入新的seed
        seed = np.row_stack((seed, new_seed))
    turn = 0
    while True:
        # 计算训练次数
        turn = turn + 1
        # 按照最近聚类中心更新分类
        classify_result = [[] for i in range(0, K)]
        for i in range(0, len(data)):
            distance_to_seed = [maha(data[i],seed[j],data)
                                for j in range(0, K)]
            c = distance_to_seed.index(min(distance_to_seed))
            classify_result[c].append(i)
        # 计算新的聚类中心
        center = np.zeros((K,4))
        for i in range(0 , K):
            all_point = np.zeros((1, 4))
            for j in classify_result[i]:
                all_point  = all_point + data[j]
            center[i] = all_point / len(classify_result[i])
        # 收敛了就及时跳出，否则更新聚类中心继续循环
        if sum([maha(seed[i],center[i],data) for i in range(0,K)]) > DEMAND:
            seed = center
        else:
            break
    print("after %d turn(s)" % turn)
    print("the data has been classified into %d classes" % K)
    accuracy = np.zeros((3, 3))
    for i in range(0, K):
        for num in classify_result[i]:
            k = label[num]
            accuracy[i][k] = accuracy[i][k] + 1
        print("class %d has %d member(s), %d %d %d for each kind"
            % (i+1, len(classify_result[i]),
                accuracy[i][0], accuracy[i][1], accuracy[i][2]))

if __name__ == '__main__':
    main()
