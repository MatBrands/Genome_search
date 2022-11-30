from socket import *
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
        sleep(0.01)
        
        length = int(self.socket.recv(1024).decode())
        sleep(0.01)
        
        result = []
        if length:
            for _ in range (length):
                result.append(self.socket.recv(1024).decode())
                sleep(0.01)
        return result

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