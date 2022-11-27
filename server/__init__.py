from interface.socketServer import *

if __name__ == '__main__':
    server = SocketServer()
    
    while True:
        server.startServer()
