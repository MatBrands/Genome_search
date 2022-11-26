from socket import *

class SocketServer:
    def __init__(self, host = 'localhost', port = 6666):
        self.setup(host, port)
        
    def setup(self, host: str, port: int):
        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.socket.bind((host, port))
        except Exception as e:
            print('Erro ao ligar um servidor!')
            exit()
        self.socket.listen()
        print('Server ready')
        
    def startServer(self):
        connect, _ = self.socket.accept()
        message = connect.recv(1024)

        if message.decode() == 'get_items':
            pass

        elif message.decode() == 'set_file':
           pass
            
        elif message.decode() == 'get_file':
            pass

        connect.close()