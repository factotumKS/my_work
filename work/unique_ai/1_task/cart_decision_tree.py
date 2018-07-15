import numpy as np
from iris_preprocessing import iris_preprocessing, boostraping

FEATURE_UNM = 4

# 生成树之前的预处理，构建数据集D和特征集A
def preprocessing(data, existed_feature):
    # 若已用训练集生成过feature但是需要处理验证集测试集就直接导入
    if existed_feature:
        feature = existed_feature
    else:
        feature = [[] for i in range(0, FEATURE_UNM)]
    for i in range(0, len(data)):
        for j in range(0, FEATURE_UNM):
            if data[i][j] not in feature[j]:
                feature[j].append(data[i][j])
    # 把取值按大小排序
    for a in feature:
        sorted(a)
    # 连续特征处理，取中点构成集合
    T = [[(feature[i][j] + feature[i][j+1])/2
                for j in range(0, len(feature[i])-1)]
                for i in range(0, FEATURE_UNM)]
    # 更新数据集，按照分界点,转化为离散属性的取值
    for i in range(0, len(data)):
        for j in range(0, FEATURE_UNM):
            for k in range(0, len(T)):
                if data[i][j] < T[j][0]:
                    data[i][j] = feature[j][0]
                    break
                if data[i][j] >= T[j][k]:
                    data[i][j] = feature[j][k+1]
                    break
    return data, feature

# ------------------------------------------------------------------
# 计算给出的树在数据集上的表现
def accuracy(tree, data):
    accuracy = 0
    for point in data:
        classify_result, _ = classify(tree, point)
        accuracy = accuracy + classify_result
    accuracy = 1.0*accuracy/len(data)
    return accuracy
# 计算决策树精度时每个样本的判断正误
def classify(node, point):
    if type(node[0]) is str:
        return (int(node[0]) == point[-1]), int(node[0])
    a = point[node[0]]
    result = classify(node[1][a], point)
    return result

# -------------------------------------------------------------------
# 创建cart决策树的递归函数,传入validate_data用于选择最好
def cart_tree_create(data, pre_data, feature, used):
    # 准备这一层的结点
    node = []
    # 第一步，情形1：data中样本同属一类
    p = list(count_p(data))
    if max(p) == sum(p):
        # 用负数表示叶节点，其绝对值是类别编号
        node.append( str(p.index(max(p))) )
        return node
    # 第二步，情形2：data为空，或者样本的属性取值完全相同
    situation_2 = True
    for i in range(0, FEATURE_UNM):
        domain = np.transpose(data)[i]
        if max(domain) != min(domain):
            situation_2 = False
            break
    if (len(feature) == 0) or situation_2:
        p = list(count_p(data))
        node.append( str(p.index(max(p))) )
        return node
    # 第三步，从feature中选择最优划分属性，使用Gini指数作为标准
    a_ = low_gini(data, feature, used)
    # 第四步，按照最优属性a_分支
    # 第a_表示这个节点的划分属性，字典中装填各个分支
    node.append(a_)
    node.append({})
    # 为了节省空间不生成data和feature
    # 而是维护一个失效属性集合
    new_used = used[:]
    new_used.append(a_)
    # 从当前节点根据a属性分出取值ai的分支
    for ai in feature[a_]:
        data_ai = [point for point in data if point[a_] == ai]
        # 情形3:划分后的数据集为空，无法划分
        if len(data_ai) == 0:       
            continue
        else:
            next_node = cart_tree_create(data_ai, data, feature, new_used)
            node[1].update({ai:next_node})
    return node
# cart决策树生成中：计算给定数据集中各类样本的占有比例
def count_p(data):
    num_label = [0 for i in range(0, 3)]
    for num in np.transpose(data)[-1]:
        c = int(num)
        num_label[c] = num_label[c] + 1
    p = np.array([1.0*num/sum(num_label) for num in num_label])
    return p
# cart决策树生成中：根据属性集合找到最优属性的函数
def low_gini(data, feature, used):
    gini_index = []
    # 分析每一个可用属性
    for a in range(0, FEATURE_UNM):
        if a in used:
            # 基尼指数不会超过1,借此忽略已用属性
            gini_index.append(1)
            continue
        gini_index_a = 0
        # 计算属性a在取值为ai的Gini index求和项
        for ai in feature[a]:
            count = [ai == data[i][a] for i in range(0, len(data))]
            weight = sum(count)/len(count)
            data_ai = [point for point in data if point[a] == ai]
            # 为0则gini index求和项权值为零，直接跳过
            if len(data_ai) == 0:
                continue
            p_ai = count_p(data_ai)
            gini_ai = 1 - p_ai.dot(p_ai)
            gini_index_a = gini_index_a + weight*gini_ai
        gini_index.append(gini_index_a)
    # 选出Gini index值最小的属性作为最优属性
    a_ = gini_index.index(min(gini_index)) 
    return a_

# ------------------------------------------------------------
# adaboost：cart作为一个弱分类器被使用，写一个训练函数
def cart_adaboost_create(data, feature):
    # 递归生成CART决策树
    tree = cart_tree_create(data, [], feature, [])
    # 后剪枝

    # 测试
    accu = accuracy(tree, data)
    return tree, 1 - accu

# ------------------------------------------------------------
def main():
    # 训练集：验证集：测试集 = 3：1：1
    _, train_data, rest_data = iris_preprocessing(0.6)
    validate_data, test_data = boostraping(rest_data, 0.5)
    # 数据全部准备就绪
    train_data, feature = preprocessing(train_data, False)
    validate_data, _ = preprocessing(validate_data, feature)
    test_data, _ = preprocessing(test_data, feature)
    # 递归生成CART决策树
    tree = cart_tree_create(train_data, [], feature, [])
    # 后剪枝

    # 测试
    train_accuracy = accuracy(tree, train_data)
    test_accuracy = accuracy(tree, test_data)
    print("the accuracy of current CART Decision Tree on training is: %f"
            % train_accuracy)
    print("the accuracy of current CART Decision Tree on  testing is: %f"
            % test_accuracy)

if __name__ == '__main__':
    main()
