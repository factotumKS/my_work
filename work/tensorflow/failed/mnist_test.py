#coding=utf-8
# google深度学习框架第五章MNIST数字识别问题
from tensorflow.examples.tutorials.mnist import input_data
    
# 载入MNIST数据集，如果指定地址没有就会从网上自动下载
mnist = input_data.read_data_sets("/home/mage/work/tensorflow/MNIST/",
            one_hot=True)
print("Training data size: ", mnist.train.num_examples)
print("Validating data size: ", mnist.validation.num_examples)
print("Testing data size: ", mnist.test.num_examples)
print("Example training data: ", mnist.train.images[0])
print("Example training data label: ", mnist.train.labels[0])
