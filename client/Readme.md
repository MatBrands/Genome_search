# Client

## Class Menu
Como o foco do trabalho foi o estudo e implementação da biblioteca Sockets e suas funcionalidades, falaremos muito brevemente sobre o funcionamento desta classe.

- Responsável pela interatividade do terminal;
- Recebe como parâmetros o titulo a ser exibido e os itens do seu menu;

Podemos percorrer os itens do menu com as setas do teclado e escolhermos com o 'Enter'.

## Class SocketClient

### Bibliotecas

- Socket, possibilita a montagem e configuração do socket de rede.
```py
from socket import *
```

- OS, possibilita acessar funcionalidades do sistema (ex:. Pastas, Limpar terminal, Etc).
```py
from os import path
```

- Time, possibilita pausar o sistema, utilizado para poder ter intervalos entre as mensagens enviadas.
```py
from time import sleep
```

### Funcionamento

#### Construtor da classe

- Inicializa a configuração do socket com o host e a porta que o cliente irá conectar.

```py
def __init__(self, host='localhost', port=55552):
    self.setup(host, port)
```

#### Configuração do Socket

- Configura o socket para se conectar ao servidor.

```py
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

```py
def get_items(self, arg='get_items'):
    self.socket.send(arg.encode())
    sleep(0.1)
    
    length = int(self.socket.recv(1024).decode())
    sleep(0.1)
    
    result = []
    if length:
        for _ in range (length):
            result.append(self.socket.recv(1024).decode())
            sleep(0.1)
    return result
```

#### Download do genoma

- Envia a mensagem do protocolo de aplicação para iniciar a operação;
- Envia o nome do genoma a ser baixado;
- Se o cliente ja tiver o arquivo envia uma flag 'over' e encerra o método;
- Então abrimos o arquivo de maneira binária e enviamos linha por linha;
- Ao finalizar enviamos uma flag para encerrar 'stop'.

```py
def get_file(self, name: str, arg='get_file'):
    self.socket.send(arg.encode())
    sleep(0.1)
    
    self.socket.send(name.encode())
    sleep(0.1)
    
    if path.exists(f'./storage/{name}.fasta'):
        sleep(0.1)
        self.socket.send(b'over')
        sleep(0.1)
        input('Erro ! Arquivo ja existe')
        return
    
    self.socket.send(b'Ok')
    sleep(0.1)

    with open(f'./storage/{name}.fasta', 'wb') as arq:    
        while True:
            data = self.socket.recv(1024)
            sleep(0.1)
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

```py
def set_file(self, name, genoma, arg='set_file'):
    self.socket.send(arg.encode())
    sleep(0.1)

    self.socket.send(name.encode())
    sleep(0.1)

    status = self.socket.recv(1024).decode()
    sleep(0.1)
    
    if status == 'over':
        input(f'Erro {genoma} ja esta cadastrado')
        return

    with open(f'./storage/{genoma}.fasta', 'rb') as arq:
        while True:
            line = arq.read(1024)
            self.socket.send(line)
            sleep(0.1)
            if not line:
                self.socket.send(b'stop')
                break
    input(f'Genoma {genoma} foi cadastrado')
```

#### Finaliza a conexão

- Envia a mensagem do protocolo de aplicação para iniciar a operação;
- Encerra a conexão do socket.

```py
def close(self, arg='close'):
    self.socket.send(arg.encode())
    self.socket.close()
```

## Main

#### Definir os parametros do menu

- Definimos o titulo e itens para percorrer no menu.

```py
def parametros_menu(titulo: list, itens: list):
    menu = Menu()
    menu.setTitulo(titulo)
    menu.setItems(itens)
    option = menu.iniciarMenu()
    return option
```

#### Main, Menu inicial

- Inicializa o SocketClient()
- Menu principal
<div style="line-height: 2;">
    <ol>
        <li>Redireciona para o menu de observar/download do genoma;</li>
        <li>Redireciona para cadastro de genoma;</li>
        <li>Finaliza a conexão.</li>
    </ol>
</div>

```py
if __name__ == '__main__':
    client_socket = SocketClient()

    while True:
        try:
            menu_item = parametros_menu(['Selecione uma opção: '], ['Buscar genoma (Download)', 'Cadastrar genoma (Upload)', 'Sair'])
            if menu_item == 0:
                menu_genoma(client_socket)
            elif menu_item == 1:
                cadastrar_genoma(client_socket)
            else:
                client_socket.close()
                break
        except KeyboardInterrupt:
            client_socket.close()
            system('clear')
            exit()
```

#### Menu de observação do genoma

- Pede a lista de itens catalogados no database através do protocolo 'get_items()'.
<div style="line-height: 2;">
    <ol>
        <li>Demonstra os genomas catalogados;</li>
        <li>Pede para o usuário fazer uma busca (tentando assemelhar ao buscador Google);</li>
        <li>Retorna ao menu anterior (Principal).</li>
    </ol>
</div>

```py
def menu_genoma(socket):
    list_of_items_db = socket.get_items()
    itens = ['Observar genomas catalogados', 'Busca e download de genoma', 'Retornar']
    while True:
        menu_item = parametros_menu(['Selecione uma opção:'], itens)
        if menu_item == 0:
            print('Todos os genomas catalogados: ')
            for item in list_of_items_db:
                print(item)
            input('Digite qualquer tecla para retornar')
        elif menu_item == 1:
            name = input('Digite o nome científico ou o popular: \n')
            buscar_genoma(socket, name, list_of_items_db)
            return
        else:
            return
```

#### Download do genoma

- A partir do nome buscamos associar as especies correspondentes;
- Se não achar informa e cancela;
- Então vc pode percorrer para fazer o download através do protocolo 'get_file()';
- Caso não queira pode retornar.

```py
def buscar_genoma(socket, name, list_of_items_db):
    resultado = []
    for item in list_of_items_db:
        if name in item:
            resultado.append(item)

    if not resultado:
        input('Espécie não catalogada')
        return

    resultado.append('Retornar')
    menu_item = parametros_menu(['Selecione o genoma para download: '], resultado)

    if menu_item != len(resultado) - 1:
        socket.get_file(resultado[menu_item])
```

#### Cadastro de genoma

- Pede os dados da espécie, caso não sejam informados ocorre um erro;
- Caso não exista um arquivo .fasta na pasta '/storage' informará erro;
- Então através do protocolo 'set_file()' cataloga a espécie.

```py
def cadastrar_genoma(socket):
    nome_especie = input('Digite o nome científico da espécie\n')
    if not nome_especie:
        input('Erro ! Entrada inválida, tecle para sair ...\n')
        return
    nome_popular = input('Digite o nome popular da espécie\n')
    if not nome_popular:
        input('Erro ! Entrada inválida, tecle para sair ...\n')
        return
    
    filenames = [filenames for (_, _, filenames) in os.walk('./storage/')][0]
    filenames = [item.replace('.fasta', '') for item in filenames]
    
    if not filenames:
        input('Erro ! Não existem arquivos para catalogar, tecle para sair ...\n')
        return
    filenames.append('Retornar')
    
    nome = f'{nome_especie}: {nome_popular}'
    genoma_especie = parametros_menu(['Selecione o arquivo que deseja enviar:'], filenames)
    genoma_especie = filenames[genoma_especie]
    
    if genoma_especie == 'Retornar':
        return
    
    socket.set_file(nome, genoma_especie)
```