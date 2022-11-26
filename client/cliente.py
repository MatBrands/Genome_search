from socket import *
from time import sleep
from os import system


if __name__ == '__main__':
    host = gethostname()
    porta = 55551

    clientSocket = socket(AF_INET, SOCK_STREAM)

    try:
        clientSocket.connect((host, porta))
    except ConnectionRefusedError:
        print('Conexão Recusada. Verifique as portas dos serviços')
        exit()
    except Exception as e:
        print('Erro ao ligar um cliente')
        exit()

    opcao = 0
    escolha = -1

    while 1:
        if opcao == 0:
            system("clear")
            print('<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>')
            print('<><><><><><><><><><><><> BANCO DE DADOS PÚBLICO DE GENOMAS <><><><><><><><><><><><><>')
            print('<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>')
            print('Selecione uma opção:')
            print('1 - Baixar o genoma de uma espécie')
            print('2 - Cadastrar um genoma de uma espécie')
            print('3 - Sair')
            try:
                opcao = input('> ')
            except ValueError as err:
                system("clear")
                print('\nSomente valores inteiros\n')
                sleep(2)
            if opcao == '1':
                escolha = 'GET '
                escolha += opcao
            if opcao == '2':
                escolha = 'POST '
                escolha += opcao
            clientSocket.send(escolha.encode())
        if opcao == '1':
            system("clear")
            print('Selecione a espécie:')
            print('1 - Abelha')
            print('2 - Cachorro')
            print('3 - Morcego')
            print('4 - Panda')
            print('5 - Pato')
            escolha_especie = input('> ')
            escolha += escolha_especie
            clientSocket.send(escolha.encode())
            clientSocket.close()
            print('Arquivo baixado com sucesso!')
            break
        if opcao == '2':
            system("clear")
            nome_especie = input("Digite o nome popular ou nome cientifico da espécie:")
            clientSocket.send(nome_especie.encode())
            genoma = input("Agora informe a sequencia genomica da especie:")
            clientSocket.send(genoma.encode())
            resposta = clientSocket.recv(1024)
            print(resposta.decode())
            clientSocket.close()
            break

        if opcao == '3':
            clientSocket.close()
            print('Até breve')
            break
