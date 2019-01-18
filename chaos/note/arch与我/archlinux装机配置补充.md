---
title: archlinux装机与使用错误记录 
date: 2018/10/02
---
​	大多数人装机参考的是[吴迪的博客](https://www.viseator.com/2017/05/17/arch_install/)，这篇博客真是arch入门的福音（膜），这里我根据自己的一些坑给出一些补充。

## A

### archive

​	[档案库](https://archive.archlinux.org/)，你一定用的上。

### anaconda

​	[官网下载安装](https://www.anaconda.com/download/#download)，如果你是深度学习选手你也需要它。

​	别忘了添加清华源：

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes
```

​	之后就可以创建环境了：

```bash
conda create -n your_env_name python=3.7
```

​	再在环境中安装合适的包：

```bash
conda install -n 环境 [package]
conda remove --name 环境 [package]
```



## C

### cuda & cudnn

​	本来在这里要给出官网连接，但是考虑到下载速度还有nvidia官网比较混乱，还是用上面的档案库最省心了！下载下来后`sudo pacman -U 包名称`就可以了，记得留着这些pkg。

​	还有个最大的问题就是官网下载的`.run`安装包好像非常消耗`/tmp`，我曾经装`cuda9`的时候因为空间不够终止了，与其想办法对`/tmp`扩容，还不如档案库轻松。

​	PS：不同的cuda有不同的gcc依赖，一般都是老版本，同样也要记得在档案库下。



## F

### fcitx

​	使用xfce4在命令行缺少字体，需要下载，需要下载[powerline字体](https://github.com/powerline/fonts)作为原来的补充，下载并安装即可。

​	同时安装`sunpinyin`之类的输入法之后，要更改输入方式，使用工具`fcitx-configtool`，加入`sunpinyin`输入。

​	有人提到了不一样的东西，这里mark一下：

```shell
# ~/.xinitrc
export LC_ALL=zh_CN.UTF-8
export XMODIFIERS=@im=fcitx
eval `dbus-launch --sh-syntax --exit-with-session`
exec fcitx &
```



## G

### gcc

​	gcc老版本无法用`pacman`安装，`yay`找到的很多是非官方源，下载速度也不保证，最好的办法还是去档案库。



## H

### hexo

​	在已经有git的基础上搭建博客，准备hexo需要下面这些命令，网上博客实在太多了这里就抓大放小。

```bash
sudo pacman -S hexo-cli
npm instlal
hexo init
```

​	准备ssh的支持的话需要安装一个包`openssh`，很多博客都没有提到，让人感觉十分粗糙。

```bash
ssh-keygen -t rsa -C "自己的邮箱"
```

​	之后上传博客就是三条命令

```bash
hexo clean
hexo g
hexo d
```



## M

### mkfs

​	在重装系统时，记得不只要对根分区格式化`mkfs.ext4`，还要对引导分区格式化，否则会无法下载`base`和`base-devel`，最后会导致`arch-chroot`失败。



## N

### nvidia

​	根据[某位前辈的博客](https://www.jianshu.com/p/eda410b53d5d)，nvidia独显在不做任何处理的情况下安装会导致黑屏，应该是跟xorg发生了冲突导致的。

​	需要添加黑名单：

```shell
# /etc/modprobe.d/配置文件
blacklist nouveau
blacklist lbm-nouveau
options nouveau modeset=0
alias nouveau off
alias lbm-nouveau off
```

​	然后再安装nvdia和bumblebee：

```bash
yaourt -S mesa xf86-input-mouse xf86-input-evdev xf86-input-keyboard nvidia bumblebee
sudo usermod -a -G bumblebee scorpion
sudo systemctl enable bumblebeed
```

### nvidia-smi

​	查看gpu的程序，如果找不到gpu，重启就可以了，不用太纠结。



## P

### pytorch

​	[官网首页](https://pytorch.org/)上给出了一张表，上面有各种配置组合下pytorch的安装方式，参考即可。

​	

## S

### shadowsocks

​	我使用的VPS是[banwagong](https://www.bwh1.net/index.php)，banwagong可以自动配置服务端，但是kiwi面板上却把这个选项删除了，但是没关系，[这个链接](https://kiwivm.64clouds.com/main-exec.php?mode=extras_shadowsocks)依然是有效的，他们只是把这个选项隐藏了而已（笑）。



## T

### tensorflow

​	tensorflow对cuda和cudnn的版本有着苛刻的依赖，用下面这种方式就可以安装

```
pip3 install tensorflow-gpu==1.8.0
pip3 install --upgrade tensorflow-gpu
```

​	之后只要看报错信息就可以了，如果`import`没有错误，还要在`sess`创建时看看有没有报错，这里的报错一般和cuda和cudnn版本不对有关，只要跟据缺少的`.so`文件版本号到档案库找到合适版本的cuda和cudnn就可以了。




## V

### vim

​	如果喜欢solarized配色的话可以到[这个仓库](https://github.com/altercation/solarized)下载，并把`.vim`文件放置在`~/.vim/colors`中。

### virtualbox

​	安装时可以选择两种modules，一种是`dkms`一种是`arch`，archwiki上推荐了安装后者，如果安装前者的话还需要安装一个包`linux-headers`，否者系统找不到虚拟机的内核。

​	如果你先前用的是`arch`，后来换了`dkms`，可能会出现大问题，对于我来说，没有自动安装`linux-headers`，并且报出了很奇怪的错误：

```bash
QT FATAL: binary applicatino ... setuid ... security hole
```

​	千万不要重捣覆辙。

​	如果实在发生了这种事的话，可以安装`virtualbox-bin`，可以有效解决问题。



## W

### wps

​	wps在按照fcitx的配置更改之后虽然可以使用中文输入法，但是不会有任何中文被输入，所以还是安装virtualbox来得更舒服一些。



## Z

### oh-my-zsh

​	第一时间安装这个

```bash
sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
```



