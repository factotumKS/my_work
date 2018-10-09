

## 1、GAN(Generative Adversarial Net)

​	GAN，即生成对抗网络，出现的目的是解决自动生成问题，在图像领域已经有了很大成果。GAN的原理是有两个网络G和D。分别代表生成（generator）和判断（Discriminator）。同时训练这两个网络：

​	1、对于G，训练其画出更高质量的图像；

​	2、对于D，训练其有更强的判断能力；

​	我们期待的最后结果是，G生成的图像在D眼中质量真假难辩（50%）。

### 1.1、 Value Function

​	GAN并没有损失函数，优化的过程是G与D之间的“零和博弈”：

$$min_{G}max_{D}V(D,G)=E_{x~p_{data}(x)}[logD(x)]+E_{z~p_{z}(z)}[log(1-D(G(z)))]$$

​	训练过程中D需要尽可能地正确分类，即最大化$E_{x~p_{data}(x)}[logD(x)]$；相应地G需要最大化D的损失，即最小化$E_{z~p_{z}(z)}[log(1-D(G(z)))$。训练中依次更新D和G的参数进行j交替迭代：

​	每次按照分布$P_{g}(z)$取minibatch：$\{z^{(1)},...,z^{(m)}\}$进行训练，

​	D的随机梯度下降：$\nabla_{\theta d} \frac{1}{m}\sum_{i=1}^{m}[log(D(x^{(i)})+log(1-D(G(z^{(i)})))]$

​	G的随机梯度下降：$\nabla_{\theta g}\frac{1}{m}\sum_{i=1}^{m}log(1-D(G(z^{(i)})))$

### 1.2、优缺点

​	优点：[OpenAI Ian Goodfellow的Quora问答：高歌猛进的机器学习人生](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2650718178&idx=1&sn=6144523762955325b7567f7d69a593bd&scene=1&srcid=0821xPdRwK2wIHNzgOLXqUrw&pass_ticket=uG39FkNWWjsW38Aa2v5b3cfMhixqsJ0l1XLhNr5mivWEaLyW5R1QED0uAKHOwuGw#rd)

​	1、生成的样本质量更高；

​	2、生成对抗式网络框架能训练任何一种生成器网络（理论上-实践中，用 REINFORCE
来训练带有离散输出的生成网络非常困难）。大部分其他的框架需要该生成器网络有一些特定的函数形式，比如输出层是高斯的。重要的是所有其他的框架需要生成器网络遍布非零质量（non-zero
mass）。生成对抗式网络能学习可以仅在与数据接近的细流形（thin manifold）上生成点；

​	3、不需要遵循任何种类的因式分解模型，任何G和D都是通用的；

​	缺点：

​	1、GAN在“纳什均衡”下达到最优，但是非凸优化可能不能靠梯度下降收敛；

​	2、过于自由，G和D缺少限制，无法区分训练过程中是否有进展；



## 2、cGAN(Conditional Generative Adversarial Nets)

​		与GAN相比，区别在于”conditional“所谓条件。

### 2.1、Value Function

​	GAN的value function：

$$min_{G}max_{D}V(D,G)=E_{x~p_{data}(x)}[logD(x)]+E_{z~p_{z}(z)}[log(1-D(G(z)))]$$

​	cGAN的value function：

$$min_{G}max_{D}V(D,G)=E_{x~p_{data}(x|y)}[logD(x)]+E_{z~p_{z}(z)}[log(1-D(G(z|y)))]$$

​	区别在于条件变量y的引入，其作为一个额外的输入层