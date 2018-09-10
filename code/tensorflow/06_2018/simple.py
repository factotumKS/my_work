import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('/tmp/mnist/', one_hot=True)

# 输入占位
x = tf.placeholder("float32", shape=[None, 784])
y_ = tf.placeholder("float32", shape=[None, 10])

# 声明参数
weight = tf.Variable(tf.zeros([784, 10]))
biases = tf.Variable(tf.zeros([10]))

# 
y = tf.nn.softmax(tf.matmul(x, weight) + biases)
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
train_step = tf.train.GradientDescentOptimizer(0.01).\
    minimize(cross_entropy)

# 
with tf.Session() as sess:
    sess.run(tf.initialize_all_variables())
    for i in range(1,1000):
        if i % 10 == 0:
            print("the %d step(s) on training" % i)
        batch = mnist.train.next_batch(50)
        train_step.run(feed_dict={x: batch[0], y_: batch[1]})
    correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float32"))
    print(sess.run(accuracy,
        feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
