from socket import *
import os
import pickle as pc
import struct as st
from time import *

class SocketServer:
    def __init__(self, host=gethostbyname(gethostname()), port=55552):
        self.setup(host, port)

    def setup(self, host: str, port: int):
        self.socket = socket(AF_INET, SOCK_STREAM)

        try:
            self.socket.bind((host, port))
            print('Servidor ligando')
            sleep(1)
            os.system('clear')
            print('Servidor aguardando conexão ...')
        except:
            print('Erro ao ligar o servidor!')
            exit()

        self.socket.listen()

    def startServer(self):
        self.setup(host=gethostbyname(gethostname()), port=55552)

        while True:
            connection_, addr = self.socket.accept()
            print(f'Cliente: {addr} conectado')
            message = connection_.recv(1024).decode()
            sleep(0.01)
            
            if message == 'get_items':
                self.get_items(connection_)
            elif message == 'set_file':
                self.set_file(connection_)
            elif message == 'get_file':
                self.get_file(connection_)

            connection_.close()

    def get_items(self, socket):
        filenames = [filenames for (_, _, filenames) in os.walk('./database')][0]
        filenames = [item.replace('.fasta', '') for item in filenames]
        data = pc.dumps(filenames)
        message_size = st.pack('i', len(data))
        socket.send(message_size + data)
        sleep(0.01)

    def get_file(self, socket):
        name = socket.recv(1024).decode()
        sleep(0.01)
        
        with open(f'./database/{name}.fasta', 'rb') as arq:
            while True:
                line = arq.read(1024)
                if not line:
                    break
                socket.send(line)
                sleep(0.01)

    def set_file(self, socket):
        name = socket.recv(1024).decode()
        sleep(0.01)

        with open(f'./database/{name}.fasta', 'wb') as arq:
            while True:
                data = socket.recv(1024)
                sleep(0.01)
                if not data:
                    break
                arq.write(data)