import os
from termcolor import colored
from pynput import keyboard

class Menu:
    def __init__(self):
        pass

    def on_press(self, key):
        if (str(key) == 'Key.up'):
            self.option-=1
        elif (str(key) == 'Key.down'):
            self.option+=1
        elif (str(key) == 'Key.enter'):
            self.acess = True

        return False

    def setTitulo(self, *args):
        self.title = ''.join(*args)

    def setItems(self, *args):
        self.elementos = len(*args)
        self.items = list(*args)

    def iniciarMenu(self):
        self.option = 0
        self.acess = False
        menu_atual = self.items.copy()

        while not self.acess:
            os.system("clear")
            
            for i in range (self.elementos):
                if self.option%self.elementos == i:
                    if menu_atual[i] in ['Sair', 'Retornar']:
                        menu_atual[i] = colored(menu_atual[i], 'red')
                    else:
                        menu_atual[i] = colored(menu_atual[i], 'green')

            if self.title:
                print (self.title)
                
            [print(item) for item in menu_atual]

            with keyboard.Listener(on_press=self.on_press) as listener: 
                listener.join()
                menu_atual = self.items.copy()

        input()
        os.system("clear")

        return self.option%self.elementos