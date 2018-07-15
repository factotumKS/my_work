#coding=utf-8
# 第五章手写数字识别问题
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# MNIST数据集相关的数据
INPUT_NODE = 784    # 输入层节点数，即图片像素
OUTPUT_NODE = 10    # 输出层节点数，有0-9十种数字

# 配置神经网络的参数
LAYER1_NODE = 500   # 隐藏层节点数
BATCH_SIZE = 100    # 一个训练batch种的数量
LEARNING_RATE_BASE = 0.8        # 学习率
LEARNING_RATE_DECAY = 0.99      # 学习率衰减率
REGULARIZATION_RATE = 0.0001    # 正则化项在损失函数中的系数lambda
TRAINING_STEPs = 30000          # 训练轮数
MOVING_AVERAGE_DECAY = 0.99     # 滑动平均衰减数

# 辅助函数inference给定神经网络的输出和参数，计算神经网络的前向传播结果
# 此程序中定义的是使用ReLU的三层全链接神经网络
def inference(input_tensor, avg_class, weights1, biasses1,
        weights2, biasses2):
    # 当没有提供滑动平均类时，直接使用参数当前的权值
    if avg_class == None:
        # 计算隐藏层的前向传播结果，这里使用了ReLU激活函数
        layer1 = tf.nn.relu(tf.matmul(input_tensor, weights1) + biasses1)

        # 计算损失函数时会一并计算softmax函数
        # 所以这里不需要加入激活函数，而且不加也没问题
        # 预测时比较的是相对大小，所以没有softmax层也不会造成影响
        return tf.matmul(layer1, weights2) + biasses2

    else:
        # 使用avg_class.average来得到滑动平均值
        # 然后计算相应的前向神经网络传播结果
        layer1 = tf.nn.relu(
            tf.matmul(input_tensor, avg_class.average(weights1)) +
            avg_class.average(biasses1))
        return tf.matmul(layer1, avg_class.average(weights2) +
            avg_class.average(biasses2))

# 训练模型的过程
def train(mnist):
    x = tf.placeholder(tf.float32, [None, INPUT_NODE], name="x-input")
    y_ = tf.placeholder(tf.float32, [None, OUTPUT_NODE], name="y-input")

    # 生成隐藏层的参数
    weights1 = tf.Variable(
        tf.truncated_normal([INPUT_NODE, LAYER1_NODE], stddev=0.1))
    biasses1 = tf.Variable(tf.constant(0.1, shape=[LAYER1_NODE]))
    # 生成输出层的参数
    weights2 = tf.Variable(
        tf.truncated_normal([LAYER1_NODE, OUTPUT_NODE], stddev=0.1))
    biasses2 = tf.Variable(tf.constant(0.1, shape=[OUTPUT_NODE]))

    # 计算在当前参数下神经网络前向传播的结果，
    # 这里不使用滑动平均值
    y = inference(x, None, weights1, biasses1, weights2, biasses2)

    # 定义存储训练轮数的变量
    # 这个变量不需要训练，设置为False
    global_step = tf.Variable(0, trainable=False)

    # 初始化滑动平均类的实例，给定滑动平均衰减数和训练轮数的变量
    # 准备传入reference
    variable_averages = tf.train.ExponentialMovingAverage(
        MOVING_AVERAGE_DECAY, global_step)

    # 在所有神经网络参数变量上使用滑动平均
    # 如训练轮数这种辅助变量应该在声明时设定不可训练
    # tf.trainable_variables返回图上
    # GraphKeys_TRAINABLE_VARIABLES中元素
    variables_averages_op = variable_averages.apply(
        tf.trainable_variables())

    # 计算使用滑动平均值的前向传播结果
    average_y = inference(
        x, variable_averages, weights1, biasses1, weights2, biasses2)

    # 损失函数为交叉熵，使用那个结合了softmax的长函数
    # 第一个参数是刚出炉没有softmax的，第二个参数是正确答案
    # 这里是手写数字识别，所以正确答案对每个样本时一个0-9的数字
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
        logits=y, labels=tf.argmax(y_, 1))
    # 计算batch中所有样例的平均值
    cross_entropy_mean = tf.reduce_mean(cross_entropy)

    # 获得方法：计算定制的L2正则化损失函数，需要参数是lambda
    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
    # 计算模型的正则化损失。一般只计算神经网络边上权重的损失，不使用偏置项
    regularization = regularizer(weights1) + regularizer(weights2)
    # 总损失等于交叉熵损失和正则化损失的和
    loss = cross_entropy_mean + regularization
    # 设置指数衰减的学习率
    learning_rate = tf.train.exponential_decay(
        LEARNING_RATE_BASE,     # 基础学习率，随着迭代递减
        global_step,            # 当前迭代的轮数
        mnist.train.num_examples / BATCH_SIZE,  # 所有训练需要的迭代次数
        LEARNING_RATE_DECAY)    # 学习率衰减速度

    # 使用巴拉巴拉巴拉优化算法优化损失函数，包含交叉熵和正则化两项损失
    train_step = tf.train.GradientDescentOptimizer(learning_rate)\
        .minimize(loss, global_step=global_step)
    # 训练中，每次迭代需要反向传播更新参数，也要更新滑动平均值
    # 下面和train_op = tf.group(train_step, variables_averages_op)等价
    with tf.control_dependencies([train_step, variables_averages_op]):
        train_op = tf.no_op(name="train")

    # 检验是否正确，表示为0-1的一位向量
    # argmax参数1表示返回每行最大元素的下标，也就是预测数字
    correct_prediction = tf.equal(tf.argmax(average_y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # 初始化会话开始训练过程
        # argmax返回的是最大元素的下标
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        # 准备验证数据，通过验证来大概判断停止条件和评判结果
        validate_feed = {x: mnist.validation.images,
                        y_: mnist.validation.labels}

        # 准备测试数据，训练时不可见，作为模型优劣的最后评判标准
        test_feed = {x: mnist.test.images, y_: mnist.test.labels}

        # 迭代训练神经网络
        for i in range(TRAINING_STEPs):
            # 每1000轮输出一次在验证数据集上的测试结果（反应正确率）
            if i % 1000 == 0:
            # mnist的batch足够小，不需要额外划分
                validate_acc = sess.run(accuracy, feed_dict=validate_feed)
                print("After %d training step(s), Validation accuracy "
                        "using average model is %g " % (i, validate_acc))

            # 产生这一轮使用的一个batch训练数据，并运行训练过程
            xs, ys = mnist.train.next_batch(BATCH_SIZE)
            sess.run(train_op, feed_dict={x: xs, y_:ys})

        # 训练结束之后，检查最终正确率
        test_acc = sess.run(accuracy, feed_dict=test_feed)
        print("After %d training step(s), test accuracy using average "
                "model is %g" % (TRAINING_STEPs, test_acc))

# 主程序入口
def main(argv=None):
    # 声明处理MNIST数据集的类，这个类在初始化时自动下载数据
    mnist = input_data.read_data_sets("/tmp/data", one_hot=True)
    train(mnist)

# tensorflow提供的主程序入口，tf.app.run会调用上面定义的main函数
if __name__ == '__main__':
    tf.app.run()
