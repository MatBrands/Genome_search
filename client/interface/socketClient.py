from socket import *
from os import path
from time import sleep

class SocketClient:
    def __init__(self, host=gethostname(), port=55552):
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
        sleep(0.05)
        
        length = int(self.socket.recv(1024).decode())
        sleep(0.05)
        
        result = []
        if length:
            for _ in range (length):
                result.append(self.socket.recv(1024).decode())
                sleep(0.05)
        return result

    def get_file(self, name: str, arg='get_file'):
        self.socket.send(arg.encode())
        sleep(0.05)
        
        self.socket.send(name.encode())
        sleep(0.05)
        
        if path.exists(f'./storage/{name}.fasta'):
            self.socket.send(b'over')
            sleep(0.05)
            input('Erro ! Arquivo ja existe')
            return
        else:
            self.socket.send(b'Ok')
            sleep(0.05)
            
        with open(f'./storage/{name}.fasta', 'wb') as arq:    
            while True:
                data = self.socket.recv(1024)
                sleep(0.05)
                if data == b'stop':
                    break
                arq.write(data)
                
        input(f'Download do genoma {name} foi um sucesso')

    def set_file(self, name, genoma, arg='set_file'):
        self.socket.send(arg.encode())
        sleep(0.05)

        self.socket.send(name.encode())
        sleep(0.05)

        status = self.socket.recv(1024).decode()
        sleep(0.05)
        
        if status == 'over':
            input(f'Erro {genoma} ja esta cadastrado')
            return

        with open(f'./storage/{genoma}.fasta', 'rb') as arq:
            while True:
                line = arq.read(1024)
                self.socket.send(line)
                sleep(0.05)
                if not line:
                    self.socket.send(b'stop')
                    break
        input(f'Genoma {genoma} foi cadastrado')
        
    def close(self, arg='close'):
        self.socket.send(arg.encode())
        self.socket.close()