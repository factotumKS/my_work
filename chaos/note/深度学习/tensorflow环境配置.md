# archlinux上pytorch和tensorflow的环境配置anaconda+cuda+cudnn

### 一、安装nvidia显卡驱动

这一部分来自https://www.jianshu.com/p/eda410b53d5d做了些许改动
安装之后会导致黑屏，与原来的一些配置产生了冲突，需要进行一些修改。

```sh
#/etc/modprobe.d/这里有一个nvidia相关的配置文件
blacklist nouveau
blacklist lbm-nouveau
options nouveau modeset=0
alias nouveau off
alias lbm-nouveau off
```

去除原来的nvidia的设置，如果有的话

```bash
cd /etc/X11/
rm xorg.conf
```

安装一些必要依赖

```bash
yaourt -S mesa xf86-input-mouse xf86-input-evdev xf86-input-keyboard
```

**在这里才要安装nvidia显卡驱动**

```bash
yaourt -S nvidia bumblebee
```

把自己就爱入用户组并启用bumbleed

```bash
sudo usermod -a -G bumblebee username
sudo systemctl enable bumblebeed
```



### 二、安装cuda

安装最新版本的cuda。

```bash
sudo pacman -S cuda
```



### 三、安装cudnn

官网的[cudnn档案库](https://developer.nvidia.com/rdp/cudnn-archive)下载合适的版本，并把相应的文件补充到cuda当中。话说这里有个坑，好像cuda并不会把自己的库文件加入某个路径中，所以你必须手动补上一句。

```sh
# ~/.zshrc 或者 ~/.bashrc
export LD_LIBRARY_PATH="/你cuda的位置/lib64:$LD_LIBRARY_PATH"
```



### 四、安装anaconda3

[虚拟环境管理器下载](https://www.anaconda.com/download/#download)，集中了一些深度学习需要用到的package，可以选择python的版本；

``` bash
conda create -n your_env_name python=3.5
```

如果你不添加国内的地址（清华镜像），我觉得你的速度会慢到无法创建一个环境；

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes
```

环境的激活&关闭；

```bash
source activate 环境
source deactivate
```

对环境安装、删除额外的包；

```bash
conda install -n 环境 [package]
conda remove --name 环境 [package]
```

删除整个虚拟环境；

```
onda remove -n 环境 --all
```

PS：如果你使用的是zsh而不是bash，可能anaconda的路径并不会加入你的$PATH，手动添加一下；

```
# ~/.zshrc
export PATH="$PATH:/home/fool/anaconda3/bin"
```



### 五、框架1：tensorflow

直接到python官方找合适版本的轮子下载；

要求比较苛刻，需要合适版本的python，合适版本的cuda（附带cudnn）。

安装特定版本和更新到最新版本。	

```bash
pip install tensorflow-gpu==1.8.0
pip install --upgrade tensorflow-gpu
```

PS：如果你的pip找不到tensorflow，要么你的python是32位的，要么你的python版本太高了，对!tensorflow不支持高版本的python，你需要用anaconda弄一个python3.5的虚拟环境。

PS：如果你import tensorflow成功了，别高兴太早，可能会出现下面这样的warning

```bash
>>> sess = tf.Session()
2018-09-10 17:31:02.206807: I tensorflow/core/platform/cpu_feature_guard.cc:137] Your CPU supports instructions that this TensorFlow binary was not compiled to use: SSE4.1 SSE4.2 AVX AVX2 FMA
2018-09-10 17:31:02.306919: E tensorflow/stream_executor/cuda/cuda_driver.cc:406] failed call to cuInit: CUDA_ERROR_UNKNOWN
2018-09-10 17:31:02.306971: I tensorflow/stream_executor/cuda/cuda_diagnostics.cc:145] kernel driver does not appear to be running on this host (Saya): /proc/driver/nvidia/version does not exist
>>>
```

原因是你的CPU虽然支持tensorflow，但是tensorflow并没有按照你的CPU进行编译，虽然这并不影响你的程序运行，但是总让人感觉某一天就会炸掉。如果你不喜欢这个warning，最好下载tensorflow源码，用bazel编译你自己的.whl文件。

最后在你的虚拟环境里按照这两条语句安装。

```bash
pip install XXX.whl
conda install -n TensorFlow --use-local XXX.whl
```



### 六、框架2：pytorch

使用conda在cuda9.2的支持下安装pytorch，详见[pytorch官网](https://pytorch.org/)

```bash
conda install pytorch torchvision cuda92 -c pytorch
```



### 七、简单的package版本回退工具

考虑到tensorflow对各组件的版本控制过于严格，使用downgrade来回退版本，但是downgrade并似乎不能自动解决依赖，必须手动解决。

```bash
sudo pacman -S downgrade
downgrade cuda
```



### 八、pacman不更新某些软件

我们不能让cuda一更新就退回去，所以加一下“黑名单”。

```sh
# /etc/pacman.conf 
IgnorePkg = emacs		#软件包
IgnoreGroup = xfce4		#软件包组
```

如果不确定自己安装的cuda到底是什么版本可以用pacman查看详细信息。

```
pacman -Qi cuda
```



### 九、各种组合尝试

直至2018/09/09我尝试过的组合。

这里版本是不确定的，根据import时显示的报错信息来选择合适的cuda和cudnn，看丢失了那个版本的so文件就补上哪个就行了。

其中因为不明原因我没能装上cuda9.0，需要gcc6但是依赖无法解决的样子，自己yaourt也无法装上，十分无奈。

```sh
#cuda	cudnn	tensorflow
#9.2	7.1		None
#9.0	7.1		1.6.0~1.10.0
#8.0	6.0		1.4.0
```


