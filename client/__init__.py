from interface.socketClient import *
from interface.menuClass import *
from os import system

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
            name = input('Digite o nome científico ou o popular: \n')
            buscar_genoma(socket, name, list_of_items_db)
            return
        else:
            return

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

if __name__ == '__main__':
    client_socket = SocketClient(host='10.0.0.188')

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