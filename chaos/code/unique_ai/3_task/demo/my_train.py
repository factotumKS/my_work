import tensorflow as tf
from data import get_data_set
import my_inference
import os

BATCH_SIZE = 100
LEARNING_RATE_BASE = 0.8
LEARNING_RATE_DECAY = 0.99
REGULARIZATION_RATE = 0.0001
TRAINING_STEPS = 30000
MOVING_AVERAGE_DECAY = 0.99
MODEL_SAVE_PATH="./CIFAR10_model/"
MODEL_NAME="cifar10_model"


def train():
    # 获得总训练数据
    train_x, train_y, train_l = get_data_set(cifar = 10)
    
    # 占位准备
    x = tf.placeholder(tf.float32, [None, inference.INPUT_NODE], name='x-input')
    y_ = tf.placeholder(tf.float32, [None, inference.OUTPUT_NODE], name='y-input')
    keep_prob = tf.placeholder(tf.float32)
    x_imgs = tf.reshape(x,[-1,32,32,3])
    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
    # 这里直接调用之前的反向传播函数
    y = my_inference.inference(x_imgs, True, regularizer)
    global_step = tf.Variable(0, trainable=False)


    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    variables_averages_op = variable_averages.apply(tf.trainable_variables())
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(y, tf.argmax(y_, 1))
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))
    learning_rate = tf.train.exponential_decay(
        LEARNING_RATE_BASE,
        global_step,
        len(train_x) / BATCH_SIZE, LEARNING_RATE_DECAY,
        staircase=True)
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
    with tf.control_dependencies([train_step, variables_averages_op]):
        train_op = tf.no_op(name='train')


    saver = tf.train.Saver()
    with tf.Session() as sess:
        tf.global_variables_initializer().run()

        for i in range(TRAINING_STEPS):
            # 单次迭代的数据传入
            randidx = np.random.randint(len(train_x), size=BATCH_SIZE)
            xs = train_x[randidx]
            ys = train_y[randidx]
            _, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x: xs, y_: ys})
            # 每隔1000次训练保存一下
            if i % 1000 == 0:
                print("After %d training step(s), loss on training batch is %g." % (step, loss_value))
                saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)


def main(argv=None):
    train()

if __name__ == '__main__':
    tf.app.run()


