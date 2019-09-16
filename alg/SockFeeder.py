import socket
from time import sleep
from Serialization import Serialization as ser
from params import *

class SockFeeder(object):

    def __init__(self, alg_name):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.alg = alg_name
        self.sock.bind(('', op_map[alg_name][1]))
        self.sock.listen(1)
        pass

    def connect(self):
        print('Waiting for connection ...')
        self.c_sock, self.c_addr = self.sock.accept()
        self.c_sock.settimeout(3.0)
        print('Connected: {}.'.format(self.c_addr))
        return self.c_sock

    def reconnect(self):
        try:
            print('Broken pipe! Reconnecting ...')
            self.c_sock.close()
        finally:
            self.c_sock, self.c_addr = self.sock.accept()
            self.c_sock.settimeout(3.0)
            print('Connected: {}.'.format(self.c_addr))
        pass

    def get(self, num=1):
        results, _brokens, _collected = list(), 0, 0
        while _collected < num:
            buffer = self.c_sock.recv(8192)
            if len(buffer) == 0:
                self.reconnect()
                continue

            try:
                buffer = ser.restore(buffer)
                results.append(buffer)
                _collected += 1
            except Exception as e:
                _brokens += 1
            pass
        return _brokens, results

    pass