# tensorlfow_note0_查看电脑的GPU

	

	GPU即图形处理器几条基本命令可以得知自己电脑上GPU的相关信息。

```bash
lspci |grep -i nvidia
```

​	英伟达送了一个动态监视显存的工具，如果它说无法与GPU交流……那就重装一次嘿嘿嘿

```bash
sudo pacman -S nvidia
nvidia-smi
```

	

	在创建sess时你可能会得到这种错误报告，

```bash
InvalidArgumentError (see above for traceback): Cannot assign a device for operation ‘InceptionV3/Predictions/Softmax’: Could not satisfy explicit device specification ‘/device:GPU:0’ because no supported kernel for GPU devices is available. 
```

	这应该是因为有的操作不能使用GPU，不能使用CPU，你需要的是一个在GPU不可用的时候选用CPU的策略，创建sess的时候应该使用这一句。

```python
sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True, log_device_placement=True))
```

