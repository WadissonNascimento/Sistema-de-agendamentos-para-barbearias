from uteis import limpar_terminal, titulo
from servicos import funcoes_cliente
from conexaoBanco import conexaoBanco



def menuCliente(opcoes):
    cursor, conexao = conexaoBanco()
    limpar_terminal()

    titulo('PAINEL DO CLIENTE')

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
        escolhaBarbeiro = funcoes_cliente.escolherBarbeiro(cursor)
        
        dataCompleta, escolhaDiaSemana, diaAtual =  funcoes_cliente.escolherData()

        escolhaServico, duracao, valor = funcoes_cliente.escolherServico(cursor, conexao)
            
        escolhaHorario, horarioFim = funcoes_cliente.escolherHorario(cursor, escolhaBarbeiro, escolhaDiaSemana, diaAtual, dataCompleta, duracao)
        
        while True:
            nomeCliente = str(input('Qual seu nome: '))
            if not nomeCliente.isalpha():
                input('Digite apenas letras! aperte enter para tentar novamente...')
                continue
            else:
                break
        
        resumo = funcoes_cliente.exibirResumoAgendamento(cursor, conexao, nomeCliente, escolhaServico, escolhaHorario, horarioFim, valor, dataCompleta, escolhaBarbeiro)
    elif resposta == 2:
        funcoes_cliente.mostrarAgendamentos(cursor)
    
    elif resposta == 3:
        funcoes_cliente.mostrarHistorico(cursor)

    
