import funcoes

funcoes.titulo('BEM VINDO AO PAINEL DO BARBEIRO')
opcoes = ['Agenda do dia', 'Agenda geral', 'Disponibilidade semanal', 'Sair']

id = input('Digite seu id de barbeiro: ')
funcoes.menuBarbeiro(opcoes, id)
