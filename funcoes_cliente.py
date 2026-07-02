import funcoes
import datetime

def mostrarHistorico(cursor):
    funcoes.limpar_terminal()

    nome = pegarNomeUsuario()

    cursor.execute('''
    SELECT *
    FROM agendamentos
    WHERE nome = %s AND status IN ('concluido', 'cancelado')
    ORDER BY data, horario_inicio
    ''',
    (nome,)
    )

def pegarNomeUsuario():
    funcoes.limpar_terminal()
    while True:
        nome = input('Digite seu nome de usuário: ').strip()

        if nome == '':
             input('Preencha o nome corretamente! aperte enter parar digitar novamente...')
        else:
            break
        


    return nome


def mostrarAgendamentos(cursor):
    while True:
        funcoes.limpar_terminal()
        nome = pegarNomeUsuario()
        cursor.execute('''
        SELECT *
        FROM agendamentos
        WHERE status = 'agendado' AND nome = %s
        ORDER BY data, horario_inicio
        ''',
        (nome,)
        )

        agendamentos = cursor.fetchall()

        if not agendamentos:
            input('Não há agendamento com esse nome! pressione enter para voltar... ')

        else:
            print(f'{'Cliente:':<15} {'Serviço:':<15} {'Horario-Inicio:':<15} {'Horario-fim:':<15} {'Barbeiro:':<15} {'Valor:':<15} {'Status:':<15} {'Data:':<15}')
            print('-'*120)
            for nome, servico, horarioInicio, horarioFim, barbeiro,  valor, status, data in agendamentos:
                print(f'{nome:<15} {servico:<15} {horarioInicio.strftime('%H:%M'):<15} {horarioFim.strftime('%H:%M'):<15} {barbeiro:<15} {valor:<15} {status:<15} {data.strftime('%d/%m/%y'):<15}')
            
            print()
            input('Pressione enter para sair..')
            break


def exibirResumoAgendamento(cursor, conexao, nomeCliente, escolhaServico, escolhaHorario, horarioFim, valor, dataCompleta, escolhaBarbeiro):
    while True:

        funcoes.limpar_terminal()
            
        funcoes.titulo('RESUMO DO AGENDAMENTO')

        print(f'data: {dataCompleta}\nserviço: {escolhaServico}\nhorário: {escolhaHorario.strftime('%H:%M')}\nbarbeiro: {escolhaBarbeiro}\nCliente: {nomeCliente}\nvalor: {valor}')

        confirmacao = int(input('Aperte [ 1 ] para confirmar ou [ 2 ] para cancelar: ').strip())
        print(confirmacao)
        if confirmacao == 1:
            cursor.execute('''
            INSERT INTO agendamentos (nome, servico, horario_inicio, horario_fim, barbeiro, valor, status, data)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''',
            (nomeCliente, escolhaServico, escolhaHorario, horarioFim, escolhaBarbeiro, valor, 'agendado', dataCompleta )
            )
            conexao.commit()
            print('AGENDAMENTO CONCLUIDO, CHEGUE com 5 minutos de antecendência!')
            break
        elif confirmacao == 2:
            print('Processo de agendamento cancelado.')
            break


