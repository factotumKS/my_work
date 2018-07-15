#coding=utf-8
# 使用参考书实战google学习框架第三章的前向传播算法实验P55
import tensorflow as tf

w1 = tf.Variable(tf.random_normal([2,3], stddev=1, seed=1))
w2 = tf.Variable(tf.random_normal([3,1], stddev=1, seed=1))

x = tf.constant([[0.7, 0.9]])

a = tf.matmul(x,w1)
y = tf.matmul(a,w2)

with  tf.Session() as sess:
# 需要使用初始化
    sess.run(w1.initializer)
    sess.run(w2.initializer)
    print("\n", sess.run(y))

