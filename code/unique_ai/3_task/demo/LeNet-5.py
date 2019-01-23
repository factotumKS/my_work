# _author_ = XJTU_Ironboy
import tensorflow as tf
# 导入MNIST数字手写体数据集
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/",one_hot = True)
# 定义LeNet-5的所有层的结构、训练次数、batch size
in_units = 784
C1_units = 6
S2_units = 6
C3_units = 16
S4_units = 16
C5_units = 120
F6_units = 84
output_units = 10

train_steps = 10000 
batch_size =128

# 定义输入
x = tf.placeholder(tf.float32,[None,in_units],name = "x_input")
y_= tf.placeholder(tf.float32,[None,output_units],name = "y_input")
keep_prob = tf.placeholder(tf.float32)
input_data = tf.reshape(x,[-1,28,28,1])

# 定义可配置卷积层函数
def conv(layer_name,input_x,Filter_size,activation_function = None):
	with tf.name_scope("conv_%s" % layer_name):
		with tf.name_scope("Filter"):
			Filter = tf.Variable(tf.random_normal(Filter_size,stddev = 0.1),dtype = tf.float32,name = "Filter")
			tf.summary.histogram('Filter_%s'%layer_name,Filter)
		with tf.name_scope("bias_filter"):
			bias_filter = tf.Variable(tf.random_normal([Filter_size[3]],stddev = 0.1),dtype = tf.float32,name = "bias_filter")
			tf.summary.histogram('bias_filter_%s'%layer_name,bias_filter)
		with tf.name_scope("conv"):
			conv =  tf.nn.conv2d(input_x,Filter,strides = [1,1,1,1],padding = "SAME")
			tf.summary.histogram('conv_%s'%layer_name,conv)
		temp_y = tf.add(conv,bias_filter)
		with tf.name_scope("output_y"):
			if activation_function is None:
				output_y = temp_y
			else:
				output_y = activation_function(temp_y)
			tf.summary.histogram('output_y_%s'%layer_name,output_y)
		return output_y

# 定义可配置最大池化层函数
def max_pool(layer_name,input_x,pool_size):
	with tf.name_scope("max_pool_%s" % layer_name):
		with tf.name_scope("output_y"):
			output_y = tf.nn.max_pool(input_x,pool_size,strides = [1,2,2,1],padding = "SAME")
			tf.summary.histogram('output_y_%s'%layer_name,output_y)
		return output_y

# 定义可配置全连接层函数
def full_connect(layer_name,input_x,output_num,activation_function = None):
	with tf.name_scope("full_connect_%s" % layer_name):
		with tf.name_scope("Weights"):
			Weights = tf.Variable(tf.random_normal([input_x.shape.as_list()[1],output_num],stddev = 0.1),dtype = tf.float32,name = "weight")
			tf.summary.histogram('Weights_%s'%layer_name,Weights)
		with tf.name_scope("biases"):
			biases = tf.Variable(tf.random_normal([output_num],stddev = 0.1),dtype = tf.float32,name = "biases")
			tf.summary.histogram('biases_%s'%layer_name,biases)
	output_temp = tf.add(tf.matmul(input_x,Weights) , biases)
	with tf.name_scope("output_y"):
		if activation_function is None:
			output_y = output_temp
		else:
			output_y = activation_function(output_temp)
		tf.summary.histogram('output_y_%s'%layer_name,output_y)
	return output_y
	
# 通过调用函数的形式构建LeNet-5的结构
output_layer1 = conv("layer1",input_data,[5,5,1,6],activation_function = tf.nn.relu)
output_layer2 = max_pool("layer2",output_layer1,[1,2,2,1])
output_layer3 = conv("layer3",output_layer2,[5,5,6,16],activation_function = tf.nn.relu)
output_layer4 = max_pool("layer4",output_layer3,[1,2,2,1])
output_layer4 = tf.reshape(output_layer4,[-1,tf.cast(output_layer4.shape[1]*output_layer4.shape[2]*output_layer4.shape[3],tf.int32)])
output_layer5 = full_connect("layer5",output_layer4,120,activation_function = tf.nn.relu)
output_layer6 = full_connect("layer6",output_layer5,84,activation_function = tf.nn.relu)
output_layer7 = tf.nn.dropout(output_layer6,keep_prob)
with tf.name_scope("output_y"):
	y = full_connect("layer7",output_layer7,10,activation_function = tf.nn.softmax)
# 计算损失函数(交叉熵)、优化器、准确度
with tf.name_scope("loss"):
	loss = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]),name='cross_entropy')
	tf.summary.scalar("loss",loss)
with tf.name_scope("train"):
	train = tf.train.AdamOptimizer(1e-4).minimize(loss)
prediction = tf.equal(tf.argmax(y,1),tf.argmax(y_,1))
with tf.name_scope("accuracy"):
	accuracy = tf.reduce_mean(tf.cast(prediction,tf.float32),name = 'accuracy')
# 初始化所有的变量
init = tf.global_variables_initializer()
# 正式开始导入数据进行计算
with tf.Session() as sess:
	sess.run(init)
	merge = tf.summary.merge_all()
	writer = tf.summary.FileWriter('log/LeNet_log',sess.graph)
	for i in range(train_steps):
		batch = mnist.train.next_batch(batch_size)
		sess.run(train,feed_dict = {x:batch[0],y_:batch[1],keep_prob : 0.7})
		if i%100 ==0:
			accuracy_batch = sess.run(accuracy,feed_dict = {x:batch[0],y_:batch[1],keep_prob : 0.7})
			loss_batch = sess.run(loss,feed_dict = {x:batch[0],y_:batch[1],keep_prob : 0.7})
			print('after %d train steps the loss on the train dataset is %g and the accuracy on train dataset is %g'%(i,loss_batch,accuracy_batch))
			result = sess.run(merge,feed_dict={x:batch[0],y_:batch[1],keep_prob : 0.7})
			writer.add_summary(result,i)
		if i == train_steps-1:
			loss_test = sess.run(loss,feed_dict = {x:mnist.test.images,y_:mnist.test.labels,keep_prob:1})
			accuracy_test = sess.run(accuracy,feed_dict = {x:mnist.test.images,y_:mnist.test.labels,keep_prob:1})
			print('the loss in test dataset is %g and the accuracy in test dataset is %g'%(loss_test,accuracy_test))



