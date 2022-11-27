from socket import *
import os
import pickle as pc
import struct as st

class SocketServer:
    def __init__(self, host = 'localhost', port = 6666):
        self.db_dir = os.path.curdir + '/database/'
        self.setup(host, port)
        
    def setup(self, host: str, port: int):
        self.socket = socket()
        try:
            self.socket.bind((host, port))
        except:
            print('Erro ao ligar o servidor!')
            exit()
        self.socket.listen()
        print('Server ready')
        
    def startServer(self):
        
        while True:
            connection_, _ = self.socket.accept()
            message = connection_.recv(1024).decode()
            
            if message == 'get_items':
                self.get_items(connection_)
            elif message == 'set_file':
                pass
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
                socket.send(lenght)
                lenght = arq.read(1024)