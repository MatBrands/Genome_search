from socket import *
import pickle
import os

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
            filenames = self.get_items()
            # Enviar elementos
            pass

        elif message.decode() == 'set_file':
           pass
            
        elif message.decode() == 'get_file':
            pass

        connect.close()
        
    def get_items():
        filenames = [filenames for (_, _, filenames) in os.walk(os.path.curdir + '/database')][0]
        filenames = [item.replace('.fasta', '') for item in filenames]
        return filenames