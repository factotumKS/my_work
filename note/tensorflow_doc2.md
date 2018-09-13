# tensorflow_doc2

## 一、一个真实的程序

### 输入占位符

​	为输入和标签准备占位符。

```
images_placeholder = tf.placeholder(tf.float32, shape=batch_size,IMAGE_PIXELS))
labels_placeholder = tf.placeholder(tf.int32, shape=(batch_size))
```

​	后面会使用feed_dict参数，将数据传入`sess.run()`，其键值就是占位符号。

### 构建图表

​	分为三个部分较好

​	inference()：尽可能构建好推理，表示前向传播。

​	loss()：向inference图表中添加损失函数。

​	training()：向损失图表添加计算并应用梯度。

#### 推理（inference）

​	接受占位符作为输入。图上每一层都创建于一个唯一的`tf.name_scope`之下，创建在其作用域下面的所有元素都带有该前缀，如下变量名称即为hidden1/w1。

```
with tf.name_scope('hidden1') as scope:
	w1 = tf.Variable(tftruncated_normal([IMAGE_PIXELS,
		hidden1_units], stddev=1.0 / math.sqrt(float(IMAGE_PIXELS))), name
		='weights')
	b1 = tf.Variable(tf.zeros([hidden1_units]), name='biases')
	hidden1 = tf.nn.relu(tf.matmul(images, weights) + biases
```

​	每个变量在构建的时候都进行了初始化操作。最后得到的hidden1就是这一层的输出。

```python
logits = tf.matmul(hidden2, weights) + biases
```

​	整个inference的输出是logits。

#### 损失（loss）

​	通过在原inference上面添加。

​	先将label_placeholder中的值编码成一个含有1-hot values的Tensor，再添加一个操作来比较inference的输出和1-hot标签所输出的logits Tensor。

```python
cross_entropy=tf.nn.softmax_cross_entropy_with_logits(logits,onehot_labels,name='xentropy')1
loss = tf.reduce_mean(cross_entropy, name='xentropy_mean')
```

​	最后使用tf.reduce_mean函数计算交叉熵平均值。

