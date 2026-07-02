import funcoes
import datetime

def exibirAgendaGeral(cursor, id, conexao):
    funcoes.limpar_terminal()

    dia = int(input('Digite o dia que deseja vizualizar a agenda: '))

    diaAtual = datetime.datetime.today()

    dataDeConsulta = datetime.date(diaAtual.year, diaAtual.month, dia)

    cursor.execute('''
    SELECT nome, servico, horario_inicio, barbeiro, data, status
    FROM agendamentos
    WHERE barbeiro = %s AND data = %s
    ORDER BY horario_inicio
    ''',
    (id, dataDeConsulta)
    )

    consulta = cursor.fetchall()

    print(f'{'nome':<15} {'servico':<15} {'horario':<15} {'barbeiro':<15} {'data':<15} {'status':<15}')
    print('-'*85)

    for nome, servico, horarioInicio, barbeiro, data, status in consulta:
        print(f'{nome:<15} {servico:<15} {horarioInicio.strftime('%H:%M'):<15} {barbeiro:<15} {data.strftime('%d/%m/%y'):<15} {status:<15}')
    
    print('[ 1 ] Para concluir um agendamento \n[ 2 ] para cancelar um agendamento \n[ 3 ] para voltar ao menu')
    escolha = int(input())
    
    if escolha ==  1:
        concluirAgendamento(cursor, id, conexao, dataDeConsulta)
    elif escolha == 2:
        cancelarAgendamento(cursor, id, conexao, dataDeConsulta)
    

    






def mostrarAgendaHoje(cursor, id, conexao):
    funcoes.limpar_terminal()

    dataAtual = datetime.datetime.today()
    dataAtual = datetime.date(dataAtual.year, dataAtual.month, dataAtual.day)

    cursor.execute('''
    SELECT nome, servico, horario_inicio, barbeiro, data, status
    FROM agendamentos 
    WHERE barbeiro = %s AND data = %s
    ORDER BY horario_inicio
    ''',
    (id, dataAtual)
    )

    consulta =  cursor.fetchall()

    print(f'{'nome':<15} {'servico':<15} {'horario':<15} {'barbeiro':<15} {'data':<15} {'status':<15}')
    print('-'*85)

    for nome, servico, horarioInicio, barbeiro, data, status in consulta:
        print(f'{nome:<15} {servico:<15} {horarioInicio.strftime('%H:%M'):<15} {barbeiro:<15} {data.strftime('%d/%m/%y'):<15} {status:<15}')
    
    print('[ 1 ] Para concluir um agendamento \n[ 2 ] para cancelar um agendamento \n[ 3 ] para voltar ao menu')
    escolha = int(input())
    
    if escolha ==  1:
        concluirAgendamento(cursor, id, conexao, dataAtual)
    elif escolha == 2:
        cancelarAgendamento(cursor, id, conexao, dataAtual)

def cancelarAgendamento(cursor, id ,conexao, data):
    horario = input('Digite o horario que deseja cancelar: ')
    cursor.execute('''
    UPDATE agendamentos
    SET status = 'cancelado'
    WHERE barbeiro = %s AND horario_inicio = %s AND data = %s
    ''',
    (id, horario, data)
    )

    conexao.commit()


def concluirAgendamento(cursor, id, conexao, data):
    horario = input('Digite o horario que deseja concluir: ')
    cursor.execute('''
    UPDATE agendamentos
    SET status = 'concluido'
    WHERE barbeiro = %s AND horario_inicio = %s AND data = %s
    ''',
    (id, horario, data)
    )

    conexao.commit()


def pegarIdBarbeiro():
    id = int(input('Digite seu id de barbeiro: '))

    return id 


def alterarDisponibilidadeInicio(cursor, dia, horarioInicio, id, conexao):
    cursor.execute('''
    UPDATE disponibilidade
    SET horario_inicio = %s
    WHERE dia_semana = %s AND id_barbeiro = %s 
    ''',
    (horarioInicio, dia, id)
    )

    conexao.commit()

    exibirDisponibilidade(cursor, id)


def alterarDisponibilidadeFim(cursor, dia, horarioFim, id, conexao):
    cursor.execute('''
    UPDATE disponibilidade
    SET horario_fim = %s
    WHERE dia_semana = %s AND id_barbeiro = %s 
    ''',
    (horarioFim, dia, id)
    )

    conexao.commit()

    exibirDisponibilidade(cursor, id)

def alterarStatus(cursor, dia, id, conexao):
    cursor.execute('''
    SELECT status
    FROM disponibilidade
    WHERE dia_semana = %s AND id_barbeiro = %s
    ''',
    (dia, id)
    )

    resposta = cursor.fetchone()

    if resposta[0] == 'ativo':
        cursor.execute('''
        UPDATE disponibilidade
        SET status = 'desativado'
        WHERE id_barbeiro = %s AND dia_semana = %s
        ''',
        (id, dia)
        )

        conexao.commit()
        
    if resposta[0] == 'desativado':
        cursor.execute('''
        UPDATE disponibilidade
        SET status = 'ativo'
        WHERE id_barbeiro = %s AND dia_semana = %s
        ''',
        (id, dia)
        )

        conexao.commit()
    
    exibirDisponibilidade(cursor,id)


def exibirDisponibilidade(cursor, id):
    funcoes.limpar_terminal()
    funcoes.titulo('DISPONIBILIDADE DO BARBEIRO')
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
    print(f'{colunas[1]:<20} {colunas[2]:<20} {colunas[3]:<30} {colunas[4]:<30}')
    print('-'*85)
    for id_barbeiro, dia, horario_inicio, horario_fim, status  in horarios:
        inicio = horario_inicio.strftime('%H:%M')
        fim = horario_fim.strftime('%H:%M')
        print(f'{dia:<20} {inicio:<20} {fim:<30} {status:<30}')
    input('Aperte enter para continuar...')