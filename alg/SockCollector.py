import socket
from sys import argv
from time import sleep
from itertools import cycle
from alg.Serialization import Serialization as ser
from alg.params import *

import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from sklearn import datasets

class SockCollector(object):
    def __init__(self, op_code):
        self.alg = op_code
        self.data = list()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect( op_map[op_code] )
        pass

    def load_data(self):
        if self.alg=='svm':         #NOTE: load dataset for SVM jobs
            digits = datasets.load_digits()
            n_samples = len(digits.images)
            shaped_images = digits.images.reshape((n_samples, -1))
            return zip(shaped_images, digits.target) #FIXME: pick a random subset
        elif self.alg=='idpa':      #NOTE: load dataset for IDPA jobs
            (x_train, y_train), (x_test, y_test) = mnist.load_data()
            x_train = np.reshape(x_train/255.0, (60000, 784))
            y_train = tf.keras.utils.to_categorical(y_train, 10)
            return zip(x_train, y_train)
        else:
            return -1
        pass

    def reconnect(self):
        try:
            self.sock.close()
        finally:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect( op_map[self.alg] )
        pass

    def send(self, obj):
        _len, _buffer = ser.dump(obj)
        while self.sock.send(_buffer) < _len:
            self.reconnect()
        pass

def main():
    if len(argv) < 2:
        print('No Dataset Specified!')
        exit()
    
    op_code = argv[2]
    try:
        sc = SockCollector(op_code)
        dataset = sc.load_data()
        for sample in cycle(dataset):
            sc.send(sample)
            sleep(1.0) #FIXME: fairly sleep for lower rate
            pass
    except Exception as e:
        print('No "%s" dataset!'%argv[2])
        raise(e)
        pass
    pass

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise(e) #print(e)
    finally:
        exit()