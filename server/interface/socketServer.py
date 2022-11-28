from socket import *
import os
import pickle as pc
import struct as st
import time

class SocketServer:
    def __init__(self, host=gethostbyname(gethostname()), port=55552):
        self.db_dir = os.path.curdir + '/database/'
        self.setup(host, port)

    def setup(self, host: str, port: int):
        self.socket = socket(AF_INET, SOCK_STREAM)

        try:
            self.socket.bind((host, port))
            print('Servidor Funcionando')
            time.sleep(3)
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

        with open(self.db_dir + name + '.fasta', 'r') as arq:
            lenght = arq.read(1024)
            while lenght:
                time.sleep(0.01)
                socket.send(lenght.encode())
                lenght = arq.read(1024)

    def set_file(self, socket):
        name = socket.recv(1024).decode()

        if os.path.exists(f'{self.db_dir} + {name} + .fasta'):
            exit()

        genoma = socket.recv(1024).decode()

        with open(self.db_dir + name + '.fasta', 'w') as arq:
            arq.write(genoma)
        return 1
