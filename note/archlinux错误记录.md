# archlinux错误记录

## git

​	[gitdownload](https://minhaskamal.github.io/DownGit/#/home)可以下载特定文件，只要输入连接就行。

## virtualbox

### 1、内核消失错误

​	FATAL显示一个十分重要的内核没了`vboxdrv`，没有这个内核，虚拟机是无法启动的。

​	据说需要更新系统的`heard`文件，所以安装一下`linux-headers`这个包，就解决了这个问题。

### 2、

```bash
➜  ~ virtualbox
Qt FATAL: FATAL: The application binary appears to be running setuid, this is a security hole.
[1]    1533 abort      virtualbox
```

​	

