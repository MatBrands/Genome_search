from socket import *
import os
import pickle as pc
import struct as st
import time

class SocketServer:
    def __init__(self, host=gethostbyname(gethostname()), port=55551):
        self.db_dir = os.path.curdir + '/database/'
        self.setup(host, port)

    def setup(self, host: str, port: int):
        self.socket = socket(AF_INET, SOCK_STREAM)

        try:
            self.socket.bind((host, port))
        except:
            print('Erro ao ligar o servidor!')
            exit()

        print('Servidor Funcionando')
        time.sleep(2)
        os.system("clear")
        print('Servidor aguardando conexão de cliente ...')
        self.socket.listen()


    def startServer(self):
        self.setup(host=gethostbyname(gethostname()), port=55551)

        while True:
            connection_, _ = self.socket.accept()
            message = connection_.recv(1024).decode()

            if message == 'get_items':
                self.get_items(connection_)
            elif message == 'set_file':
                self.set_file(connection_)
            elif message == 'get_file':
                self.get_file(connection_)

            connection_.close()

    def get_items(self, socket):
        filenames = [filenames for (_, _, filenames) in os.walk(self.db_dir)][0]
        filenames = [item.replace('.fasta', '') for item in filenames]
        data = pc.dumps(filenames)
        message_size = st.pack('i', len(data))
        socket.send(message_size + data)

    def get_file(self, socket):
        name = socket.recv(1024).decode()

        with open(self.db_dir + name + '.fasta', 'rb') as arq:
            lenght = arq.read(1024)
            while lenght:
                time.sleep(0.01)
                socket.send(lenght)
                lenght = arq.read(1024)

    def set_file(self, socket):
        name = socket.recv(1024).decode()

        try:
            with open(self.db_dir + name + '.fasta', 'rb') as arq:
                dados = arq.readfile()
        except FileNotFoundError:
            msg = 'Arquivo não existe'
            socket.send(msg.encode())

        with open(self.db_dir + name + '.fasta', 'wb') as arq:
            data = True
            while data:
                time.sleep(0.01)
                data = socket.recv(1024)
                arq.write(data)
