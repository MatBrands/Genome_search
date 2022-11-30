from socket import *
from threading import Thread
from os import walk, system
from time import sleep

class ClientThread(Thread):
    def __init__(self, clientSocket, clientAddress):
        Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        print (f'Novo cliente conectado: {clientAddress}')

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
            new_client = ClientThread(clientSocket, clientAdress)
            while True:
                message = new_client.clientSocket.recv(1024).decode()
                sleep(0.01)
                
                if message == 'get_items':
                    self.get_items(new_client.clientSocket)
                if message == 'set_file':
                    self.set_file(new_client.clientSocket)
                if message == 'get_file':
                    self.get_file(new_client.clientSocket)
                if message == 'close':
                    break
            print (f'Cliente {new_client.clientAddress} disconectou ...')
            new_client.clientSocket.close()

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