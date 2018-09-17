# coding:utf-8

import glob
import os.path
import random
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile

# Inception-v3瓶颈层的节点个数
BOTTLENECK_TENSOR_SIZE = 2048

# 从数据文件夹中读取所有图片并按照训练、验证、测试分开
def create_images_list(rate_training, rate_test):
""" 把不同的照片文件排成三个随机队列"""
    image_list = []
    is_current_dir = True
    for root, _, files in os.walk(./data):
        if is_current_dir:
            is_current_dir = False
            continue  
        extensions = ['jpg','JPG','jpeg','JPEG']
        for file in files:
            if file.split('.')[-1] in extensions:
                image_list.append(root+"/"+file)
    num_training = int(rate_training/100.0 * len(image_list))
    num_test = int(rate_test/100.0 * len(image_list))
    sample_training_test = random.sample(image_list, num_training+num_test)
    input_list = {}
    input_list[training] = []
    input_list[test] = []
    input_list[validation] = []
    # 随机划分测试集、测试集和验证集
    for image in image_list:
        chance = np.random.randint(100)
        if chance < num_training:
            input_list[training].append(image)
        elif chance < num_training+num_test:
            input_list[test].append(image)
        else
            input_list[validation].append(image)
    return input_list

# 计算一个图片tensor经过Inception-v3处理后的瓶颈值“特征向量”
def run_bottlecheck_on_image(sess, image_data, bottle_tensor):
    bottleneck_values

# 找一个图片的瓶颈值，先查看文件，如果没有就创建一个文件
def get_or_create_bottleneck(sess, image_data):


# 获得随机batch的函数，可以把batch里面的图片都变成“特征向量”

# 主函数
d
#ef main():

if __name__ == "__main__":
    tf.app.run()
