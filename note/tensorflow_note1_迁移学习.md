# tensorflow_note1_迁移学习

​	利用已训练好的神经网络模型进行微调来解决自己的问题，迁移学习的原因有二：

​	（1）、计算机性能有限，对于家里没有矿，相关比赛时间也不长的学生，计算机的性能有限，很多网络模型是不能自己训练出来的。

​	（2）、时间有限，一个庞大的模型需要训练几天甚至更久。

​	其中微调就是针对那些VGG16之类的多层深度学习网络，固定大部分参数，只对几层甚至一层进行参数训练



### 训练准备-数据“注册”

​	



### 开始训练-文件结构

​	下载tensorflow的[models](http://github.com/tensorflow/models.git)，使用其中的slim，这是一个很方便的微调模型。

```
slim/
	satellite/
		train_dir/
			训练过程中的日志和模型
		data/
			训练数据.tfrecord
			验证数据.tfrecord
		pretrained/
			别人训练的模型.ckpt
	
```

​	使用slim下面的微调程序，一大串参数都不能少

```bash
python train_image_classifier.py \
 --train_dir=satellite/train_dir \
 --dataset_name=satellite \
 --dataset_split_name=train \
 --dataset_dir=satellite/data \
 --model_name=inception_v3 \
 --checkpoint_path=satellite/pretrained/inception_v3.ckpt \
 --checkpoint_exclude_scorpes=InceptionV3/Logits,InceptionV3/AuxLogits \
 --trainable_scorpes=InceptionV3/Logits,InceptionV/AuxLogits \
 --batch_size=32 \
 --learning_rate=0.001 \
 --learning_rate_decay_type=fixed \
 --save_interval_secs=300 \
 --save_summaries_secs=2 \
 --log_every_n_steps=10 \
 --optimizer=rmsprop \
 --weight_decay=0.00004				
```

​	PS：以后自己写模型，写计算图的时候，可能也会需要上面这些超参数。