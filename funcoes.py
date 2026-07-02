import psycopg2
import os
from dotenv import load_dotenv
import time
import datetime
import funcoes_cliente

load_dotenv()



def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def titulo(msg):
    tamanho = 85

    print(msg.center(tamanho))
    print('-'*tamanho)


def menuAdmin(opcoes):
    horario_padrao = [
        ('segunda', '09:00', '18:00'),
        ('terca', '09:00', '18:00'),
        ('quarta', '09:00', '18:00'),
        ('quinta', '09:00', '18:00'),
        ('sexta', '09:00', '18:00'),
        ('sabado','09:00', '18:00' ),
        ('domingo','09:00', '18:00' )
    ]
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
            limpar_terminal()
            titulo('CADASTRO DE BARBEIRO')

            while True:
                nome = input('NOME: ')
                telefone = input('TELEFONE: ').replace(' ', '').replace('(', '').replace(')', '').replace('-', '').strip()
                email = input('EMAIL: ')

                telefone_valido = telefone.isdigit() and len(telefone) == 11
                email_valido = '@' in email and '.' in email

                if telefone_valido and email_valido:
                    break
                else:
                    print('Digite os dados corretamente!')

            cursor.execute('''
            INSERT INTO barbeiros (nome, telefone, email)
            VALUES (%s, %s, %s)
            RETURNING id
            ''',
            (nome, telefone, email)
            )

            barbeiro_id =  cursor.fetchone()[0]
            for dia, inicio, fim in horario_padrao:
                cursor.execute('''
                INSERT INTO disponibilidade (id_barbeiro, dia_semana, horario_inicio, horario_fim)
                VALUES (%s, %s, %s, %s)
                ''',
                (barbeiro_id, dia, inicio, fim )
                )


            conexao.commit()

            print('Barbeiro cadastrado com sucesso')
            print('Você sera redirecionado em 3 segundos')
            print('1', end='')
            time.sleep(1)
            print('2', end='')
            time.sleep(1)
            print('3')
            time.sleep(1)

        elif resposta == 2:
            limpar_terminal()
            titulo('BARBEIROS CADASTRADOS')
            cursor.execute('''
            SELECT * FROM barbeiros
            ''')

            barbeiros = cursor.fetchall()

            if barbeiros:
                colunas = [coluna[0] for coluna in cursor.description]
                print(f'{colunas[0]:<10}{colunas[1]:<20}{colunas[2]:<30}{colunas[3]:<40}')

                print('-' * 85)
                for barbeiro in barbeiros:
                    print(f'{barbeiro[0]:<10}{barbeiro[1]:<20}{barbeiro[2]:<30}{barbeiro[3]:<40}')

                
                print()
                id_Consulta = input('Digite o ID do barbeiro para consultar os horarios de trabalho ou enter para sair: ').strip()
                if id_Consulta == '':
                    return
                try:
                    cursor.execute('''
                    SELECT *
                    FROM disponibilidade
                    WHERE id_barbeiro = %s
                    ORDER BY CASE dia_semana
                        WHEN 'segunda' THEN 1
                        WHEN 'terca' THEN 2
                        WHEN 'quarta' THEN 3
                        WHEN 'quinta' THEN 4
                        WHEN 'sexta' THEN 5
                        WHEN 'sabado' THEN 6
                        WHEN 'domingo' THEN 7
                    END
                    ''',
                    (id_Consulta,)
                    )

                    disponibilidadeBarbeiro =  cursor.fetchall()
                    coluna = [coluna[0] for coluna in cursor.description]

                    cursor.execute('''
                    SELECT *
                    FROM barbeiros
                    WHERE id = %s
                    ''',
                    (id_Consulta,)
                    )
                    nomeBarbeiro = cursor.fetchall()
                    limpar_terminal()
                    titulo(f'Horários do barbeiro {nomeBarbeiro[0][1]}')
                    print(f'{coluna[1]:<20} {coluna[2]:<20} {coluna[3]:<20}')
                    for id_barbeiro, dia_semana, horario_inicio, horario_fim in disponibilidadeBarbeiro:
                        inicio = horario_inicio.strftime('%H:%M')
                        final = horario_fim.strftime('%H:%M')
                        print(f'{dia_semana:<20} {inicio:<20} {final:<20}')
                    print('-'*85)
                    input('Pressione enter para voltar...')
                except:
                    print('Preencha um id válido')
                    time.sleep(5)


        

            else:
                input('Nao ha barbeiros cadastrados, pressione enter para retornar ao menu...')
        else:
            break


def menuBarbeiro(opcoes, id):
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
        if resposta == 3:
                limpar_terminal()
                titulo('DISPONIBILIDADE DO BARBEIRO')
                cursor.execute('''
                SELECT *
                FROM disponibilidade
                WHERE id_barbeiro = %s
                ORDER BY CASE dia_semana
                    WHEN 'segunda' THEN 1
                    WHEN 'terca' THEN 2
                    WHEN 'quarta' THEN 3
                    WHEN 'quinta' THEN 4
                    WHEN 'sexta' THEN 5
                    WHEN 'sabado' THEN 6
                    WHEN 'domingo' THEN 7
                END
                ''',
                (id,)
                )
                horarios = cursor.fetchall()
                colunas = [coluna[0] for coluna in cursor.description]
                print(f'{colunas[1]:<20} {colunas[2]:<20} {colunas[3]:<30}')
                print('-'*85)
                for id_barbeiro, dia, horario_inicio, horario_fim in horarios:
                    inicio = horario_inicio.strftime('%H:%M')
                    fim = horario_fim.strftime('%H:%M')
                    print(f'{dia:<20} {inicio:<20} {fim:<30}')
                while True:
                    diaAlteracao = input('Digite o dia que deseja alterar o horario ou enter pra sair: ')
                    diasDaSemana = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']
                    try:
                        if diaAlteracao in  diasDaSemana:
                            alteracao = input('Deseja alterar o inicio ou o fim? ').strip().lower()
                            alteracaoHorario = input('Digite o novo horario no formato (00:00): ')
                            if alteracao == 'inicio':
                                cursor.execute('''
                                UPDATE disponibilidade
                                SET horario_inicio = %s
                                WHERE id_barbeiro = %s AND dia_semana = %s
                                ''',
                                (alteracaoHorario, id, diaAlteracao )
                                )
                                conexao.commit()
                                break
                            elif alteracao == 'fim':
                                cursor.execute('''
                                UPDATE disponibilidade
                                SET horario_fim = %s
                                WHERE id_barbeiro = %s AND dia_semana = %s
                                ''',
                                (alteracaoHorario, id, diaAlteracao )
                                )
                                conexao.commit()
                                break
                            else:
                                print('preencha os dados corretamente')
                        elif diaAlteracao == '':
                            break
                        else:
                            print('preencha os dados corretamente')
                    except:
                        print('Preencha os dados corretamente!')
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
