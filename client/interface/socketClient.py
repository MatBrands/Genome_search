from socket import *
import pickle as pc
import struct as st
import os
import time


class SocketClient:
    def __init__(self, host='localhost', port=6666):
        self.db_dir = os.path.curdir + '/'
        self.host = host
        self.port = port

    def setup(self, host: str, port: int):
        self.socket = socket()
        self.socket.connect((host, port))

    def get_items(self):
        self.setup(self.host, self.port)
        self.socket.send(b'get_items')

        data = b''
        payload_size = st.calcsize('i')

        while len(data) < payload_size:
            data += self.socket.recv(1024 * 100)

        packed_message_size = data[:payload_size]
        data = data[payload_size:]
        message_size = st.unpack('i', packed_message_size)[0]

        while len(data) < message_size:
            data += self.socket.recv(1024 * 100)

        items = data[:message_size]
        data = data[message_size:]

        self.socket.close()

        return pc.loads(items)

    def get_file(self, name: str):
        self.setup(self.host, self.port)
        self.socket.send(b'get_file')
        time.sleep(0.01)
        with open(name + '.fasta', 'wb') as arq:
            self.socket.send(name.encode())
            data = True
            while data:
                time.sleep(0.01)
                data = self.socket.recv(1024)
                arq.write(data)

        self.socket.close()

    def set_file(self, name, arq_path):
        if not os.path.exists(self.db_dir + arq_path + '.fasta'):
            input('Arquivo não existe')
            return
        self.setup(self.host, self.port)
        self.socket.send(b'set_file')
        time.sleep(0.01)
        with open(self.db_dir + arq_path + '.fasta', 'rb') as arq:
            self.socket.send(name.encode())
            lenght = arq.read(1024)
            while lenght:
                time.sleep(0.01)
                self.socket.send(lenght)
                lenght = arq.read(1024)

        self.socket.close()