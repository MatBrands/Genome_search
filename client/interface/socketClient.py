from socket import *
import pickle as pc
import struct as st

class SocketClient:
    def __init__(self, host='localhost', port=6666):
        self.setup(host, port)

    def setup(self, host: str, port: int):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((host, port))
        
    def get_items(self):
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
