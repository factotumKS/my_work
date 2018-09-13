# tensorflow_doc1

## 一、tensorflow基础知识

### 计算图Graph

​	tensorflow程序维护着一个默认计算图(default graph)，有需要的话也可以使用一些管理图的函数来 同时使用多个图。一个计算图上记载了需要进行的计算。

​	使用计算图可以把高运算计算放在python外进行，同时更进一步设法避免上述的额外运算开销，好像是用C/C++写的。python只作为指挥，通过图和计算部分进行交流。

### 会话session

​	计算图上记载了我们需要做的事情，但是如何去做？计算的工作由tensorflow内部进行优化，这时我们就需要申请一个会话`sess = tf.Session()`并用这个会话对象去进行实际的计算。会话是很宝贵的，使用之后需要及时释放资源。

​	在会话中，计算可以被指定部署在一个GPU或者CPU上：

```python
with tf.Session() as sess:
    with tf.device("/gpu:0"):
        mat1 = tf.constant([[1., 2.]])
        mat2 = tf.constant([[3., 4.]])
        result = tf.matmul(mat1, mat2)
```

​	使用`sess.sun()`开始计算整个图。

### 张量tensors

​	张量包含但是不局限于一个高维数组，tensorflow中所有的数据都以张量的形式被存储，包括常量和变量。

### 变量variables

​	变量维持图计算时的状态信息。

​	变量能够在计算过程中被读取和修改，模型参数一般都是变量。变量需要先被初始化，才能在session中被使用，这很好理解，“形参”在被赋值之前是没办法进行计算的。

### 供给feeds

​	feed用一个tensor临时替换一个操作的输出结果，最常见的用法是创建placeholder等待feed作为输入。

```python
x = tf.placeholder("float", shape=[None, 784])
```

​	placeholder如其名，是一个需要赋值的占位符，shape是一个可选参数，通过shape我们可以自动捕捉到传入数据的格式错误。



## 二、训练模型

​	计算我们的预测结果，并定义代价函数（这里以交叉熵为例），用来衡量预测结果的糟糕程度。

```
y = tf.nn.softmax(tf.matmul(x,W) + b)
cross_entropy = tf.reduce_sum(y_*tf.log(y))
```

​	使用下面这条语句为计算图添加一个新的操作，包括梯度计算和参数的步长优化等（这里用快速梯度下降函数作为例子）。

```python
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
```

​	`train_step`这个操作可以用梯度下降来更新权值，反复运行`train_step`可以进行训练。



## 三、测试模型

​	测试时使用单独的测试数据集合，依然用argmax函数来比较前向传播结果和标签的一致程度。

​	对返回的布尔数组转换成相应的浮点数数组，然后再取平均值。

​	最后计算在测试数据集上的准确率。这里把测试部分加入了计算图，feed部分喂的是测试集。

```python
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction,"float"))
print accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels})
```

​	

## 四、卷积神经网络

​	一般由卷积层conv和池化层交替而成，其中需要重点强调的是

### dropout

​	dropout是一种优秀的正则化策略，训练出来的模型不仅泛化能力强，还可以减少训练的工作量。

​	下面的这条语句表示训练时神经元的保留概率是0.5。

```python
h_fc1_drop = tf.nn.dropout(h_fc1, 0.5)
```