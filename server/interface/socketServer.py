from socket import *
import os
import pickle as pc
import struct as st

class SocketServer:
    def __init__(self, host = 'localhost', port = 6666):
        self.setup(host, port)
        
    def setup(self, host: str, port: int):
        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.socket.bind((host, port))
        except:
            print('Erro ao ligar um servidor!')
            exit()
        self.socket.listen()
        print('Server ready')
        
    def startServer(self):
        connect, _ = self.socket.accept()
        message = connect.recv(1024)

        if message.decode() == 'get_items':
            # Enviar items do db
            self.get_items(connect)

        elif message.decode() == 'set_file':
           pass
            
        elif message.decode() == 'get_file':
            pass

        connect.close()
        
    def get_items(self, socket):
        filenames = [filenames for (_, _, filenames) in os.walk(os.path.curdir + '/database')][0]
        filenames = [item.replace('.fasta', '') for item in filenames]
        data = pc.dumps(filenames)
        message_size = st.pack('i', len(data))
        socket.sendall(message_size + data)
        