import numpy as np
import cart_decision_tree as cdt
import random as rd
from iris_preprocessing import iris_preprocessing

K = 10
CLASSES = 3

# 计算在数据集上的分类准确率
def accuracy(classifier, alpha, test_data):
    result = 0
    for point in test_data:
        right, _ = classify(classifier, alpha, point)
        result = result + right
    accu = 1.0*result / len(test_data)
    return accu
def classify(classifier, alpha, point):
    result = [0.0 for i in range(0, CLASSES)]
    for i in range(0, len(classifier)):
        _, h = cdt.classify(classifier[i], point)
        result[point[-1]] = result[point[-1]] + alpha[i]*h
    classify_result = result.index(max(result))
    return (classify_result == point[-1]), classify_result

# adaboost集成分类器的训练
def train(train_data, feature):
    # 维护一个权重向量，保存训练集中所有样本的权重
    weight = [1.0/len(train_data) for sth in train_data]
    # 维护一个分类器集合，和一个aplpha参数集合
    # 通过迭代生成K个弱分类器，这里使用cart决策树
    classifier = []
    alpha = []
    for i in range(0, K):
        gained_train_data_num = []
        # 按照权重采样,固定训练集规模来采样
        for j in range(0 , len(train_data)):
            tmp = rd.random()
            p = 0
            add_num = 0
            for m in range(0, len(weight)):
                if tmp < p:
                    add_num = m
                    break
                p = p + weight[m]
            # if add_num not in gained_train_data_num:
            gained_train_data_num.append(add_num)
        gained_train_data = [train_data[k] for k in gained_train_data_num]
        # 如果已经无法提取数据就说明数据已经几乎分类正确可以结束训练
        if len(gained_train_data) == 0:
            break
        # 训练cart学习器
        tree, error = cdt.cart_adaboost_create(gained_train_data, feature)
        # 如果由于提取的数据过少，即训练已基本完成，应该立即结束
        if error == 0:
            break
        # 虽然几乎不可能，但是可能存在一开始错误及其高的可能所以需要预防
        if error == 1:
            continue
        classifier.append(tree)
        # 根据训练结果更新权值
        alpha.append(0.5*np.log((1 - error)/error))
        for n in gained_train_data_num:
            right, _ = cdt.classify(tree, train_data[n])
            if right:
                weight[n] = weight[n] * np.exp(-alpha[i])
            else:
                weight[n] = weight[n] * np.exp(alpha[i])
        weight = [w/sum(weight) for w in weight]
    return classifier, alpha

def main():
    # 数据预处理，获得训练数据和测试数据
    data, train_data, test_data = iris_preprocessing(0.6)
    # 按照cart的连续特征加工一下
    train_data, feature = cdt.preprocessing(train_data, False)
    # adaboost训练，获得集成分类器和它们的权值,合并重复的分类器
    classifier, alpha = train(train_data, feature)
    print(len(classifier))
    alpha = [a/sum(alpha) for a in alpha]
    # 把test_data中的连续特征离散化
    test_data, _ = cdt.preprocessing(test_data, feature)
    # 用测试集计算正确率,不能忘了要对测试集的连续特征离散化
    accu = accuracy(classifier, alpha, test_data)
    print("adaboost has got %d classifier." % len(classifier))
    print("the alpha paramenter and tree structure of each classifier are:")
    for i in range(0, len(classifier)):
        print(alpha[i], classifier[i])
    print("the accuracy of adaboost with CART is: %f" % accu)
    
if __name__ == "__main__":
    main()
