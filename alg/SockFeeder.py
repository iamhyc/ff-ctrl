import socket
import DataTypes as types

class SockFeeder(object):

    def __init__(self, srv_port, data_type):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = srv_port
        self.sock.bind(('', srv_port))
        self.sock.listen(1)
        pass

    def connect():
        self.c_sock, self.c_addr = self.sock.accept()
        return self.c_sock

    def get(num=1):
        results = list()
        for i in range(num):
            buffer = self.c_sock.recv(1024) #FIXME: fix with real data type
            results.append(buffer) 
        return results

    pass