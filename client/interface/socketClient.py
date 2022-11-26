from socket import *

class SocketClient:
    def __init__(self, host = 'localhost', port = 6666):
        self.setup(host, port)

    def setup(self, host: str, port: int):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((host, port))
        
        