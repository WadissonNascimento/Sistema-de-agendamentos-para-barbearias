import os

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def titulo(msg):
    tamanho = 85

    print(msg.center(tamanho))
    print('-'*tamanho)
