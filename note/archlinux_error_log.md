# archlinux_error_log

## git

​	[gitdownload](https://minhaskamal.github.io/DownGit/#/home)可以下载特定文件，只要输入连接就行。

## virtualbox

### 1、内核消失错误

​	FATAL显示一个十分重要的内核没了`vboxdrv`，没有这个内核，虚拟机是无法启动的。

​	据说需要更新系统的`heard`文件，所以安装一下`linux-headers`这个包，就解决了这个问题。



### 2、包错误

​	参照问题3会发现virtualbox的包本身有错误

```bash
➜  ~ virtualbox
Qt FATAL: FATAL: The application binary appears to be running setuid, this is a security hole.
[1]    1533 abort      virtualbox
```



### 3、virtualbox-bin

​	这个软件包解决了上面的错误2，替换了下面这些包。

```bash
==> Package conflicts found:
==> You will have to confirm these when installing
 -> Installing virtualbox-bin will remove: virtualbox-svn (virtualbox), virtualbox-host-modules-arch

[Aur: 1]  virtualbox-bin-5.2.18-1

:: Downloaded PKGBUILD (1/1): virtualbox-bin
  1 virtualbox-bin                   (Build Files Exist)
==> [N]one [A]ll [Ab]ort [I]nstalled [No]tInstalled or (1 2 3, 1-3, ^4)
==> Diffs to show?
==> 
```

​	替换之后virtualbox可以正常打开错误解决。

```bash
==> Remember to add allowed users to the vboxusers group:
==> # gpasswd -a USERNAME vboxusers
Optional dependencies for virtualbox-bin
    virtualbox-ext-oracle: for Oracle extensions
:: Running post-transaction hooks...
(1/8) Updating linux module dependencies...
(2/8) Install DKMS modules
==> dkms install vboxhost/5.2.18 -k 4.18.10-arch1-1-ARCH
Error! Module version 5.2.18 for vboxdrv.ko
is not newer than what is already found in kernel 4.18.10-arch1-1-ARCH (5.2.97).
You may override by specifying --force.
Error! Module version 5.2.18 for vboxnetflt.ko
is not newer than what is already found in kernel 4.18.10-arch1-1-ARCH (5.2.97).
You may override by specifying --force.
Error! Module version 5.2.18 for vboxnetadp.ko
is not newer than what is already found in kernel 4.18.10-arch1-1-ARCH (5.2.97).
You may override by specifying --force.
Error! Module version 5.2.18 for vboxpci.ko
is not newer than what is already found in kernel 4.18.10-arch1-1-ARCH (5.2.97).
You may override by specifying --force.
```



​	

