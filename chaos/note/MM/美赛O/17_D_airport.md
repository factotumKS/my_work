# 55285

- 乘客到达
- 乘客从A到B
- ID检查
- 等待安检
- 准备安检，在队列首部放东西
- 进行安检
- 安检失败的选手要去D

## 2、模型假设

### 2.1、假设

- 体现整体水平
- 乘客到达间隔为泊松分布
- ID检查、安检扫描时间符合高斯分布
- 乘客知道规则
- 没有紧急事件
- 检查点在A和b都有4个站点
- 不考虑过境时间

```
We do not take the transiting time between different stations into consideration
```



### 2.1、记号



## 3、安检的基本模型

### 3.1、模型设计

​	四个子模型

- 流入模型：该模型旨在模拟乘客的随机到达；

```
Inflow model: This model is designed to simulate the random arrivals of the pas-
sengers
```

- 子模型二：属性生成模型：在这个模型中，对乘客赋予不同的属性来影响安全检查的时间长度；

```
Sub model two: Attributes generating model: In this model, we attribute different
properties to the passengers that will influence the time length of security check.
```

- 排队模型：该模型研究排队等待的过程；

```
Queuing model: This model studies the process of waiting in lines.
```

- 筛选模型：讨论了准备过程和扫描过程；

```
Screening model:  The preparing process and the screening process are discussed
in this model.
```

### 3.2、子模型

#### 3.2.1、流入

​	泊松拟合，excel

#### 3.2.2、子模型二

​	高斯分布，excel找到他们的样本均值和样本方差

#### 3.2.3、排队模型

​	

#### 3.2.4、扫描模型

​	人和物品screening最大值

```
When the passengers finished queuing, they first begin to prepare their belongings.
Then  the  passengers  and  their  belongings  are  scanned  respectively.   The  time  cost  in
this process should be the maximum of the millimeter wave scanning ti...
```



### 3.3、模型结果

#### 3.3.1、总时间的分布T

​	不同总时间的概率差不多，解释了为什么乘客难以找到合适的时间到达机场（就是啥也没看出来喽）

```
First we want to figure out how T, the total time consumed in the security check distribute among the travelling populations. We pick out 31678 samples, obtain their total times, and plot Figure 2. According to Figure 2, the total time distribute very uniformly among the populations.  That is to say, the probability of the different total time is similar. That explains why it is difficult for passengers to find a suitable time to arrive at the airport
```



#### 3.3.2、不同步骤花费的时间比例

​	扇形图显示等待screening的时间很长。

```
Then we consider the proportion of the time consumed in different steps, and draw figure 3.  We can see that the time of waiting for screening is very large in proportion to the rest of time. That is the main reason for the congestion of the airport
```



#### 3.3.3、预检乘客与普通乘客比例的影响

​	PS：预检是美国的快速通道政策，检查步骤会简化，需要提前申请。

​	预检乘客越多，平均时间越短；

​	这里居然使用了生物中自然生长的S曲线，也就是sigmoid函数拟合来拟合数据。

```
We know that the more Pre-Check passengers, the smaller average time.  Therefore, （T avg）will finally converge to the value when everyone can use Pre-Check lane and spend less time, just like the ‘S’ curve of the Natural Growth Model (NGM) in biolagy.  We try to use one function of the NGM, Equation (4), to fit the data.  The correlation coefficient of the fitting is 0.99, which confirms our thought
```



#### 3.2.4、预检通道和普通通道的比例的影响

​	尝试了1：3、2：2、3：1三种，结果画图拟合，现实稳定时间消耗，比例越大平均消耗时间越大。

​	

​	

## 4、当前进程的改进

​	根据第一个模型，四个车分配和百分比预检乘客都是最佳的，然而，机场仍然发生拥堵。因此，我们需要找到更多策略来改进安全检查制度。

​	提出三个模型：

- Multi-passenger linkage model of belongings preparation (MPL model)
- Priority-based queuing model(PBQ model)，优先队列模型
- Model of special population (SP model)

### 4.1、Multi-passenger Linkage Model of Belongings Preparation

​	之前说拥挤主要发生在等待screen的过程中。

​	（计算机中流水线中很常见的情况，有的计算需要外部输入，这个时候我们的处理办法是在早的计算进行时就开始输入做好准备）

```
a  passenger  cannot  begin  preparing  his  or  her belongings until the last passenger finishes preparing.	
```

​	假设每个检查站都允许N人准备乘客同时准备他们的物品。 一旦乘客完成准备并开始筛选过程，等候线前面的另一名乘客可以加入准备过程。 在这个联系过程中，我们可以保证总有几名乘客一起准备他们的物品。 虽然某位乘客的准备时间没有减少，但其他乘客的等候时间却减少了。

#### 4.1.2、MPL模型的有效性

​	等待区域不拥挤的话就可以增长N，改变N的值画曲线发现，N=3是最好的。

​	（蛤？咋实现的？）

### 4.2、Priority-based Queuing Model，优先队列模型

#### 4.2.1、PBQ模型的设计

​	设置了两个时间常量Tad1、Tad2，所以根据等待时间分成3个优先级别；有1个预检通道，2个普通通道，和一个紧急通道；等待时间过长的人可以按照优先级进入紧急通道。（差不多是这个意思）

```
For different priorities, passengers enjoy different policies.  For the priority group, passengers can use the emergency lane immediately.  For the regular group, passengers cannot  go  pass  the  emergency  lane  until  they  have  been  waiting  at  the  airport  for  a period of tad1.  When a period of tad2 has passed, the passengers of the over-punctual group  can  make  use  of  the  emergency  lane.   This  policy  can  not  only  guarantee  that the one in an urgent can get aboard in the first time, but also warn people not to arrive unnecessarily early. Figure 12 discribes this new modification
```

#### 4.2.2、PBQ模型的可行性，Effectivene

​	

