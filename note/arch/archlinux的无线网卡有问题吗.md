# 2018-07-07

  ## ss

​	今天购买了banwagong的代理，开始配置ss，并且处理了一直以来的上网问题。

`sudo systemctl start shadowsocks@XXXX.service `可以激活代理服务。

## wifi  

​	

​	这一篇给自己留作记录。使用archlinux在使用wifi-menu时发生了报错:

```bash
Job for netctl@wlp3s0\x2dUniqueStudio\x2d810.service failed because the control process exited with error code.
See "systemctl status "netctl@wlp3s0\x2dUniqueStudio\x2d810.service"" and "journalctl -xe" for details.
```

​	似乎是ip和netctl发生冲突导致的，使用：

`ip link set (服务名) down` 

​	再使用 

`netctl start (服务名-ssid)`

​	最后成功连上wifi。