import random

def boostraping(data, rate):
    # 实现自助法选择数据，要求生成含有60%的数据集，这里只保存数据的下标
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
    # 剩下的数据用于测试
    b_numbers = [i for i in range(0, len(data)) if i not in a_numbers]
    b_data = [data[i] for i in b_numbers]
    return a_data, b_data
   
def iris_preprocessing(rate):
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
    # 如果是监督学习，就需要训练集和验证集
    if rate:
        train_data, test_data = boostraping(data, rate)
        return data, train_data, test_data
    else:
        return data

if __name__ == '__main__':
    iris_preprocessing()
