import funcoes

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