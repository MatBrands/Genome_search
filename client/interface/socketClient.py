from socket import *
import pickle as pc
import struct as st
import os
import time


class SocketClient:
    def __init__(self, host=gethostbyname(gethostname()), port=55552):
        self.db_dir = os.path.curdir + '/'
        self.host = host
        self.port = port
        self.db_server = '../../server/database'

    def setup(self, host: str, port: int):
        self.socket = socket(AF_INET, SOCK_STREAM)

        try:
            self.socket.connect((host, port))
            return True
        except ConnectionRefusedError:
            return False

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
        with open(f'../client_storage/{name}.fasta', 'w') as arq:
            self.socket.send(name.encode())
            data = True
            while data:
                time.sleep(0.01)
                data = self.socket.recv(1024).decode()
                arq.write(data)

        self.socket.close()

    def set_file(self, name, genoma):
        self.socket.send(b'set_file')

        time.sleep(1)

        self.socket.send(name.encode())

        time.sleep(1)

        self.socket.send(genoma.encode())
        self.socket.close()
