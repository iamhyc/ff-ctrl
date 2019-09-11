import socket
from alg.Serialization import Serialization as ser
from alg.params import *

class SockFeeder(object):

    def __init__(self, alg_name):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.alg = alg_name
        self.sock.bind(('', op_map[alg][1]))
        self.sock.listen(1)
        pass

    def connect(self):
        self.c_sock, self.c_addr = self.sock.accept()
        return self.c_sock

    def reconnect(self):
        try:
            self.c_sock.close()
        finally:
            self.c_sock, self.c_addr = self.sock.accept()
        pass

    def get(self, num=1):
        results, _brokens, _collected = list(), 0, 0
        while _collected < num:
            try:
                buffer = self.c_sock.recv(4096)
            except Exception as e:
                self.reconnect()
                continue
            
            try:
                buffer = ser.restore(buffer)
                results.append(buffer)
                _collected += 1
            except Exception as e:
                _brokens += 1
        return _brokens, results

    pass