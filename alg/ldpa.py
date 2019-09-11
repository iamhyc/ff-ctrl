# View more python tutorial on my Youtube and Youku channel!!!

# Youtube video tutorial: https://www.youtube.com/channel/UCdyjiB5H8Pu7aDTNVXTTpcg
# Youku video tutorial: http://i.youku.com/pythontutorial

"""
Please note, this code is only for python 3+. If you are using python 2+, please modify the code accordingly.
"""

from __future__ import print_function

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import math, time
import numpy as np
#from tensorflow.examples.tutorials.mnist import input_data
# number 1 to 10 data
# mnist = input_data.read_data_sets('data/fashion', one_hot=True)
from alg.SockFeeder import SockFeeder

# little modification
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0
x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)

y_train = tf.keras.utils.to_categorical(y_train,10) # with label dimensions
y_test = tf.keras.utils.to_categorical(y_test,10)  # with label dimensions


def compute_accuracy(v_xs, v_ys):
    global prediction
    y_pre = sess.run(prediction, feed_dict={xs: v_xs, keep_prob: 1})
    correct_prediction = tf.equal(tf.argmax(y_pre,1), tf.argmax(v_ys,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={xs: v_xs, ys: v_ys, keep_prob: 1})
    return result

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    # stride [1, x_movement, y_movement, 1]
    # Must have strides[0] = strides[3] = 1
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    # stride [1, x_movement, y_movement, 1]
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

# define placeholder for inputs to network
xs = tf.placeholder(tf.float32, [None, 784])/255.   # 28x28
ys = tf.placeholder(tf.float32, [None, 10])
keep_prob = tf.placeholder(tf.float32)
x_image = tf.reshape(xs, [-1, 28, 28, 1])
# print(x_image.shape)  # [n_samples, 28,28,1]

## conv1 layer ##
W_conv1 = weight_variable([5,5, 1,32]) # patch 5x5, in size 1, out size 32
b_conv1 = bias_variable([32])
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1) # output size 28x28x32
h_pool1 = max_pool_2x2(h_conv1)                                         # output size 14x14x32

## conv2 layer ##
W_conv2 = weight_variable([5,5, 32, 64]) # patch 5x5, in size 32, out size 64
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2) # output size 14x14x64
h_pool2 = max_pool_2x2(h_conv2)                                         # output size 7x7x64

## fc1 layer ##
W_fc1 = weight_variable([7*7*64, 128])
b_fc1 = bias_variable([128])
# [n_samples, 7, 7, 64] ->> [n_samples, 7*7*64]
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

## fc2 layer ##
W_fc2 = weight_variable([128, 10])
b_fc2 = bias_variable([10])
prediction = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

# number of parameters: (5*5+1)*32+(5*5*32+1)*64+(7*7*64+1)*1024+(1024+1)*10

# the error between prediction and real data
cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction),
                                              reduction_indices=[1]))       # loss
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

start_time = time.time()

sess = tf.Session()
# important step
# tf.initialize_all_variables() no long valid from
# 2017-03-02 if using tensorflow >= 0.12

###################### Main Section ######################
sf = SockFeeder('idpa')
while sf.connect() < 0:
    time.sleep(1.0) #retry until connected

while True:
    results = sf.get(num=1) #blocking, until get $num samples
    #TODO: 把下面的复制过来并且可以work
    pass

size_vec =[1553,1367,1245,1484,1336,1486,1077,1487,1423,1898] #NOTE: random index
acc_vec=np.ones(10)*0.1
for j in range(10):
    while acc_vec[j]<0.2 and size_vec[j]>1:
        if int((tf.__version__).split('.')[1]) < 12 and int((tf.__version__).split('.')[0]) < 1:
            init = tf.initialize_all_variables()
        else:
            init = tf.global_variables_initializer()
        sess.run(init)
    
        size=size_vec[j]
        num_mini = math.ceil(size/100)
        batch_xs = x_train[size*0:size*1]
        batch_ys = y_train[size*0:size*1]
        num_epochs = math.ceil(5000/num_mini)
        for epoch in range(num_epochs):
            for i in range(num_mini):
                sess.run(train_step, feed_dict={xs: batch_xs[100*(i):100*(i+1)], 
                                    ys: batch_ys[100*(i):100*(i+1)],
                                    keep_prob: 0.5})
    
        # sess.run(train_step, feed_dict={xs: batch_xs, ys: batch_ys, keep_prob: 0.5}) 
        #if epoch == num_epochs-100:
#            print(compute_accuracy(
#                   x_test[:1000], y_test[:1000]))
        
        acc_vec[j]=compute_accuracy(x_test[:1000], y_test[:1000])
        if acc_vec[j]>0.2:
            print(acc_vec[j])

#NOTE: your code
elapsed_time = time.time() - start_time
print(elapsed_time)
print('finish')
print(acc_vec)
print(sum(acc_vec)/10)