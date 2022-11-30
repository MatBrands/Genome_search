from socket import *
import pickle as pc
import struct as st
from time import sleep

class SocketClient:
    def __init__(self, host=gethostbyname(gethostname()), port=55552):
        self.setup(host, port)

    def setup(self, host: str, port: int):
        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.socket.connect((host, port))
        except ConnectionRefusedError:
            print('Servidor não encontrado')
            exit()

    def get_items(self, arg='get_items'):
        self.socket.send(arg.encode())
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

        return pc.loads(items)

    def get_file(self, name: str, arg='get_file'):
        self.socket.send(arg.encode())
        sleep(0.01)
        
        self.socket.send(name.encode())
        sleep(0.01)
        
        with open(f'./storage/{name}.fasta', 'wb') as arq:    
            while True:
                data = self.socket.recv(1024)
                sleep(0.01)
                if data == b'stop':
                    break
                arq.write(data)

    def set_file(self, name, genoma, arg='set_file'):
        self.socket.send(arg.encode())
        sleep(0.01)

        self.socket.send(name.encode())
        sleep(0.01)

        with open(f'./storage/{genoma}.fasta', 'rb') as arq:
            while True:
                line = arq.read(1024)
                self.socket.send(line)
                sleep(0.01)
                if not line:
                    self.socket.send(b'stop')
                    break
        
    def close(self, arg='close'):
        self.socket.send(arg.encode())
        self.socket.close()