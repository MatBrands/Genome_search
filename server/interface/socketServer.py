from socket import *
from _thread import start_new_thread
from os import walk, system
from time import sleep

class SocketServer:
    def __init__(self, host=gethostbyname(gethostname()), port=55552):
        self.setup(host, port)

    def setup(self, host: str, port: int):
        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.socket.bind((host, port))
            print('Servidor ligando')
            sleep(1)
            system('clear')
            print('Servidor aguardando conexão ...')
        except:
            print('Erro ao ligar o servidor!')
            exit()
        self.socket.listen(1)

    def startServer(self):
        while True:
            clientSocket, clientAdress = self.socket.accept()
            start_new_thread(self.new_client,(clientSocket, clientAdress))

    def new_client(self, clientSocket, clientAdress):
        print (f'Novo cliente {clientAdress[0]}:{clientAdress[1]}')
        while True:
            message = clientSocket.recv(1024).decode()
            sleep(0.01)
            
            if message == 'get_items':
                self.get_items(clientSocket)
            if message == 'set_file':
                self.set_file(clientSocket)
            if message == 'get_file':
                self.get_file(clientSocket)
            if message == 'close':
                break
        print (f'Cliente {clientAdress[0]}:{clientAdress[1]} disconectou ...')
        clientSocket.close()

    def get_items(self, socket):
        filenames = [filenames for (_, _, filenames) in walk('./database')][0]
        filenames = [item.replace('.fasta', '') for item in filenames]
        length = len(filenames)
        socket.send(str(length).encode())
        sleep(0.01)
        
        if not length:
            return
        
        for item in filenames:
            socket.send(item.encode())
            sleep(0.01)
        
    def get_file(self, socket):
        name = socket.recv(1024).decode()
        sleep(0.01)
        with open(f'./database/{name}.fasta', 'rb') as arq:
            while True:
                line = arq.read(1024)
                socket.send(line)
                sleep(0.01)
                if not line:
                    socket.send(b'stop')
                    break

    def set_file(self, socket):
        name = socket.recv(1024).decode()
        sleep(0.01)

        with open(f'./database/{name}.fasta', 'wb') as arq:
            while True:
                data = socket.recv(1024)
                sleep(0.01)
                if data == b'stop':
                    break
                arq.write(data)