# meet1



## 1、markdown

​	markdown是一种标记语言，其简洁、高效的特点决定了这是程序员记录笔记的好工具。



​	编辑器：typora、remarkable等。



​	常用功能：插入链接、插入图片、代码高亮、数学公式渲染。



​	数学公式渲染：



​		例子：

​		`min_{G}max_{D}V(D,G)=E_{x~p_{data}(x)}[logD(x)]+E_{z~p_{z}(z)}[log(1-D(G(z)))]`

​		$$min_{G}max_{D}V(D,G)=E_{x~p_{data}(x)}[logD(x)]+E_{z~p_{z}(z)}[log(1-D(G(z)))]$$

​	

​		常用：

​		_{}：下标

​		^{}：上标

​		\lambda：希腊字母lambda（小写）

​		\Lambda：希腊字母lambda（大写）

​		\rightarrow：箭头

​		\frac {} {}：分式

​		……





## 2、机器学习与深度学习

![](/home/factotum/my_work/tencent_ML/MLnDL.jpg)



### 2.1、人工智能是什么？

​	无定论。

​	

​	解决的问题：回归、分类、聚类、（降维）。



### 2.1、机器学习是什么？

​	

​	机器学习算法可以分为监督，无监督，半监督。



​	常用的机器学习算法：

​	KNN

![](/home/factotum/my_work/tencent_ML/knn.jpg)



​	LR

![](/home/factotum/my_work/tencent_ML/sigmoid.jpg)

![](/home/factotum/my_work/tencent_ML/lr.jpg)



​	K-means

![](/home/factotum/my_work/tencent_ML/kmeans.jpg)



​	SVM

![](/home/factotum/my_work/tencent_ML/svm.jpg)



​	NN

​	[神经网络游乐场](http://playground.tensorflow.org)



### 2.2、深度学习是什么？

![](/home/factotum/my_work/tencent_ML/feeling.jpg)

​	

![](/home/factotum/my_work/tencent_ML/model.jpg)

​	

​	经典深度学习模型：CNN、RNN

![](/home/factotum/my_work/tencent_ML/cnn.jpg)​	![](/home/factotum/my_work/tencent_ML/rnn.jpg)

​	

​	深度学习的应用：CV、NLP、OCR、强化学习

![](/home/factotum/my_work/tencent_ML/cv.jpg)	



### 2.3、需要什么知识储备？

#### 2.3.1、数学知识

​	线性代数：不需多言；

​	概率论：ML的本质就是概率论；

​	数值分析：SGD、adam等优化方法；



​	可以去看《深度学习》这本书的数学知识部分（其余内容门槛较高，不建议强行看）



#### 2.3.2、工具

​	机器学习：

​		python编程语言，pandas、numpy、skit-learn等库,

​		《机器学习》、《统计学习方法》；

​		matlab软件， 含有各种工具箱；



​	深度学习：

​		python编程语言；

​		深度学习框架：tensorflow、pytorch、kera、caffe；

​		官方文档、教程、论文；

​		[cuda+cudnn+(pip3/anaconda](https://factotumks.github.io/2018/10/02/archlinux%E8%A3%85%E6%9C%BA%E9%85%8D%E7%BD%AE%E8%A1%A5%E5%85%85/)



## 3、下次的任务

### 1、DDL

​	两星期后的第三次见面；



### 2、内容

#### 2.1、数学部分

​	《深度学习》数学部分



#### 2.2、代码部分

##### 2.2.1、机器学习

​	LR（逻辑回归），最多使用numpy库写一个。

​	K-means，同上。



##### 2.2.2、深度学习

​	配环境 + 找文档跟着教程做一个手写数字识别。

