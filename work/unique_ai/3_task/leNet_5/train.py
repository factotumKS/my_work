import tensorflow as tf
from tensorflow.models.tutorials.image.cifar10 import cifar10_input
import inference
import os

BATCH_SIZE = 100
LEARNING_RATE_BASE = 0.8
LEARNING_RATE_DECAY = 0.99
REGULARIZATION_RATE = 0.0001
TRAINING_STEPS = 30000
MOVING_AVERAGE_DECAY = 0.99
MODEL_SAVE_PATH="./CIFAR10_model/"
MODEL_NAME="cifar10_model"


def train(cifar10):
    images_train, labels_train = cifar10_input.distortd_inputs(data_dir = "/tmp/",
            batch_size = BATCH_SIZE)
    images_test, labels_test = cifar10_input.distortd_inputs(eval_data = True,
            data_dir = "/tmp/", batch_size = BATCH_SIZE)

    x = tf.placeholder(tf.float32, [None, inference.INPUT_NODE], name='x-input')
    y_ = tf.placeholder(tf.float32, [None, inference.OUTPUT_NODE], name='y-input')
    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
    # 这里直接调用之前的反向传播函数
    y = inference.inference(x, True, regularizer)
    global_step = tf.Variable(0, trainable=False)


    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    variables_averages_op = variable_averages.apply(tf.trainable_variables())
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(y, tf.argmax(y_, 1))
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))
    learning_rate = tf.train.exponential_decay(
        LEARNING_RATE_BASE,
        global_step,
        cifar10.train.num_examples / BATCH_SIZE, LEARNING_RATE_DECAY,
        staircase=True)
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
    with tf.control_dependencies([train_step, variables_averages_op]):
        train_op = tf.no_op(name='train')


    saver = tf.train.Saver()
    with tf.Session() as sess:
        tf.global_variables_initializer().run()

        for i in range(TRAINING_STEPS):
            xs, ys = cifar10.train.next_batch(BATCH_SIZE)
            _, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x: xs, y_: ys})
            # 每隔1000次训练保存一下
            if i % 1000 == 0:
                print("After %d training step(s), loss on training batch is %g." % (step, loss_value))
                saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)


def main(argv=None):
    cifar10.maybe_download_and_extract()
    train(cifar10)

if __name__ == '__main__':
    tf.app.run()


