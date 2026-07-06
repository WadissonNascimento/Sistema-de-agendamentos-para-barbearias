import menus.menuAdmin as menuAdmin
import datetime
from conexaoBanco import conexaoBanco
from uteis import limpar_terminal, titulo



def mostrarHistorico():
    cursor, conexao = conexaoBanco()
    limpar_terminal()

    nome = pegarNomeUsuario()

    cursor.execute('''
    SELECT *
    FROM agendamentos
    WHERE nome = %s AND status IN ('concluido', 'cancelado')
    ORDER BY data, horario_inicio
    ''',
    (nome,)
    )

    historico = cursor.fetchall()


    print(f'{'Cliente:':<15} {'Serviço:':<15} {'Horario-Inicio:':<15} {'Horario-fim:':<15} {'Barbeiro:':<15} {'Valor:':<15} {'Status:':<15} {'Data:':<15}')
    print('-'*120)

    if not historico:
        input('Não há histórico disponivel, pressioe enter para voltar...')

    else:
        for nome, servico, horarioInicio, horarioFim, barbeiro,  valor, status, data in historico:
            print(f'{nome:<15} {servico:<15} {horarioInicio.strftime('%H:%M'):<15} {horarioFim.strftime('%H:%M'):<15} {barbeiro:<15} {valor:<15} {status:<15} {data.strftime('%d/%m/%y'):<15}')

def pegarNomeUsuario():
    limpar_terminal()
    while True:
        nome = input('Digite seu nome de usuário: ').strip()

        if nome == '':
             input('Preencha o nome corretamente! aperte enter parar digitar novamente...')
        else:
            break
        


    return nome


def mostrarAgendamentos(cursor):
    while True:
        menuAdmin.limpar_terminal()
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

        limpar_terminal()
            
        titulo('RESUMO DO AGENDAMENTO')

        print(f'{'data:':<10} {dataCompleta.strftime('%D/%M')}\n{'serviço:':<10} {escolhaServico}\n{'horário:':<10} {escolhaHorario.strftime('%H:%M')}\n{'barbeiro:':<10} {escolhaBarbeiro}\n{'Cliente:':<10} {nomeCliente}\n{'valor:':<10} {valor}')

        confirmacao = int(input('Aperte [ 1 ] para confirmar ou [ 2 ] para cancelar: ').strip())
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
        else:
            input('Selecione uma das opções acima! pressione enter para escolher novamente...')


def escolherHorario(cursor, escolhaBarbeiro, escolhaDiaSemana, diaAtual, dataCompleta, duracao):
     while True:
        limpar_terminal()

        titulo('Horários Disponiveis')
            
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
        if not disponibilidade:
            input('Esse barbeiro não possui dias disponíveis')
            continue

        cursor.execute('''
        SELECT horario_inicio, horario_fim
        FROM agendamentos
        WHERE status = 'agendado' AND barbeiro = %s AND data = %s
        ''',
        (escolhaBarbeiro, dataCompleta)
        )

        horariosOcupados = cursor.fetchall()

        horarios = {
            'manha' : [],
            'tarde' : [],
            'noite' : []
        }

        inicio = datetime.datetime.combine(diaAtual, disponibilidadeInicio)
        fim = datetime.datetime.combine(diaAtual, disponibilidadeFim)
        

        while inicio < fim:
            horario_ocupado = False
            hora = inicio.hour
            horario_formatado = inicio.strftime('%H:%M')
            novo_fim = inicio + datetime.timedelta(minutes=duracao)
            for inicio_ocupado, fim_ocupado in horariosOcupados:
                inicio_ocupado = datetime.datetime.combine(dataCompleta, inicio_ocupado)
                fim_ocupado = datetime.datetime.combine(dataCompleta, fim_ocupado)

                if inicio < fim_ocupado and novo_fim > inicio_ocupado:
                    horario_ocupado = True
                    break
            if novo_fim > fim:
                horario_ocupado = True
        
            if not horario_ocupado:
                if hora < 12:
                    horarios['manha'].append(horario_formatado)
                elif hora < 18:
                    horarios['tarde'].append(horario_formatado)
                else:
                    horarios['noite'].append(horario_formatado)


            inicio += datetime.timedelta(minutes=10)
            
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

        try:
            escolhaHorarioTexto = input('Escolha um dos horarios acima: ').strip()

            escolhaHorario = datetime.datetime.strptime(escolhaHorarioTexto, ('%H:%M')).time()

            horarioInicio = datetime.datetime.combine(dataCompleta, escolhaHorario)
            horarioFim = horarioInicio + datetime.timedelta(minutes=duracao)
            horarioFim = horarioFim.time()

            if escolhaHorarioTexto not in todosHorarios:
                input('Escolha um dos horarios que aparecem acima! aperte enter para escolher novamente...')
                
            else:
                return escolhaHorario, horarioFim
        except ValueError:
            input('Digite um dos horários mostrados acima!!')

        
def escolherServico(cursor, conexao):
    while True:
            menuAdmin.limpar_terminal()

            menuAdmin.titulo('Escolha o serviço desejado')

            cursor.execute('''
            SELECT nome, valor, duracao
            FROM servicos
            ''')


            servicosDisponiveis = cursor.fetchall()


            if not servicosDisponiveis:
                input('Nenhum serviço cadastrado! pressione enter para voltar...')
                break

            coluna = [coluna[0] for coluna in cursor.description]

            listaDeServico = []

            print(f'{coluna[0]:<20} {coluna[1]:<20}')
            for servico in servicosDisponiveis:
                print(f'{servico[0]:<20} {servico[1]:<20}')
                listaDeServico.append(servico[0])
            
            escolhaServico = input('Digite o nome do serviço desejado: ').strip()

            cursor.execute('''
            SELECT valor, duracao
            from servicos
            where nome = %s
            ''',
            (escolhaServico,)
            )

            resultado = cursor.fetchone()

            if not resultado:
                input('Digite um dos serviços acima!! pressione enter para escolher novamente...')
                conexao.rollback()
                continue
            valor, duracao = resultado

            if escolhaServico in listaDeServico:
                break
            else:
                input('Digite um serviço valido! pressione enter para escolher novamente.')

    return escolhaServico, duracao, valor


def escolherData():
    while True:
            limpar_terminal()

            titulo('DIAS DISPONIVEIS')
            
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

    if not barbeiros:
        input('Não há barbeiros disponíveis! pressione enter para voltar...')
    else:
        informacoesColuna = [coluna[0] for coluna in cursor.description]

        id_barbeiros = []

        limpar_terminal()

        titulo('BARBEIROS DISPONIVEIS')

        print(f'{informacoesColuna[0]:<75} {informacoesColuna[1]}')
        for id_barbeiro, nome_barbeiro, _, _ in barbeiros:
            id_barbeiros.append(id_barbeiro)
            print(f'{id_barbeiro:<75} {nome_barbeiro}')
        print('-'*85)
        
        while True:
            try:
                escolhaBarbeiro = int(input('Digite o ID do barbeiro desejado: ').strip())

                if escolhaBarbeiro not in id_barbeiros:
                    input('ID inválido, pressione enter e digite novamente...')
                    print(id_barbeiros)
                else:
                    break
            except ValueError:
                print('Digite apenas números!')
        

    return escolhaBarbeiro