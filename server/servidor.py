import socket
from socket import *
from time import sleep
from os import system


def buscaArquivo(nome_arquivo):
    try:
        with open(f'database/{nome_arquivo}.fasta') as file:
            return file.read()

    except Exception as err:
        return err


if __name__ == '__main__':
    # Utiliza o ip da máquina
    host = gethostbyname(gethostname())
    porta = 55551

    # Com o AF_INET as conexões vão ser aceitas via IPV4, e o SOCK_STREAM é via protocolo TCP
    serverSocket = socket(AF_INET, SOCK_STREAM)

    try:
        # É necessário ligar o soquete ao endereço do servidor
        serverSocket.bind((host, porta))
    except Exception as e:
        print('Erro ao ligar um servidor!')
        exit()

    serverSocket.listen()

    print('Aguarde ...')
    sleep(2)
    system("clear")
    print('Servidor funcionando. Aguardando requisição do usuário...')
    while 1:
        connectionSocket, addr = serverSocket.accept()
        escolha = connectionSocket.recv(1024)

        verbo_http = escolha.decode().split(' ')[0]
        opcao_selecionada = escolha.decode().split(' ')[1]

        if verbo_http == 'GET':
            if opcao_selecionada == '1':
                genoma = buscaArquivo('abelha')
                with open(f'desktop_cliente/abelha_download.fasta', 'w') as file:
                    file.write(genoma)
                mensagem = 'Arquivo baixado com sucesso!'
                print(mensagem)
                connectionSocket.close()
                serverSocket.close()
                break
            if opcao_selecionada == '2':
                genoma = buscaArquivo('cachorro')
                with open(f'desktop_cliente/cachorro_download.fasta', 'w') as file:
                    file.write(genoma)
                print('Arquivo baixado com sucesso!')
                connectionSocket.close()
                serverSocket.close()
                break
            if opcao_selecionada == '3':
                genoma = buscaArquivo('morcego')
                with open(f'desktop_cliente/morcego_download.fasta', 'w') as file:
                    file.write(genoma)
                print('Arquivo baixado com sucesso!')
                connectionSocket.close()
                serverSocket.close()
                break
            if opcao_selecionada == '4':
                genoma = buscaArquivo('panda')
                with open(f'desktop_cliente/panda_download.fasta', 'w') as file:
                    file.write(genoma)
                print('Arquivo baixado com sucesso!')
                connectionSocket.close()
                serverSocket.close()
                break
            if opcao_selecionada == '5':
                genoma = buscaArquivo('pato')
                with open(f'desktop_cliente/pato_download.fasta', 'w') as file:
                    file.write(genoma)
                print('Arquivo baixado com sucesso!')
                connectionSocket.close()
                serverSocket.close()
                break
        elif verbo_http == 'POST':
            nome_especie = connectionSocket.recv(1024)
            genoma = connectionSocket.recv(1024)

            try:
                with open(f'database/{nome_especie.decode()}.fasta', 'w') as file:
                    file.write(genoma.decode())
            except FileExistsError as err:
                resposta = "HTTP 1.1 400"
                connectionSocket.send(resposta.encode())
            resposta = "HTTP 1.1 201"
            connectionSocket.send(resposta.encode())
            connectionSocket.close()
            serverSocket.close()
            break


