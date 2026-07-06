import datetime
import conexaoBanco
from uteis import limpar_terminal, titulo
from servicos.funcoes_barbeiro import concluirAgendamento, cancelarAgendamento, exibirAgendaGeral



def exibirAgendaGeral():
    cursor, conexao = conexaoBanco.conexaoBanco()
    limpar_terminal()

    cursor.execute('''
    SELECT nome, servico, horario_inicio, barbeiro, status, data
    FROM AGENDAMENTOS 
    ORDER BY data, horario_inicio
    ''')

    consulta = cursor.fetchall()

    if not consulta:
        input('Nenhum agendamento encontrado! pressione enter para sair.')
    
    else:
        dataAtual = datetime.date.today()

        print(f'{'nome':<15} {'servico':<15} {'horário':<15} {'barbeiro':<15} {'status':<15} {'data':<15}')

        print('-'*85)

        for nome, servico, horario_inicio, barbeiro, status, data in consulta:
            print(f'{nome:<15} {servico:<15} {horario_inicio.strftime('%H:%M'):<15} {barbeiro:<15} {status:<15} {data.strftime('%d/%m/%y'):<15}')
        
        print()
        print('-'*85)

        print('[ 1 ] para concluir algum atendimento \n[ 2 ] para cancelar algum atendimento \n[ 3 ] para escolher um dia para visualizar \n[ 4 ] para voltar ao menu')
        while True:
            try:
                escolha = int(input('escolha: '))

                if escolha == 1:
                    limpar_terminal()

                    id_barbeiro = int(input('Digite o ID do barbeiro:'))
                    
                    concluirAgendamento(cursor, id_barbeiro, conexao, dataAtual)
                    break
                elif escolha == 2:
                    id_barbeiro = int(input('Digite o ID do barbeiro:'))

                    cancelarAgendamento(cursor, id_barbeiro, conexao, dataAtual)
                    break
                elif escolha == 3:

                    exibirAgendaGeral(cursor, id=None, conexao=conexao)
                    break
            except ValueError:
                input('Escolha uma das opções acima! pressione enter para tentar novamente...')


def exibirEquipe(cursor, conexao):
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

        print('-' * 85)
        print('[ 1 ] para excluir um barbeiro da equipe \n[ 2 ] para exibir horário do barbeiro \n[ 3 ] para sair')
        while True:
            try:
                escolha = int(input('Escolha:'))
                if escolha == 1: 
                    excluirBarbeiro(cursor, conexao)
                    break
                elif escolha == 2:
                    exibirHorariosBarbeiro(cursor)
                    break
            except ValueError:
                input('Escolha uma das opções acima...')
            
    else:
        input('Não há barbeiros cadastrados! pressione enter para voltar...')


def excluirBarbeiro(cursor, conexao):
    while True:
        try:
            id_barbeiro = int(input('Digite o id do barbeiro que deseja excluir: '))

            cursor.execute('''
            SELECT id
            FROM barbeiros
            WHERE id = %s
            ''',
            (id_barbeiro,)
            )

            id_existe = cursor.fetchone()

            if id_existe:
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
                break
        except ValueError:
            input('Digite um id válido! pressione enter para tentar novamente...')


def exibirHorariosBarbeiro(cursor):
    while True:
        try:
            id_Consulta = int(input('Digite o ID do barbeiro para consultar os horarios de trabalho ou enter para sair: ').strip())

            if id_Consulta == '':
                break
            else:
                cursor.execute('''
                SELECT id
                FROM barbeiros
                WHERE id = %s
                ''',
                (id_Consulta,)
                )

                id_existe = cursor.fetchone()

                if id_existe:
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

                    if not disponibilidadeBarbeiro:
                        input('Diponíbilidade não encontrada! pressione enter e tente novamente...')
                        continue
                    coluna = [coluna[0] for coluna in cursor.description]


                    cursor.execute('''
                    SELECT *
                    FROM barbeiros
                    WHERE id = %s
                    ''',
                    (id_Consulta,)
                    )
                    nomeBarbeiro = cursor.fetchall()

                    if not nomeBarbeiro:
                        input('Nome do barbeiro não encontrado! pressione enter para voltar...')
                        continue

                    limpar_terminal()

                    titulo(f'Horários do barbeiro {nomeBarbeiro[0][1]}')

                    print(f'{coluna[1]:<20} {coluna[2]:<20} {coluna[3]:<20} {coluna[4]:<20}')
                    print('-'*85)
                    for id_barbeiro, dia_semana, horario_inicio, horario_fim, status in disponibilidadeBarbeiro:
                        inicio = horario_inicio.strftime('%H:%M')
                        final = horario_fim.strftime('%H:%M')
                        print(f'{dia_semana:<20} {inicio:<20} {final:<20} {status:<20}')
                    print('-'*85)
                    input('Pressione enter para voltar...')
                else:
                    input('Id inválido! pressione enter para voltar...')
        except ValueError:
            input('Digite um ID válido! pressione enter para voltar...')


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
        limpar_terminal()
        
        titulo('CADASTRO DE BARBEIRO')

        while True:
            nome = input('NOME: ')
            if nome.isalpha():
                cursor.execute('''
                SELECT nome
                FROM barbeiros
                WHERE nome = %s
                ''',
                (nome,)
                )

                nome_existe = cursor.fetchone()

                if nome_existe:
                    print('Nome já cadastrado!')
                else:
                    break
            else:
                print('Digite somente letras!!')
            

        while True:
            telefone = input('TELEFONE: ').replace(' ', '').replace('(', '').replace(')', '').replace('-', '').strip()
            telefone_valido = telefone.isdigit() and len(telefone) == 11
            
            if telefone_valido:
                cursor.execute('''
                SELECT telefone
                FROM barbeiros
                WHERE telefone = %s
                ''',
                (telefone,)
                )

                telefone_existe = cursor.fetchone()

                if telefone_existe:
                    print('Telefone já cadastrado!')
                else:
                    break
            else:
                print('Digite o telefone corretamente! somente números')

        while True:
            email = input('EMAIL: ').lower()
            email_valido = '@' in email and '.' in email
            if email_valido:
                cursor.execute('''
                SELECT email
                FROM barbeiros
                WHERE email = %s
                ''',
                (email,)
                )

                email_existe = cursor.fetchone()

                if email_existe:
                    print('Email já cadastrado!')
                else:
                    break
            else:
                print('Digite um email válido!!')
    
        try: 
            cursor.execute('''
            INSERT INTO barbeiros (nome, telefone, email)
            VALUES (%s, %s, %s)
            RETURNING id
            ''',
            (nome, telefone, email)
            )

        except Exception as erro:
            conexao.rollback()
            print(erro)
            input('Aconteceu um erro ao inserir os dados ao banco. Aperte enter para tentar novamente...')
            continue

        barbeiro_id =  cursor.fetchone()[0]

        try:
            for dia, inicio, fim in horario_padrao:
                cursor.execute('''
                INSERT INTO disponibilidade (id_barbeiro, dia_semana, horario_inicio, horario_fim, status)
                VALUES (%s, %s, %s, %s, %s)
                ''',
                (barbeiro_id, dia, inicio, fim, 'ativo')
                )

            conexao.commit()
            

            print('Barbeiro cadastrado com sucesso')
            input('Aperte enter para voltar...')
            break

        except Exception as erro:
            conexao.rollback()
            print(erro)
            input('Aconteceu um erro ao inserir a disponibilidade do barbeiro. Aperte enter para tentar novamente...')
