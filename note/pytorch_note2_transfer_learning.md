# pytorch_note2_transfer_learning

​	Finetuning the convnet：用已有的网络的参数取代随机初始化，后续训练不变。

​	ConvNet as fixed feature extractor：把除了尾部全连接部分的部分当作一个特征提取器，只训练后面全连接的部分。