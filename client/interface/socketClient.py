from socket import *
import pickle as pc
import struct as st

class SocketClient:
    def __init__(self, host = 'localhost', port = 6666):
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
            data += self.socket.recv(1024*100)

        packed_message_size = data[:payload_size]
        data = data[payload_size:]
        message_size = st.unpack('i', packed_message_size)[0]

        while len(data) < message_size:
            data += self.socket.recv(1024*100)

        items = data[:message_size]
        data = data[message_size:]
        
        self.socket.close()
        
        return pc.loads(items)
    
    def get_file(self, name: str):
        self.setup(self.host, self.port)
        self.socket.send(b'get_file')
        
        with open(name + '.fasta', 'wb') as arq:
            self.socket.send(name.encode())
            data = 1
            while data:
                data = self.socket.recv(1024)
                arq.write(data)

        self.socket.close()
        