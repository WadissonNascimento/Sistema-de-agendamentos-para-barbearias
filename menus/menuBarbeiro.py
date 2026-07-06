from servicos import funcoes_barbeiro
from conexaoBanco import conexaoBanco
from uteis import limpar_terminal, titulo


def menuBarbeiro(opcoes):
    
    cursor, conexao = conexaoBanco()
    id_barbeiro = funcoes_barbeiro.pegarIdBarbeiro(cursor)

    while True:
        limpar_terminal()

        titulo('BEM VINDO AO PAINEL DO BARBEIRO')
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
            funcoes_barbeiro.mostrarAgendaHoje(cursor, id_barbeiro, conexao)
        elif resposta == 2:
            funcoes_barbeiro.exibirAgendaGeral(cursor, id_barbeiro, conexao)

        elif resposta == 3:
            funcoes_barbeiro.exibirDisponibilidade(cursor, id)

            print('-'*85)
            print('Deseja alterar algo na disponibilidade? ')
            print('[ 0 ] para alterar inicio \n[ 1 ] para alterar fim \n[ 2 ] para alterar o status \n[ 3 ] para voltar ao menu')
            escolherAlteracao = int(input())
            
            if escolherAlteracao == 0:
                dia = input('Qual Dia deseja alterar? ')
                horarioInicio = input('Digite o novo horario: ')
                funcoes_barbeiro.alterarDisponibilidadeInicio(cursor, dia, horarioInicio, id, conexao)

            elif escolherAlteracao == 1:
                dia = input('Qual Dia deseja alterar? ')
                horarioFim = input('Digite o novo horario: ')
                funcoes_barbeiro.alterarDisponibilidadeFim(cursor, dia, horarioFim, id, conexao)

            elif escolherAlteracao == 2:
                dia = input('Qual Dia deseja alterar? ')
                funcoes_barbeiro.alterarStatus(cursor, dia, id, conexao)
        elif resposta == 4:
            break