#coding=utf-8
import time
import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
# 加载计算图模块和运行模块
import CNN_mnist_inference
import CNN_mnist_train


# 每十秒加载一次新模型，并在测试数据集上测试最新模型
EVAL_INTERVAL_SECS = 10

def evaluate(mnist):
    with tf.Graph().as_default() as g:
        # 定义输入输出格式
        x = tf.placeholder(tf.float32,
            [100, CNN_mnist_inference.INPUT_NODE], name='x-input')
        y_ = tf.placeholder(tf.float32,
            [100, CNN_mnist_inference.OUTPUT_NODE], name='y-input')
        valiable_feed = {x: mnist.validation.images,
                        y_: mnist.validation.labels}
        reshaped_x =np.reshape(x,
            (100,
            CNN_mnist_inference.IMAGE_SIZE,
            CNN_mnist_inference.IMAGE_SIZE,
            CNN_mnist_inference.NUM_CHANNELS))

        # 调用自定义封装函数计算FP结果
        # 测试时不关心正则化，不需要dropout
        y = CNN_mnist_inference.inference(x, False, None)

        # 使用FP结果计算正确率
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        # 变量重命名，加载模型
        variable_averages = tf.train.ExponentialMovingAverage(
            CNN_mnist_train.MOVING_AVERAGE_DECAY)
        variables_to_restore = variable_averages.variables_to_restore()
        saver = tf.train.Saver(variables_to_restore)

        # 每隔EVAL_INTERVAL_SECS秒调用一次计算正确率的过程
        while True:
            with tf.Session() as sess:
                # 通过checkpoint自动找到文件名
                ckpt = tf.train.get_checkpoint_state(
                    CNN_mnist_train.MODEL_SAVE_PATH)
                if ckpt and ckpt.model_checkpoint_path:
                    # 加载模型
                    saver.restore(sess, ckpt.model_checkpoint_path)
                    # 通过文件名得到保存时的迭代轮数
                    global_step = ckpt.model_checkpoint_path\
                        .split('/')[-1].split('-')[-1]
                    accuracy_rate = sess.run(accuracy,
                        feed_dict=valiable_feed)
                    print ("After %s training step(s), validation "
                        "accuracy = %g" % (global_step, accuracy_rate))
                else:
                    print('No checkpoint file found')
                    return None
            time.sleep(EVAL_INTERVAL_SECS)

def main(argv=None):
    mnist = input_data.read_data_sets("/tmp/data", one_hot=True)
    evaluate(mnist)

if __name__ == '__main__':
    tf.app.run()



