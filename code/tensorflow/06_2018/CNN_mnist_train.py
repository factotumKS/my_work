# -*- coding: utf-8 -*-
import os
import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
# 加载reference.py中定义的常量和前向传播的函数
import CNN_mnist_inference

# 配置神经网络的参数
BATH_SIZE = 100
LEARNING_RATE_DECAY = 0.99
LEARNING_RATE_BASE = 0.8
REGULARIZATION_RATE = 0.0001
TRAINING_STEPS = 30000
MOVING_AVERAGE_DECAY = 0.99
# 模型保存的路径和文件名
MODEL_SAVE_PATH = "/home/mage/work/tensorflow/save"
MODEL_NAME = "CNN_mnist.ckpt"

def train(mnist):
    # 定义输入输出
    # 这里修改了输入格式，将一组784维向量修改为一组28x28x1矩阵
    x = tf.placeholder(
        tf.float32, [BATH_SIZE,
                    CNN_mnist_inference.IMAGE_SIZE,
                    CNN_mnist_inference.IMAGE_SIZE,
                    CNN_mnist_inference.NUM_CHANNELS], name='x-input')
    y_ = tf.placeholder(
        tf.int32, [BATH_SIZE,CNN_mnist_inference.OUTPUT_NODE], 
        name='y-input')
    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
    # 直接使用mnist_inference.py中定义的FP过程
    # y是一组10向量
    y = CNN_mnist_inference.inference(x, True, regularizer)
    global_step = tf.Variable(0, trainable=False)

    # 定义损失函数、学习率、滑动平均值
    variable_averages = tf.train.ExponentialMovingAverage(
        MOVING_AVERAGE_DECAY, global_step)
    variable_averages_op = variable_averages.apply(
        tf.trainable_variables())
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
        logits=y, labels=tf.argmax(y_,1))
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))
    learning_rate = tf.train.exponential_decay(
        LEARNING_RATE_BASE,
        global_step,
        mnist.train.num_examples / BATH_SIZE,
        LEARNING_RATE_DECAY)
    train_step = tf.train.GradientDescentOptimizer(learning_rate)\
        .minimize(loss, global_step=global_step)
    with tf.control_dependencies([train_step, variable_averages_op]):
        train_op = tf.no_op(name='train')
    
    # 初始化tensorflow持久类
    saver = tf.train.Saver()
    with tf.Session() as sess:
        tf.initialize_all_variables().run()
        # 在训练过程中不测时模型表现，验证测试有独立程序完成
        for i in range(TRAINING_STEPS):
            xs, ys = mnist.train.next_batch(BATH_SIZE)
            reshaped_xs = np.reshape(xs,
                (BATH_SIZE,
                CNN_mnist_inference.IMAGE_SIZE,
                CNN_mnist_inference.IMAGE_SIZE,
                CNN_mnist_inference.NUM_CHANNELS))
            _, loss_value, step = sess.run([train_op, loss, global_step],
                feed_dict={x: reshaped_xs, y_: ys})
            # 每1000轮保存一次数据
            if i % 1000 == 0:
                # 输出当前训练情况
                print("After %d training step(s), loss on training batch"
                    " is %g." % (step, loss_value))
                # 保存模型，文件名尾加上训练次数
                saver.save(
                    sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME),
                    global_step=global_step)
    
def main(argv=None):
    mnist = input_data.read_data_sets("/tmp/data", one_hot=True)
    train(mnist)

if __name__ == '__main__':
    tf.app.run()
