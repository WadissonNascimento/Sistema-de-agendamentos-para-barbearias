import funcoes
import time
import funcoes_barbeiro
import datetime

def exibirAgendaGeral(cursor, conexao):
    cursor.execute('''
    SELECT nome, servico, horario_inicio, barbeiro, status, data
    FROM AGENDAMENTOS 
    ORDER BY data, horario_inicio
    ''')

    consulta = cursor.fetchall()

    dataAtual = datetime.date.today()

    print(f'{'nome':<15} {'servico':<15} {'horario_inicio':<15} {'barbeiro':<15} {'status':<15} {'data':<15}')

    print('-'*85)

    for nome, servico, horario_inicio, barbeiro, status, data in consulta:
        print(f'{nome:<15} {servico:<15} {horario_inicio.strftime('%H:%M'):<15} {barbeiro:<15} {status:<15} {data.strftime('%d/%m/%y'):<15}')
    
    print()
    print('-'*85)

    print('[ 1 ] para concluir algum atendimento \n[ 2 ] para cancelar alguma atendimento \n[ 3 ] para visualizar agenda de outro dia \n[ 4 ] para voltar ao menu')
    escolha = int(input('escolha: '))

    if escolha == 1:
        funcoes.limpar_terminal()

        id_barbeiro = int(input('Digite o ID do barbeiro:'))
        
        funcoes_barbeiro.concluirAgendamento(cursor, id, conexao, dataAtual)
    elif escolha == 2:
        id_barbeiro = int(input('Digite o ID do barbeiro:'))

        funcoes_barbeiro.cancelarAgendamento(cursor, id_barbeiro, conexao, dataAtual)
    
    elif escolha == 3:

        funcoes_barbeiro.exibirAgendaGeral(cursor, id=None, conexao=conexao)




def exibirEquipe(cursor, conexao):
    funcoes.limpar_terminal()
    funcoes.titulo('BARBEIROS CADASTRADOS')
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

        print('-' * 85)
        print('[ 1 ] para excluir um barbeiro da equipe \n[ 2 ] para exibir hoário do barbeiro \n[ 3 ] para sair')
        escolha = int(input('Escolha:'))
        if escolha == 1: 
            excluirBarbeiro(cursor, conexao)
        elif escolha == 2:
            exibirHorariosBarbeiro(cursor)
            
    else:
        input('Não há barbeiros cadastrados! pressione enter para voltar...')

def excluirBarbeiro(cursor, conexao):
    id_barbeiro = int(input('Digite o id do barbeiro que deseja excluir: '))

    cursor.execute('''
    DELETE FROM disponibilidade
    WHERE id_barbeiro = %s
    ''',
    (id_barbeiro,)
    )


    cursor.execute('''
    DELETE FROM barbeiros
    WHERE id = %s
    ''',
    (id_barbeiro,)
    )

    conexao.commit()




def exibirHorariosBarbeiro(cursor):
    id_Consulta = int(input('Digite o ID do barbeiro para consultar os horarios de trabalho ou enter para sair: ').strip())
    if id_Consulta == '':
            pass
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
    funcoes.limpar_terminal()
    funcoes.titulo(f'Horários do barbeiro {nomeBarbeiro[0][1]}')
    print(f'{coluna[1]:<20} {coluna[2]:<20} {coluna[3]:<20} {coluna[4]:<20}')
    print('-'*85)
    for id_barbeiro, dia_semana, horario_inicio, horario_fim, status in disponibilidadeBarbeiro:
        inicio = horario_inicio.strftime('%H:%M')
        final = horario_fim.strftime('%H:%M')
        print(f'{dia_semana:<20} {inicio:<20} {final:<20} {status:<20}')
    print('-'*85)
    input('Pressione enter para voltar...')


def cadastrarBarbeiro(cursor, conexao):
    
    horario_padrao = [
        ('segunda', '09:00', '18:00'),
        ('terca', '09:00', '18:00'),
        ('quarta', '09:00', '18:00'),
        ('quinta', '09:00', '18:00'),
        ('sexta', '09:00', '18:00'),
        ('sabado','09:00', '18:00' ),
        ('domingo','09:00', '18:00' )
    ]

    while True:
        funcoes.limpar_terminal()
        funcoes.titulo('CADASTRO DE BARBEIRO')
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
            VALUES (%s, %s, %s, %s, %s)
            ''',
            (barbeiro_id, dia, inicio, fim, 'ativo')
            )


            conexao.commit()

        print('Barbeiro cadastrado com sucesso')
        print('Você sera redirecionado em 3 segundos')
        time.sleep(3)