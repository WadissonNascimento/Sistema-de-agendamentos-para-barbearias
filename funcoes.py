import psycopg2
import os
from dotenv import load_dotenv
import time
import datetime
import funcoes_cliente
import funcoes_barbeiro
import funcoes_admin

load_dotenv()



def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def titulo(msg):
    tamanho = 85

    print(msg.center(tamanho))
    print('-'*tamanho)


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


def menuBarbeiro(opcoes):
    id = funcoes_barbeiro.pegarIdBarbeiro()
    while True:
        limpar_terminal()

        cursor, conexao = conexaoBanco()
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
            funcoes_barbeiro.mostrarAgendaHoje(cursor, id, conexao)
        elif resposta == 2:
            funcoes_barbeiro.exibirAgendaGeral(cursor, id, conexao)

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



def menuCliente(opcoes):
    limpar_terminal()
    cursor, conexao = conexaoBanco()

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

        escolhaServico, duracao, valor = funcoes_cliente.escolherServico(cursor)
            
        escolhaHorario, horarioFim = funcoes_cliente.escolherHorario(cursor, escolhaBarbeiro, escolhaDiaSemana, diaAtual, dataCompleta, duracao)

        nomeCliente = str(input('Qual seu nome: '))
        
        resumo = funcoes_cliente.exibirResumoAgendamento(cursor, conexao, nomeCliente, escolhaServico, escolhaHorario, horarioFim, valor, dataCompleta, escolhaBarbeiro)
    elif resposta == 2:
        funcoes_cliente.mostrarAgendamentos(cursor)
    
    elif resposta == 3:
        funcoes_cliente.mostrarHistorico(cursor)

    
def conexaoBanco():
    conexao = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password=os.getenv('key_db'),
        port="5432"
    )

    cursor = conexao.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS barbeiros(
        id SERIAL PRIMARY KEY,
        nome VARCHAR(20),
        telefone VARCHAR(20),
        email VARCHAR(100)
    );
    CREATE TABLE IF NOT EXISTS disponibilidade(
        id_Barbeiro INTEGER REFERENCES barbeiros(id),
        dia_semana VARCHAR(20),
        horario_inicio TIME,
        horario_fim TIME,
        status VARCHAR(20) DEFAULT 'ativo'
     );
    CREATE TABLE IF NOT EXISTS servicos(
        nome VARCHAR(20) UNIQUE,
        duracao INTEGER,
        valor DECIMAL (10, 2)
    );
    CREATE TABLE IF NOT EXISTS agendamentos(
        nome VARCHAR(20),
        servico VARCHAR(20),
        horario_inicio TIME,
        horario_fim TIME,
        barbeiro VARCHAR(20),
        valor DECIMAL (10, 2),
        status  VARCHAR(20),
        data date
    );
    ''')

    conexao.commit()
    return cursor, conexao
