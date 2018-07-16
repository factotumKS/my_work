import numpy as np
from iris_preprocessing import iris_preprocessing

INPUT_SIZE = 4
OUTPUT_SIZE = 3
LEARNING_RATE = 0.1
TRAINING_STEP = 10000
LAMBDA = 0.001 
OPTIMIZE_METHOD = 'N'

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

# 数据标准化函数
def standarlize(data):
    data = np.transpose(np.array(data))
    for i in range(0, len(data)-1):
        row = data[i]
        data[i] = (row - np.mean(row))/np.std(row, ddof=1)
    data = np.transpose(data)
    data = [list(row) for row in data]
    for row in data:
        row[-1] = int(row[-1])
    return data

# main函数，实现训练、验证和储存功能
def main():
    # 数据预处理,逻辑回归是监督学习
    data, train_data, test_data = iris_preprocessing(0.6)
    # 数据标准化
    data = standarlize(data)
    train_data = standarlize(train_data)
    test_data = standarlize(train_data)
    # 参数定义
    w = np.random.rand(3, 4)
    b = np.random.rand(3, 1)
    beta = np.hstack((w, b))
    for k in range(1, TRAINING_STEP):
        # 取出本次的训练样本
        # 这里是如果训练集取完了就从头开始，所以取模
        x = np.array([[train_data[k%len(train_data)][i]]
            for i in range(0,4)])
        y_ = train_data[k%len(train_data)][4]
        x1 = np.row_stack((x, [1]))
        result = np.exp(beta.dot(x1)).tolist()
        raw_p = [result[i][0] for i in range(0, 3)]
        p = [raw_p[i]/sum(raw_p) for i in range(0, 3)]
        # 更新参数继续训练
        if OPTIMIZE_METHOD == 'G':
            for i in range(0,3):
                grad_p =  -np.transpose(x1)*((y_==i)-p[i]) + LAMBDA*beta[i]
                beta[i] = beta[i] - LEARNING_RATE*grad_p
        if OPTIMIZE_METHOD == "N":
            for i in range(0,3):
                grad_p =  -np.transpose(x1)*((y_==i)-p[i]) + LAMBDA*beta[i]
                Hessian = np.zeros((5,5))
                for j in range(0, 5):
                    for k in range(0, 5):
                        Hessian[j][k] = x1[j]*x1[k]*p[i]*(1-p[i])
                # Hessian = np.mat(Hessian)
                # print(Hessian)
                # Hessian_I = Hessian.I
                # Hessian_I = np.array(Hessian_I)
                # beta[i] = beta[i] - grad_p.dot(Hessian_I)
                g_Hessian_g = grad_p.dot(Hessian).dot(np.transpose(grad_p))
                if g_Hessian_g == 0:
                    beta[i]=beta[i] - LEARNING_RATE*grad_p
                else:
                    beta[i]=beta[i] - grad_p.dot(np.transpose(grad_p))/g_Hessian_g*grad_p

        # 每两百次迭代输出一次代价函数的值，测试一次网络
        if k % 100 == 0 or k < 100:
            J = -np.log(p).tolist()[y_] + 0.5*LAMBDA*np.sum(np.square(beta))
            accuracy = validate(beta, test_data)
            print("the value of cost function in %d step(s) is : %f"
                    "   ,the accuracy of classifier is %f"
                    % (k, J, accuracy))
            if accuracy >= 0.99:
                break
    print(beta)
if __name__ == '__main__':
    main()
