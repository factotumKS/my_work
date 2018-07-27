# 只用于训练
import tensorflow as tf
import numpy as np

from data import get_data_set

train_x, train_y, train_l = get_data_set(cifar=10)
test_x, test_y, test_l = get_data_set("test", cifar=10)

batch_size = 128
Train_steps = 100000

def add_full_layer(input_x,layer_numble,node_num,alpha = 1,activation_function = None):
	layer_name = 'full_connected_layer%s' %layer_numble
	with tf.name_scope(layer_name):
		with tf.name_scope('Weight'):
			Weight = tf.Variable(tf.random_normal([input_x.shape.as_list()[1]]+[node_num],stddev=0.0001),dtype = tf.float32,name = "W")
			tf.summary.histogram(layer_name+'/Weight',Weight)
		with tf.name_scope('Bias'):
			bias = tf.Variable(tf.constant(0.1,shape = [node_num]),dtype = tf.float32,name = "b")
			tf.summary.histogram(layer_name+'/bias',bias)
		with tf.name_scope('W_x_add_b'):
			temp = tf.add(tf.matmul(input_x,alpha*Weight),bias)
		if(activation_function is None):
			output_y = temp
		else:
			output_y = activation_function(temp)
		tf.summary.histogram(layer_name+'/output',output_y)
		return output_y

def add_cov_layer(input_x,layer_numble,filter_size,activation_function = None):
	layer_name = "convolutional_layer%s" %layer_numble
	with tf.name_scope(layer_name):
		with tf.name_scope("Filter"):
			Filter = tf.Variable(tf.random_normal(filter_size,stddev=0.1),dtype = tf.float32,name = "filter")
			tf.summary.histogram(layer_name+'/filter',Filter)
		with tf.name_scope("Bias"):
			bias = tf.Variable(tf.constant(0.1,shape = [filter_size[3]]),dtype = tf.float32,name = "bias")
			tf.summary.histogram(layer_name+'/bias',bias)
		with tf.name_scope("convolution"):
			conv = tf.nn.conv2d(input_x,Filter,strides=[1, 1, 1, 1], padding='SAME')
		with tf.name_scope('conv_add_b'):
			temp = tf.add(conv,bias)
		if(activation_function is None):
			output_y = temp
		else:
			output_y = activation_function(temp)
		tf.summary.histogram(layer_name+'/output',output_y)
		return output_y

def add_max_pool(input_x,layer_numble,k_size):
	layer_name = 'pool_layer%s' %layer_numble
	with tf.name_scope(layer_name):
		output_y = tf.nn.max_pool(input_x,[1, k_size, k_size, 1],strides=[1, 2, 2, 1],padding = 'SAME')
		tf.summary.histogram(layer_name+'/output',output_y)
	return output_y

def add_avg_pool(input_x,layer_numble,k_size):
	layer_name = 'pool_layer%s' %layer_numble
	with tf.name_scope(layer_name):
		output_y = tf.nn.avg_pool(input_x, [1, k_size, k_size, 1],strides=[1, 2, 2, 1],padding = 'SAME')
		tf.summary.histogram(layer_name+'/output',output_y)
	return output_y

def stack2line(input_x,layer_numble):
	layer_name = 'stack2line%s' %layer_numble
	with tf.name_scope(layer_name):
		output_y = tf.reshape(input_x,[-1,tf.cast(input_x.shape[1]*input_x.shape[2]*input_x.shape[3],tf.int32)])
	return output_y

#the entrence of the data
with tf.name_scope('input'):
	x = tf.placeholder(tf.float32,[None, 3072],name = 'x_input')
	y_ = tf.placeholder(tf.float32,[None,10],name = 'y_input')
	x_imgs = tf.reshape(x,[-1,32,32,3])

keep_prob = tf.placeholder(tf.float32)
########################################################
#the structure of the cnn:
output_layer1 = add_cov_layer(x_imgs,1,[5,5,3,32],activation_function = None)
output_layer2 = add_max_pool(output_layer1,2,3)
output_relu = tf.nn.relu(output_layer2)
output_layer3 = add_cov_layer(output_relu,3,[5,5,32,32],activation_function = tf.nn.relu)
output_layer4 = add_avg_pool(output_layer3,4,3)
output_layer5 = add_cov_layer(output_layer4,5,[5,5,32,64],activation_function = tf.nn.relu)
output_layer6 = add_avg_pool(output_layer5,6,3)
output_layer6 = stack2line(output_layer6,7)
output_layer7 = add_full_layer(output_layer6,8,64,alpha = 1,activation_function = None)
y = add_full_layer(output_layer7,9,10,alpha = 1,activation_function = tf.nn.softmax)
#########################################################
#define of loss_function
with tf.name_scope('cross_entropy'):
	cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]),name='cross_entropy')
	tf.summary.scalar('cross_entropy',cross_entropy)
#########################################################
#define train optimizer
with tf.name_scope('train'):
	train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
#########################################################
#culculate the accuracy
with tf.name_scope('accuracy'):
	prediction = tf.equal(tf.argmax(y,1),tf.argmax(y_,1))
	accuracy = tf.reduce_mean(tf.cast(prediction,tf.float32),name = 'accuracy')
	tf.summary.scalar('accuracy',accuracy)
#########################################################
save=tf.train.Saver()

with tf.Session(config = tf.ConfigProto(log_device_placement = True)) as sess:
	init = tf.global_variables_initializer()
	sess.run(init)
	merge = tf.summary.merge_all()
	writer = tf.summary.FileWriter('log/',sess.graph)
	try:
		save.restore(sess,'./cifar10_quick/cifar10_quick.ckpt')
	except:
		pass
	for i in range(Train_steps):
		randidx = np.random.randint(len(train_x), size=batch_size)
		batch_xs = train_x[randidx]
		batch_ys = train_y[randidx]
		# train
		sess.run(train_step,feed_dict = {
			x:batch_xs,
			y_:batch_ys,
			keep_prob:1.0
		})
		if(i%100 == 0):
			accuracy_batch = sess.run(accuracy,feed_dict = {
			x:batch_xs,
			y_:batch_ys,
			keep_prob:1.0
		})
			loss_batch = sess.run(cross_entropy,feed_dict = {
			x:batch_xs,
			y_:batch_ys,
			keep_prob:1.0
		})
			result = sess.run(merge,feed_dict = {
			x:batch_xs,
			y_:batch_ys,
			keep_prob:1.0
		})
			writer.add_summary(result,i)
			print('after %d train steps the loss on the batch data is %g and the accuracy on batch data is %g'%(i,loss_batch,accuracy_batch))
		# 每100步保存一次训练参数
			save_path=save.save(sess,'./cifar10_quick/cifar10_quick.ckpt')
	print('check_point:save_path is ',save_path)