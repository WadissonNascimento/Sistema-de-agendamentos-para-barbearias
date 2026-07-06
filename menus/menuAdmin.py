from uteis import limpar_terminal, titulo
from conexaoBanco import conexaoBanco
from servicos import funcoes_admin




def menuAdmin(opcoes):
    cursor, conexao = conexaoBanco()

    while True:
        limpar_terminal()
        titulo('PAINEL DO ADMIN')

        for n in range(len(opcoes)):
            print(f'{n+1} {opcoes[n]:.>83}')

        while True:
            try:
                resposta = int(input('Escolha uma opção acima: '))

                if resposta == 0 or resposta > len(opcoes):
                    print('Resposta invalida, tente novamente')
                else:
                    break
            except:
                print('Selecione uma opcao valida!')

        if resposta == 1:
            funcoes_admin.cadastrarBarbeiro(cursor, conexao)

        elif resposta == 2:
            funcoes_admin.exibirEquipe(cursor, conexao)
        
        elif resposta == 3:
            funcoes_admin.exibirAgendaGeral(cursor, conexao)

        elif resposta == 4:
            break






