import numpy as np
import random as rd
import cart_decision_tree as cdt
from iris_preprocessing import iris_preprocessing

TREE_NUM = 4
FEATURE_NUM = 4
RANDOM_FEATURE_NUM = 2

# 检验森林的正确率
def accuracy(forest, test_data):
    accu_num = 0
    for point in test_data:
        classify_result = [0 for i in range(0, FEATURE_NUM)]
        for tree in forest:
            _, h = cdt.classify(tree, point)
            classify_result[h] = classify_result[h] + 1
        final_result = classify_result.index(max(classify_result))
        accu_num = accu_num + (final_result == point[-1])
    accu = accu_num/len(test_data)
    return accu

# 构建一颗用于随机森林的cart树
def rf_cart_root_create(data, feature):
    # 准备根节点
    node = []
    # 跳过情形1、2的分析，根节点的数据集必然非空且不属同类
    # 需要FOREST_NUM个数的随机属性，所以构造互补集合去除其他属性
    abandon = []
    while True:
        tmp = rd.randint(0, FEATURE_NUM-1)
        if tmp not in abandon:
            abandon.append(tmp)
        if len(abandon) == RANDOM_FEATURE_NUM:
            break
    a_ = cdt.low_gini(data, feature, abandon)
    # 用随机最优属性，构建根节点
    node.append(a_)
    node.append({})
    # 开始分支
    for ai in feature[a_]:
        data_ai = [point for point in data if point[a_] == ai]
        # 需要考虑情况3
        if len(data_ai) == 0:
            continue
        next_node = cdt.cart_tree_create(data_ai, data, feature, [a_])
        node[1].update({ai:next_node})
    return node

# 通过训练得到一片随机森林
def train(train_data, feature):
    forest = []
    for i in range(0, TREE_NUM):
        tree = rf_cart_root_create(train_data, feature)
        forest.append(tree)
    return forest


def main():
    # 数据导入预处理
    _, train_data, test_data = iris_preprocessing(0.6)
    # 为了决策树准备的数据进一步处理
    train_data, feature = cdt.preprocessing(train_data, False)
    test_data, _ = cdt.preprocessing(test_data, feature)
    # 生成随机森林
    forest = train(train_data, feature)
    # 计算随机森林在测试集上的表现能力
    accu = accuracy(forest, test_data)
    print("there are %d tree in the random forest:" % TREE_NUM)
    for tree in forest:
        print(tree)
    print("the accuracy of current random forest is: %f" % accu)

if __name__ == "__main__":
    main()
