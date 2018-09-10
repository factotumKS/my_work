# -*- coding: utf-8 -*-
import tensorflow as tf

INPUT_NODE = 784
OUTPUT_NODE = 10
IMAGE_SIZE = 28
NUM_CHANNELS = 1
NUM_LABELS = 10

# 第一层卷积网络的尺度和深度
CONV1_DEEP = 32
CONV1_SIZE = 5
# 第二层卷积网络的尺度和深度
CONV2_DEEP = 64
CONV2_SIZE = 5
# 全链接层的节点个数
FC_SIZE = 512

# 定义卷积神经网络的前向传播过程。新参数train用于区分训练和测试
def inference(input_tensor, train, regularizer):
    # 声明第一卷积层的变量并指定FP过程
    # 使用不同命名空间来隔离不同层的变量
    # 输入为28x28x1，输出为28x28x32
    with tf.variable_scope('layer1-conv1'):
        conv1_weights = tf.get_variable(
            "weight", [CONV1_SIZE, CONV1_SIZE, NUM_CHANNELS, CONV1_DEEP],
            initializer = tf.truncated_normal_initializer(stddev=0.1))
        conv1_biases = tf.get_variable(
            "bias", [CONV1_DEEP], initializer=tf.constant_initializer(0.0))
        # 使用变长5,深度32的过滤器，过滤器移动的步长为1,使用全0填充
        conv1 = tf.nn.conv2d(
            input_tensor,conv1_weights,strides=[1, 1, 1, 1],padding='SAME')
        relu1 = tf.nn.relu(tf.nn.bias_add(conv1, conv1_biases))

    # 第二层池化层的FP过程。使用最大池化层，过滤器边长为2
    # 全0填充且移动步长为2。这一层是上层输出28x28x32，输出为14x14x32
    with tf.variable_scope('layer2-pool1'):
        pool1 = tf.nn.max_pool(
            relu1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    # 第三层卷积层的FP过程。输入为14x14x32，输出为14x14x64的矩阵
    with tf.variable_scope('layer3-conv2'):
        conv2_weights = tf.get_variable(
            "weight", [CONV2_SIZE, CONV2_SIZE, CONV1_DEEP, CONV2_DEEP],
            initializer = tf.truncated_normal_initializer(stddev=0.1))
        conv2_biases = tf.get_variable(
            "bias", [CONV2_DEEP], initializer=tf.constant_initializer(0.0))
        # 使用变长5,深度64的过滤器，移动步长为1,使用全0填充
        conv2 = tf.nn.conv2d(
            pool1,conv2_weights,strides=[1, 1, 1, 1],padding='SAME')
        relu2 = tf.nn.relu(tf.nn.bias_add(conv2, conv2_biases))
    
    # 第四层池化层的FP过程。输入14x14x64，输出7x7x64
    with tf.variable_scope('layer4-pool2'):
        pool2 = tf.nn.max_pool(
            relu2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    # 第五层全链接层
    # 全链接层只接受向量，需要把7x7x64拉直，pool2.get_shape函数自动输出维度
    pool_shape = pool2.get_shape().as_list()
    # 计算拉直之后的向量长度，矩阵长宽和深度的乘积
    nodes = pool_shape[1] * pool_shape[2] * pool_shape[3]
    # tf.reshape将第四层输出变成batch向量
    reshaped = tf.reshape(pool2, [pool_shape[0], nodes])
    # 第五层全链接层的FP过程。输入为一个batch向量
    # 输入是3136向量，输出是512向量
    # dropout能将部分节点输出变更为0,避免过拟合问题
    with tf.variable_scope('layer5-fc1'):
        fc1_weights = tf.get_variable(
            "weight", [nodes, FC_SIZE],
            initializer = tf.truncated_normal_initializer(stddev=0.1))
        # 只有全链接层需要加入正则化项
        if regularizer != None:
            tf.add_to_collection('losses', regularizer(fc1_weights))
        fc1_biases = tf.get_variable(
            "bias", [FC_SIZE], initializer=tf.constant_initializer(0.1))
        fc1 = tf.nn.relu(tf.matmul(reshaped, fc1_weights) + fc1_biases)
        if train: fc1 = tf.nn.dropout(fc1, 0.5)

    # 第六层全链接层的FP过程。这层输入为一组512向量，输出为一组10向量
    # 和最后的softmax层形成最后输出
    with tf.variable_scope('layer6-fc2'):
        fc2_weights = tf.get_variable(
            "weight", [FC_SIZE, NUM_LABELS],
            initializer = tf.truncated_normal_initializer(stddev=0.1))
        if regularizer != None:
            tf.add_to_collection('losses', regularizer(fc2_weights))
        fc2_biases = tf.get_variable(
            "bias", [NUM_LABELS], initializer=tf.constant_initializer(0.1))
        logit = tf.matmul(fc1, fc2_weights) + fc2_biases

    return logit
