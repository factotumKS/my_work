# CIFAR-10数据集训练
import sys
sys.path.append("~/TensorFlow/CIFAR10/models/tutorials/image/cifar10")
# 下载和读取CIFAR-10的类
import cifar10,cifar10_input
import tensorflow as tf
import numpy as np
import time

# 训练轮数
max_steps = 3000
batch_size = 128
# 下载DIFAR-10数据的默认路径
data_dir = '/tmp/cifar10_data/cifar-10-batches-bin'

# L1正则会制造稀疏的特征，大部分无用特征的权重会被置0
# L2正则会让特征不过大，使得特征的权重比较均匀

# 使用正太分布初始化权重并添加L2正则化,使用w1控制L2损失的大小
def variable_with_weight_loss(shape, stddev, w1):
    # 从截断的(2个标准差以内)正态分布中输出随机值
    var = tf.Variable(tf.truncated_normal(shape, stddev=stddev))
    if w1 is not None:
        # l2_loss(var)*w1
        weight_loss = tf.multiply(tf.nn.l2_loss(var), w1, name='weight_loss')
        # 使用默认图
        tf.add_to_collection('losses', weight_loss)
    return var

# 从Alex的网站下载并解压到默认位置
cifar10.maybe_download_and_extract()
# 使用Reader操作构造CIFAR训练需要的数据(特征及其对应的label)
# 并对数据进行了数据增强(水平翻转/随机对比度亮度/随机裁剪)以及数据的标准化
images_train, labels_train = cifar10_input.distorted_inputs(data_dir=data_dir,batch_size=batch_size)
# 使用Reader操作构建CIFAR评估的输入(裁剪图像中间24*24大小的块并进行数据标准化)
images_test, labels_test =cifar10_input.inputs(eval_data=True, data_dir=data_dir, batch_size=batch_size)

# 输入图像占位符(24*24 3通道)
image_holder = tf.placeholder(tf.float32, [batch_size, 24, 24, 3])
# 输入标签占位符
label_holder = tf.placeholder(tf.int32, [batch_size])

# 卷积层1
# 64个5*5的卷积核3通道,不对第一个卷积层的权重加L2正则
weight1 = variable_with_weight_loss(shape=[5, 5, 3, 64], stddev=5e-2, w1=0.0)
# 卷积步长为1模式为SAME
kernel1 = tf.nn.conv2d(image_holder, weight1, [1, 1, 1, 1], padding='SAME')
# bias为0
bias1 = tf.Variable(tf.constant(0.0, shape=[64]))
# Adds bias to value
conv1 = tf.nn.relu(tf.nn.bias_add(kernel1, bias1))
# 最大池化　大小3*3步长2*2
pool1 = tf.nn.max_pool(conv1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')
# 使用LRN对结果进行处理-Local Response Normalization-本地响应标准化
# 增强大的抑制小的,增强泛化能力
norm1 = tf.nn.lrn(pool1, 4, bias=1.0, alpha=0.001/9.0, beta=0.75)

# 卷积层2
# 64个5*5的卷积核64通道,不加L2正则
weight2 = variable_with_weight_loss(shape=[5, 5, 64, 64], stddev=5e-2, w1=0.0)
# 卷积步长为1模式为SAME
kernel2 = tf.nn.conv2d(norm1, weight2, [1, 1, 1, 1], padding='SAME')
# bias为0.1
bias2 = tf.Variable(tf.constant(0.1, shape=[64]))
# Adds bias to value
conv2 = tf.nn.relu(tf.nn.bias_add(kernel2, bias2))
# LRN-本地响应标准化
norm2 = tf.nn.lrn(conv2, 4, bias=1.0, alpha=0.001/0.9, beta=0.75)
# 最大池化　大小3*3步长2*2
pool2 = tf.nn.max_pool(norm2, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')

# 全连接层
# 将样本变成一维向量
reshape = tf.reshape(pool2, [batch_size, -1])
# 数据扁平化后的长度
dim = reshape.get_shape()[1].value
# weight初始化
weight3 = variable_with_weight_loss(shape=[dim, 384], stddev=0.04, w1=0.004)
# bias初始化
bias3 = tf.Variable(tf.constant(0.1, shape=[384]))
local3 = tf.nn.relu(tf.matmul(reshape, weight3) + bias3)

# 隐含节点数降为192
weight4 = variable_with_weight_loss(shape=[384, 192], stddev=0.04, w1=0.004)
bias4 = tf.Variable(tf.constant(0.1, shape=[192]))
local4 = tf.nn.relu(tf.matmul(local3, weight4) + bias4)

# 最终输出10分类,正太分布标准差设为上一隐含层节点数的倒数,不计入L2正则
weight5 = variable_with_weight_loss(shape=[192, 10], stddev=1/192.0, w1=0.0)
bias5 = tf.Variable(tf.constant(0.0, shape=[10]))
logits = tf.add(tf.matmul(local4, weight5), bias5)


# 计算CNN的loss
def loss(logits, labels):
    labels = tf.cast(labels, tf.int64)
    # 计算logits和labels之间的稀疏softmax交叉熵
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
        logits=logits, labels=labels, name='cross_entropy_per_example')
    # 计算cross_entropy均值
    cross_entropy_mean = tf.reduce_mean(cross_entropy, name='cross_entropy')
    # 将cross_entropy的loss添加到整体的loss里
    tf.add_to_collection('losses', cross_entropy_mean)
    # 将整体losses的collection中的全部loss求和
    return tf.add_n(tf.get_collection('losses'), name='total_loss')


# 将logits节点label_holder和传入loss函数获得最终的loss
loss = loss(logits, label_holder)
# 优化器选择Adam,学习率选1e-3
train_op = tf.train.AdamOptimizer(1e-3).minimize(loss)
# 求top k的准确率(默认top1即输出分数最高的一类)
top_k_op = tf.nn.in_top_k(logits, label_holder, 1)


# 创建默认的session()
sess = tf.InteractiveSession()
# 初始化全部的模型参数
tf.global_variables_initializer().run()

# 启动图片数据增强的线程队列
tf.train.start_queue_runners()

for step in range(max_steps):
    start_time = time.time()
    # 使用sess的run方法执行images_train和labels_train的计算
    image_batch, label_batch = sess.run([images_train, labels_train])
    #
    _, loss_value = sess.run([train_op, loss],
              feed_dict={image_holder: image_batch, label_holder:label_batch})
    # 记录每个step的时间
    duration = time.time() - start_time
    if step % 10 == 0:
        # 每秒训练的样本数量
        examples_per_sec = batch_size / duration
        # 训练每个batch的时间
        sec_per_batch = float(duration)
        format_str = ('step %d, lass=%.2f (%.1f examples/sec; %.3f sec/batch)')
        print format_str % (step, loss_value, examples_per_sec, sec_per_batch)


# 测试集样本数量
num_examples = 10000
import math
# 总共多少个batch
num_inter = int(math.ceil(num_examples / batch_size))
true_count = 0
total_sample_count = num_inter * batch_size
step = 0
while step < num_inter:
    # 使用sess的run方法获取images_test和labels_test的batch
    image_batch, label_batch = sess.run([images_test, labels_test])
    # 预测正确的样本数量
    predictions = sess.run([top_k_op], feed_dict={image_holder: image_batch,
                            label_holder: label_batch})
    # 汇总预测正确的结果
    true_count += np.sum(predictions)
    step += 1

# 准确率评测结果
prediction = true_count / total_sample_count
print 'precision @ 1 = %.3f' % prediction