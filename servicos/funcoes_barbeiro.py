import datetime
import conexaoBanco
from uteis import limpar_terminal, titulo



def exibirAgendaGeral(cursor, id, conexao):
    cursor, conexao = conexaoBanco.conexaoBanco()
    limpar_terminal()
    while True:

        try:
            dia = int(input('Digite o dia que deseja vizualizar a agenda: '))

            diaAtual = datetime.datetime.today()

            dataDeConsulta = datetime.date(diaAtual.year, diaAtual.month, dia)

            break

        except ValueError:
            input('Digite apenas números!! pressione enter para escolher novamente...')
            continue

    cursor.execute('''
    SELECT nome, servico, horario_inicio, barbeiro, data, status
    FROM agendamentos
    WHERE barbeiro = %s AND data = %s
    ORDER BY horario_inicio
    ''',
    (id, dataDeConsulta)
    )

    consulta = cursor.fetchall()

    if not consulta:
        input('Não há agendamentos disponíveis para visualização nessa data, pressione enter para voltar ao menu...')
    else:
        print(f'{'nome':<15} {'servico':<15} {'horario':<15} {'barbeiro':<15} {'data':<15} {'status':<15}')
        print('-'*85)

        for nome, servico, horarioInicio, barbeiro, data, status in consulta:
            print(f'{nome:<15} {servico:<15} {horarioInicio.strftime('%H:%M'):<15} {barbeiro:<15} {data.strftime('%d/%m/%y'):<15} {status:<15}')
        
        try:
            print('[ 1 ] Para concluir um agendamento \n[ 2 ] para cancelar um agendamento \n[ 3 ] para voltar ao menu')
            escolha = int(input())
        
            if escolha ==  1:
                concluirAgendamento(cursor, id, conexao, dataDeConsulta)
            elif escolha == 2:
                cancelarAgendamento(cursor, id, conexao, dataDeConsulta)
        except ValueError:
            input('Digite uma das opções acima...')
    


def mostrarAgendaHoje(cursor, id, conexao):
    limpar_terminal()

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

    if not consulta:
        input('Não há agendamentos disponíveis para visualização, pressione enter para voltar ao menu...')
    else:
        print(f'{'nome':<15} {'servico':<15} {'horario':<15} {'barbeiro':<15} {'data':<15} {'status':<15}')
        print('-'*85)

        for nome, servico, horarioInicio, barbeiro, data, status in consulta:
            print(f'{nome:<15} {servico:<15} {horarioInicio.strftime('%H:%M'):<15} {barbeiro:<15} {data.strftime('%d/%m/%y'):<15} {status:<15}')
        
    while True:
        try:
            print('[ 1 ] Para concluir um agendamento \n[ 2 ] para cancelar um agendamento \n[ 3 ] para voltar ao menu')
            escolha = int(input())
            if escolha ==  1:
                concluirAgendamento(cursor, id, conexao, dataAtual)
                break
            elif escolha == 2:
                cancelarAgendamento(cursor, id, conexao, dataAtual)
                break
            
        except ValueError:
            input('Digite uma das opções acima!! pressione enter para tentar novamente...')
        
        

def cancelarAgendamento(cursor, id ,conexao, data):
    while True:
        horario = input('Digite o horario que deseja cancelar: ')
        cursor.execute('''
        UPDATE agendamentos
        SET status = 'cancelado'
        WHERE barbeiro = %s AND horario_inicio = %s AND data = %s
        ''',
        (id, horario, data)
        )

        consulta = cursor.fetchone()

        if not consulta:
            input('Agendamento não encontrado, pressione enter para tentar novamente...')
            conexao.rollback()
        else:
            conexao.commit()
            input('Agendamento cancelado com sucesso! pressione enter para sair...')
            break


def concluirAgendamento(cursor, id, conexao, data):
    while True:
        horario = input('Digite o horario que deseja concluir: ')
        cursor.execute('''
        UPDATE agendamentos
        SET status = 'concluido'
        WHERE barbeiro = %s AND horario_inicio = %s AND data = %s
        ''',
        (id, horario, data)
        )

        consulta = cursor.fetchone()

        if not consulta:
            input('Agendamento não encontrado, pressione enter e tente novamente...')
            conexao.rollback()
        else:
            conexao.commit()
            input('Agendamento concluído com sucesso! pressione enter para sair...')
            break


def pegarIdBarbeiro(cursor):
    while True:
        id_barbeiro = int(input('Digite seu id de barbeiro: '))

        cursor.execute('''
        SELECT id
        FROM barbeiros
        WHERE id = %s
        ''',
        (id_barbeiro,)
        )
        
        consulta = cursor.fetchone()

        if not consulta:
            input('ID não existe! pressione enter e digite um ID válido...')
        else:
            return id_barbeiro


def alterarDisponibilidadeInicio(cursor, dia, horarioInicio, id, conexao):
    cursor.execute('''
    UPDATE disponibilidade
    SET horario_inicio = %s
    WHERE dia_semana = %s AND id_barbeiro = %s 
    ''',
    (horarioInicio, dia, id)
    )

    if cursor.rowcount == 0:
        input('Erro ao atualizar disponíbilidade')
    else: 
        conexao.commit()
        input('Disponíbilidade atualizada com sucesso.')

    exibirDisponibilidade(cursor, id)


def alterarDisponibilidadeFim(cursor, dia, horarioFim, id, conexao):
    cursor.execute('''
    UPDATE disponibilidade
    SET horario_fim = %s
    WHERE dia_semana = %s AND id_barbeiro = %s 
    ''',
    (horarioFim, dia, id)
    )

    if cursor.rowcount == 0:
        input('Erro ao atualizar disponíbilidade')
    else: 
        conexao.commit()
        input('Disponíbilidade atualizada com sucesso.')

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
        if cursor.rowcount == 0:
            input('Erro ao atualizar disponíbilidade')
        else: 
            conexao.commit()
            input('Disponíbilidade atualizada com sucesso.')

        
    if resposta[0] == 'desativado':
        cursor.execute('''
        UPDATE disponibilidade
        SET status = 'ativo'
        WHERE id_barbeiro = %s AND dia_semana = %s
        ''',
        (id, dia)
        )

        if cursor.rowcount == 0:
            input('Erro ao atualizar disponíbilidade')
        else: 
            conexao.commit()
            input('Disponíbilidade atualizada com sucesso.')
    
    exibirDisponibilidade(cursor,id)


def exibirDisponibilidade(cursor, id):
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

    if not horarios:
        input('Nenhuma disponibilidade encontrada')
        conexao.rollback()
    else:
        colunas = [coluna[0] for coluna in cursor.description]
        print(f'{colunas[1]:<20} {colunas[2]:<20} {colunas[3]:<30} {colunas[4]:<30}')
        print('-'*85)
        for id_barbeiro, dia, horario_inicio, horario_fim, status  in horarios:
            inicio = horario_inicio.strftime('%H:%M')
            fim = horario_fim.strftime('%H:%M')
            print(f'{dia:<20} {inicio:<20} {fim:<30} {status:<30}')