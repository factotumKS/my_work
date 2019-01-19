from sklearn import svm
from sklearn import model_selection as ms
import numpy as np

class Mysvm:
    def __init__(self, data):
        self.x, self.z = np.split(data, (27,), axis=0)
        self.y = np.concatenate((np.zeros((21,1)), np.ones((6,1))))
        # 设定svm的各项参数
        self.clf = svm.SVC(C=0.9, kernel='linear', gamma=20, decision_function_shape='ovr')
        
    """
    def show_accuracy(self, y_predict, y_real, name):
        result = 0
        for i in range(y_real.shape[0]):
            result += (y_predict[i] == y_real[i, 0])
        accuracy = result/y_real.shape[0]
        print(name,"正确率:",accuracy)
    """

    def train(self):
        x_train, x_test, y_train, y_test = ms.train_test_split(self.x, self.y, random_state=1, train_size=0.6)
        self.clf.fit(x_train, y_train.ravel())
        print(self.clf.score(x_train, y_train))  # 精度
        y_hat = self.clf.predict(x_train)
        # self.show_accuracy(y_hat, y_train, '训练集')
        print(self.clf.score(x_test, y_test))
        y_hat = self.clf.predict(x_test)
        # self.show_accuracy(y_hat, y_test, '测试集')

    def predict(self):
        z_hat = self.clf.predict(self.z)
        print(z_hat)

PATH = "./fenlei.txt"
DATA = np.loadtxt(PATH, dtype = float)
asvm = Mysvm(DATA)
asvm.train()
asvm.predict()