# Server

## Class SocketServer
### Bibliotecas

- Socket, possibilita a montagem e configuração do socket de rede.
```py
from socket import *
```

- Thread, possibilita o servidor comunicar com mais de um cliente ao mesmo tempo na rede.
```py
from _thread import start_new_thread
```

- OS, possibilita acessar funcionalidades do sistema (ex:. Pastas, Limpar terminal, Etc).
```py
from os import walk, system, path
```

- Time, possibilita pausar o sistema, utilizado para poder ter intervalos entre as mensagens enviadas.
```py
from time import sleep
```

### Funcionamento

#### Construtor da classe

- Inicializa a configuração do socket com o host e a porta que o servidor irá rodar;
- O host pode ser alterado pelo ip, possibilitando conexão entre outros dispositivos.

```py
def __init__(self, host='localhost', port=55552):
    self.setup(host, port)
```

#### Configuração do Socket

- Configura o socket com um protocolo TCP.

```py
def setup(self, host: str, port: int):
    self.socket = socket(AF_INET, SOCK_STREAM)
    try:
        self.socket.bind((host, port))
        print('Servidor ligando')
        sleep(1)
        system('clear')
        print('Servidor aguardando conexão ...')
        print(f'{host}:{port}')
    except:
        print('Erro ao ligar o servidor!')
        exit()
    self.socket.listen(1)
```

#### Inicializar Servidor

- Aguarda a conexão de um cliente;
- Caso o programa seja encerrado, imprimirá mensagem avisando o desligamento do Server;
- Ao iniciar a conexão inicia uma nova Thread para o Client.

```py
def startServer(self):
    while True:
        try:
            clientSocket, clientAdress = self.socket.accept()
            start_new_thread(self.new_client,(clientSocket, clientAdress))
        except KeyboardInterrupt:
            print('\nDesligando servidor ...')
            self.socket.close()
            exit()
```

#### Conexão com Client

- Informa o endereço e porta do cliente conectado;
- Aguarda mensagem do protocolo de aplicação para iniciar troca de informações.

```py
def new_client(self, clientSocket, clientAdress):
    print (f'Novo cliente {clientAdress[0]}:{clientAdress[1]}')
    while True:
        message = clientSocket.recv(1024).decode()
        sleep(0.05)
        
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
```

#### Genomas catalogados

- Percorre os elementos presentes na pasta './database/' e os coloca em uma lista;
- Envia para o client seu tamanho;
- Se não existir nenhum elemento encerra;
- Envia o nome de seus elementos para o client.

```py
def get_items(self, socket):
    filenames = [filenames for (_, _, filenames) in walk('./database')][0]
    filenames = [item.replace('.fasta', '') for item in filenames]
    length = len(filenames)
    socket.send(str(length).encode())
    sleep(0.05)
    
    if not length:
        return
    
    for item in filenames:
        socket.send(item.encode())
        sleep(0.05)
```

#### Baixar genoma

- Recebe o nome e o status do client;
- Status consiste em uma flag informando se o usuário ja possui o arquivo 'over';
- Caso exista (overwriting) finalizamos;
- Então abrimos o arquivo de maneira binária e enviamos linha por linha;
- Ao finalizar enviamos uma flag para encerrar 'stop'.

```py
def get_file(self, socket):
    name = socket.recv(1024).decode()
    sleep(0.05)
    
    status = socket.recv(1024).decode()
    sleep(0.05)
    
    if status == 'over':
        return
        
    with open(f'./database/{name}.fasta', 'rb') as arq:
        while True:
            line = arq.read(1024)
            socket.send(line)
            sleep(0.05)
            if not line:
                socket.send(b'stop')
                break
```

#### Cadastrar genoma

- Recebemos o nome do genoma que devemos catalogar;
- Se o genoma ja estiver catalogado enviamos uma flag informando e encerramos;
- Abrimos um arquivo binário com seu nome em modo de escrita e escrevemos linha por linha, caso receba a flag 'stop' finalizamos.

```py
def set_file(self, socket):
    name = socket.recv(1024).decode()
    sleep(0.05)

    if path.exists(f'./database/{name}.fasta'):
        socket.send(b'over')
        sleep(0.05)
        return
    else:
        socket.send(b'Ok')
        sleep(0.05)

    with open(f'./database/{name}.fasta', 'wb') as arq:
        while True:
            data = socket.recv(1024)
            sleep(0.05)
            if data == b'stop':
                break
            arq.write(data)
```

## Main
```py
from interface.socketServer import *

if __name__ == '__main__':
    server = SocketServer()
    server.startServer()
```