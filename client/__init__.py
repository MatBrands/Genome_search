from interface.socketClient import *
from interface.menuClass import *

def parametros_menu(titulo: list, itens: list):
    menu = Menu()
    menu.setTitulo(titulo)
    menu.setItems(itens)
    option = menu.iniciarMenu()
    return option

if __name__ == '__main__':
    title = ['Selecione uma opção: ']
    itens = ['Buscar genoma (Download)', 'Cadastrar genoma (Upload)', 'Sair']
    while True:
        menu_item = parametros_menu(title, itens)
        # client_socket = SocketClient()
        
        if menu_item == 0:
            pass
        elif menu_item == 1:
            pass
        else:
            break