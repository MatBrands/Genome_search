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
        input(f'Download do genoma {resultado[menu_item]} foi um sucesso')

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
        input('Erro ! Arquivos inválidos, tecle para sair ...\n')
        return
    filenames.append('Retornar')
    
    nome = f'{nome_especie}: {nome_popular}'
    genoma_especie = parametros_menu(['Selecione o arquivo que deseja enviar:'], filenames)
    genoma_especie = filenames[genoma_especie]
    
    if genoma_especie == 'Retornar':
        return
    
    socket.set_file(nome, genoma_especie)
    input(f'Upload do genoma {nome} foi cadastrado')

if __name__ == '__main__':
    client_socket = SocketClient()

    if not client_socket.setup(host=gethostbyname(gethostname()), port=55552):
        print('Servidor não encontrado')
        exit()

    title = ['Selecione uma opção: ']
    itens = ['Buscar genoma (Download)', 'Cadastrar genoma (Upload)', 'Sair']
    while True:
        menu_item = parametros_menu(title, itens)

        if menu_item == 0:
            menu_genoma(client_socket)
        elif menu_item == 1:
            cadastrar_genoma(client_socket)
        else:
            break