# Client

## Class Menu
Como o foco do trabalho foi o estudo e implementação da biblioteca Sockets e suas funcionalidades, falaremos muito brevemente sobre o funcionamento desta classe.

- Responsável pela interatividade do terminal;
- Recebe como parâmetros o titulo a ser exibido e os itens do seu menu;

Podemos percorrer os itens do menu com as setas do teclado e escolhermos com o 'Enter'.

## Class SocketClient

### Bibliotecas

- Socket, possibilita a montagem e configuração do socket de rede.
```sh
from socket import *
```

- OS, possibilita acessar funcionalidades do sistema (ex:. Pastas, Limpar terminal, Etc).
```sh
from os import path
```

- Time, possibilita pausar o sistema, utilizado para poder ter intervalos entre as mensagens enviadas.
```sh
from time import sleep
```

### Funcionamento

#### Construtor da classe

- Inicializa a configuração do socket com o host e a porta que o cliente irá conectar.

```sh
def __init__(self, host=gethostbyname(gethostname()), port=55552):
    self.setup(host, port)
```

#### Configuração do Socket

- Configura o socket para se conectar ao servidor.

```sh
def setup(self, host: str, port: int):
    self.socket = socket(AF_INET, SOCK_STREAM)
    try:
        self.socket.connect((host, port))
    except ConnectionRefusedError:
        print('Servidor não encontrado')
        exit()
```

#### Obter os genomas do server

- Envia a mensagem do protocolo de aplicação para iniciar a operação;
- Recebemos o tamanho dos itens catalogados;
- Criamos uma lista e adicionamos seus elementos;
- Retornamos essa lista.

```sh
def get_items(self, arg='get_items'):
    self.socket.send(arg.encode())
    sleep(0.05)
    
    length = int(self.socket.recv(1024).decode())
    sleep(0.05)
    
    result = []
    if length:
        for _ in range (length):
            result.append(self.socket.recv(1024).decode())
            sleep(0.05)
    return result
```

#### Download do genoma

- Envia a mensagem do protocolo de aplicação para iniciar a operação;
- Envia o nome do genoma a ser baixado;
- Se o cliente ja tiver o arquivo envia uma flag 'over' e encerra o método;
- Então abrimos o arquivo de maneira binária e enviamos linha por linha;
- Ao finalizar enviamos uma flag para encerrar 'stop'.

```sh
def get_file(self, name: str, arg='get_file'):
    self.socket.send(arg.encode())
    sleep(0.05)
    
    self.socket.send(name.encode())
    sleep(0.05)
    
    if path.exists(f'./storage/{name}.fasta'):
        self.socket.send(b'over')
        sleep(0.05)
        input('Erro ! Arquivo ja existe')
        return
    else:
        self.socket.send(b'Ok')
        sleep(0.05)

    with open(f'./storage/{name}.fasta', 'wb') as arq:    
        while True:
            data = self.socket.recv(1024)
            sleep(0.05)
            if data == b'stop':
                break
            arq.write(data)
            
    input(f'Download do genoma {name} foi um sucesso')
```

#### Upload do genoma

- Envia a mensagem do protocolo de aplicação para iniciar a operação;
- Recebe o nome e o status do server;
- Status consiste em uma flag 'over' informando se o genoma ja está catalogado;
- Caso exista (overwriting) finalizamos;
- Então abrimos o arquivo para leitura binária e enviamos linha por linha;
- Ao finalizar enviamos uma flag para encerrar 'stop'.

```sh
def set_file(self, name, genoma, arg='set_file'):
    self.socket.send(arg.encode())
    sleep(0.05)

    self.socket.send(name.encode())
    sleep(0.05)

    status = self.socket.recv(1024).decode()
    sleep(0.05)
    
    if status == 'over':
        input(f'Erro {genoma} ja esta cadastrado')
        return

    with open(f'./storage/{genoma}.fasta', 'rb') as arq:
        while True:
            line = arq.read(1024)
            self.socket.send(line)
            sleep(0.05)
            if not line:
                self.socket.send(b'stop')
                break
    input(f'Genoma {genoma} foi cadastrado')
```

#### Finaliza a conexão

- Envia a mensagem do protocolo de aplicação para iniciar a operação;
- Encerra a conexão do socket.

```sh
def close(self, arg='close'):
    self.socket.send(arg.encode())
    self.socket.close()
```

## Main

Utilizamos diversas telas de menus para selecionar as informações que desejamos enviar para o servidor.