from interface.socketClient import *
from interface.menuClass import *


def parametros_menu(titulo: list, itens: list):
    menu = Menu()
    menu.setTitulo(titulo)
    menu.setItems(itens)
    option = menu.iniciarMenu()
    return option


def buscar_genoma(socket):
    list_of_items_db = socket.get_items()
    itens = ['Observar genomas catalogados', 'Busca e download de genoma', 'Retornar']
    menu_item = parametros_menu(['Selecione uma opção:'], itens)
    if menu_item == 0:
        print('Todos os genomas catalogados: ')
        for item in list_of_items_db:
            print(item)
        input('Para retornar digite uma tecla:')
    elif menu_item == 1:
        # Busca
        input('Digite o nome científico ou nome popular: ')
    else:
        return


if __name__ == '__main__':
    title = ['Selecione uma opção: ']
    itens = ['Buscar genoma (Download)', 'Cadastrar genoma (Upload)', 'Sair']
    print('Bem vindo, bla bla bla')
    while True:
        menu_item = parametros_menu(title, itens)
        client_socket = SocketClient()
        
        if menu_item == 0:
            buscar_genoma(client_socket)
        elif menu_item == 1:
            pass
        else:
            break
