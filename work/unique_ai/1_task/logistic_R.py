import numpy as np
from iris_preprocessing import iris_preprocessing
INPUT_SIZE = 4
OUTPUT_SIZE = 3
LEARNING_RATE = 0.01
TRAINING_STEP = 20000

# 验证模型的正确率
def validate(beta, test_data):
    right_classify = 0
    for n in range(0, len(test_data)):
        x = np.array([[test_data[n][i]] for i in range(0,4)])
        x1 = np.row_stack((x, [1]))
        y_ = test_data[n][4]
        y = np.transpose( 1/(1 + np.exp(-beta.dot(x1))) ).tolist()
        y = [y[0][i] for i in range(0,3)]
        right_classify = right_classify + (y_ == y.index(max(y)))
    accuracy = right_classify / len(test_data)
    return accuracy

# main函数，实现训练、验证和储存功能
def main():
    # 数据预处理,逻辑回归是监督学习
    data, train_data, test_data = iris_preprocessing(0.6)
    # 参数定义
    w = np.random.rand(3, 4)
    b = np.random.rand(3, 1)
    beta = np.hstack((w, b))
    for k in range(1, TRAINING_STEP):
        # 取出本次的训练样本
        x = np.array([[train_data[k%len(train_data)][i]] for i in range(0,4)])
        y_ = train_data[k%len(train_data)][4]
        x1 = np.row_stack((x, [1]))
        result = np.exp(beta.dot(x1)).tolist()
        raw_p = [result[i][0] for i in range(0, 3)]
        p = [raw_p[i]/sum(raw_p) for i in range(0, 3)]
        # 更新参数继续训练
        for i in range(0,3):
            grad_p =  -np.transpose(x1)*((y_==i) - p[i])
            beta[i] = beta[i] - LEARNING_RATE*grad_p
        # 每两百次迭代输出一次代价函数的值，测试一次网络，并保存参数
        if k % 100 == 0:
            J = -np.log(p).tolist()[y_]
            accuracy = validate(beta, test_data)
            print("the value of cost function in %d step(s) is : %f"
                    " ,the accuracy of classifier is %f"
                    % (k, J, accuracy))
    print(beta)
if __name__ == '__main__':
    main()
