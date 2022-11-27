from interface.socketClient import *
from interface.menuClass import *


def parametros_menu(titulo: list, itens: list):
    menu = Menu()
    menu.setTitulo(titulo)
    menu.setItems(itens)
    option = menu.iniciarMenu()
    return option


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
            # Busca
            name = input('Digite o nome científico ou o popular: ')
            buscar_genoma(socket, name, list_of_items_db)
            break
        else:
            break


def buscar_genoma(socket, name, list_of_items_db):
    resultado = []
    for item in list_of_items_db:
        if name in item:
            resultado.append(item)

    if len(resultado) > 0:
        resultado.append('Retornar')
        menu_item = parametros_menu(['Selecione o genoma para download: '], resultado)
        if menu_item != len(resultado) - 1:
            socket.get_file(resultado[menu_item])
            print(f'Download do genoma {resultado[menu_item]} foi um sucesso')
            input()


def cadastrar_genoma(socket):
    nome_especie = input('Digite o nome científico ou nome popular ')
    if nome_especie:
        socket.set_file(nome_especie)
        print(f'Upload do genoma {nome} foi um sucesso')
        input()


if __name__ == '__main__':
    client_socket = SocketClient()

    if not client_socket.setup(host=gethostbyname(gethostname()), port=55551):
        print('Servidor não encontrado')
        exit()

    title = ['Selecione uma opção: ']
    itens = ['Buscar genoma (Download)', 'Cadastrar genoma (Upload)', 'Sair']
    print('Bem vindo, bla bla bla')
    while True:
        menu_item = parametros_menu(title, itens)
        #client_socket = SocketClient()

        if menu_item == 0:
            menu_genoma(client_socket)
        elif menu_item == 1:
            cadastrar_genoma(client_socket)
        else:
            break
