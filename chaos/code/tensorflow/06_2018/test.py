import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# 用这个程序看一下mnist的数据格式，训练数据为784维向量，标签为10维向量
mnist = input_data.read_data_sets("/tmp/data", one_hot=True)
xs, ys = mnist.train.next_batch(3)
print(xs,'\n\n', ys)