def escolherHorario(cursor, escolhaBarbeiro, escolhaDiaSemana, diaAtual, dataCompleta, duracao):
     while True:
        funcoes.limpar_terminal()

        funcoes.titulo('Horários Disponiveis')
            
        cursor.execute('''
        SELECT horario_inicio, horario_fim
        FROM disponibilidade
        WHERE id_barbeiro = %s AND dia_semana = %s AND status = 'ativo'
        ''',
        (escolhaBarbeiro, escolhaDiaSemana)
        )

        disponibilidade = cursor.fetchall()
        disponibilidadeInicio = disponibilidade[0][0]
        disponibilidadeFim = disponibilidade[0][1]

        cursor.execute('''
        SELECT horario_inicio
        FROM agendamentos
        WHERE status = 'agendado' AND barbeiro = %s AND data = %s
        ''',
        (escolhaBarbeiro, dataCompleta)
        )

        horariosOcupados = cursor.fetchall()

        horariosOcupados = [horario[0].strftime('%H:%M') for horario in horariosOcupados]


        horarios = {
            'manha' : [],
            'tarde' : [],
            'noite' : []
        }

        inicio = datetime.datetime.combine(diaAtual, disponibilidadeInicio)
        fim = datetime.datetime.combine(diaAtual, disponibilidadeFim)
            
        while inicio < fim:
            hora = inicio.hour
            horario_formatado = inicio.strftime('%H:%M')
            if hora < 12:
                if horario_formatado in horariosOcupados:
                    pass
                else:
                    horarios['manha'].append(inicio.strftime('%H:%M'))
            elif hora < 18:
                if horario_formatado in horariosOcupados:
                    pass
                else:
                    horarios['tarde'].append(inicio.strftime('%H:%M'))
            else:
                if horario_formatado in horariosOcupados:
                    pass
                else:
                    horarios['noite'].append(inicio.strftime('%H:%M'))

            inicio += datetime.timedelta(minutes=30)
            
        todosHorarios = horarios['manha'] + horarios['tarde'] + horarios['noite'] 
            
        print('manhã')
        for i, horario in enumerate(horarios['manha'], start=1):
            print(f'{horario} ', end='' if i % 2 != 0 else '\n')
            
        print()
        print('-'*85)

        print('tarde')
        for i, horario in enumerate(horarios['tarde'], start=1):
            print(f'{horario} ', end='' if i % 2 != 0 else '\n')

        print()
        print('-'*85)

        print('noite')
        for i, horario in enumerate(horarios['noite'], start=1):
            print(f'{horario} ', end='' if i % 2 != 0 else '\n')

        print()
        print('-'*85)

        escolhaHorarioTexto = input('Escolha um dos horarios acima: ').strip()

        escolhaHorario = datetime.datetime.strptime(escolhaHorarioTexto, ('%H:%M')).time()

        horarioInicio = datetime.datetime.combine(dataCompleta, escolhaHorario)
        horarioFim = horarioInicio + datetime.timedelta(minutes=duracao)
        horarioFim = horarioFim.time()

        if escolhaHorarioTexto not in todosHorarios:
            print(escolhaHorarioTexto, horarios)
            input('Escolha um dos horarios que aparecem acima! aperte enter para escolher novamente...')
            
        else:
            return escolhaHorario, horarioFim
            break

        
def escolherServico(cursor):
    while True:
            funcoes.limpar_terminal()

            funcoes.titulo('Escolha o serviço desejado')

            cursor.execute('''
            SELECT nome, valor, duracao
            FROM servicos
            ''')


            servicosDisponiveis = cursor.fetchall()


            coluna = [coluna[0] for coluna in cursor.description]

            listaDeServico = []

            print(f'{coluna[0]:<20} {coluna[1]:<20}')
            for servico in servicosDisponiveis:
                print(f'{servico[0]:<20} {servico[1]:<20}')
                listaDeServico.append(servico[0])
            
            escolhaServico = str(input('Digite o nome do serviço desejado: ').strip())

            cursor.execute('''
            SELECT valor, duracao
            from servicos
            where nome = %s
            ''',
            (escolhaServico,)
            )

            resultado = cursor.fetchone()
            valor, duracao = resultado

            if escolhaServico in listaDeServico:
                break
            else:
                input('Digite um serviço valido! pressione enter para escolher novamente.')

    return escolhaServico, duracao, valor


def escolherData():
    while True:
            funcoes.limpar_terminal()

            funcoes.titulo('DIAS DISPONIVEIS')
            
            diaAtual = datetime.date.today()

            diasDaSemana = [
                'segunda',
                'terca',
                'quarta',
                'quinta',
                'sexta',
                'sabado',
                'domingo'
            ]
            diasDisponiveis = []
            for i, dia in enumerate(range(7)):
                dia = diaAtual + datetime.timedelta(days=i)
                print(f"{dia.strftime('%d'):<5}  {diasDaSemana[dia.weekday()]:<10} [{i}]")
                diasDisponiveis.append(dia.day)

            print('-'*85)


            
            try:
                escolhaData = int(input('Digite o indicie do número que deseja agendar: ').strip())
                dataCompleta =  datetime.date.today() + datetime.timedelta(days=escolhaData)
                escolhaDiaSemana = diasDaSemana[dataCompleta.weekday()]
            
                if escolhaData > 6  or escolhaData < 0:
                    input('Digite um dos indice acima! aperte enter para escolher novamente')
                else:
                    break
            except ValueError:
                input('Digite apenas o número do dia que deseja agendar! pressione enter para escolher novamente...')

    return dataCompleta, escolhaDiaSemana, diaAtual


def escolherBarbeiro(cursor):
    cursor.execute('''
        SELECT *
        FROM barbeiros
        ''')

    barbeiros =  cursor.fetchall()
    informacoesColuna = [coluna[0] for coluna in cursor.description]

    funcoes.limpar_terminal()

    funcoes.titulo('BARBEIROS DISPONIVEIS')

    print(f'{informacoesColuna[0]:<30} {informacoesColuna[1]:<30}')
    for id_barbeiro, nome_barbeiro, _, _ in barbeiros:
        print(f'{id_barbeiro:<30} {nome_barbeiro:<30}')
    print('-'*85)
        
    escolhaBarbeiro = input('Digite o ID do barbeiro desejado: ').strip()

    return escolhaBarbeiro