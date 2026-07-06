# Sistema de Agendamentos para Barbearias

Este é um projeto pessoal de estudos desenvolvido com **Python** e **PostgreSQL**.

Iniciei este projeto com o objetivo de aprofundar meus conhecimentos em Python e dar meus primeiros passos com banco de dados. Escolhi desenvolver um sistema de agendamentos porque, recentemente, participei do desenvolvimento de um site de agendamentos para duas barbearias com o auxílio de IA.

Embora tenha participado ativamente do planejamento, da correção de bugs, da implementação de lógicas e da criação de novas funcionalidades para melhorar a experiência dos usuários, senti que ainda precisava compreender melhor como tudo funcionava por trás da aplicação. Eu havia adquirido bastante conhecimento durante esse processo, mas queria construir um sistema com mais autonomia, entendendo cada etapa do desenvolvimento.

Antes deste projeto, concluí o curso de Python do Curso em Vídeo e um curso de Cisco Networking pela faculdade. A partir disso, decidi criar este sistema como uma forma prática de consolidar meus conhecimentos em Python, aprender PostgreSQL e compreender a lógica envolvida em um sistema real de agendamentos.

## Dificuldades e aprendizados

Durante o desenvolvimento, enfrentei diversos desafios. Um dos principais foi trabalhar com a biblioteca `datetime`, especialmente na manipulação de datas, horários e disponibilidade em um sistema de agendamentos.

Como também era meu primeiro contato com banco de dados, levei algum tempo para entender os comandos SQL e aprender a manipular corretamente os dados retornados pelas consultas.

Outro aprendizado importante foi a importância da organização do código. No início, deixei a modularização e o tratamento de erros para depois, acreditando que poderia organizá-los ao final do projeto. Essa decisão acabou dificultando a manutenção, pois precisei revisar grande parte do código linha por linha para reorganizar a estrutura. Apesar disso, essa experiência me mostrou, na prática, a importância de planejar a arquitetura do projeto desde o início e de manter o código organizado durante todo o desenvolvimento.


## Funcionalidades Cliente

- Escolher um barbeiro disponível
- Escolher a data do atendimento
- Visualizar os serviços cadastrados
- Escolher o serviço desejado
- Visualizar horários disponíveis
- Realizar um agendamento
- Consultar agendamentos ativos
- Consultar histórico de atendimentos concluídos ou cancelados

## Funcionalidades Barbeiro

- Informar o ID do barbeiro para acessar o painel
- Visualizar a agenda do dia
- Consultar a agenda por data
- Concluir atendimentos
- Cancelar atendimentos
- Visualizar a disponibilidade semanal
- Alterar horário de início do expediente
- Alterar horário de fim do expediente
- Ativar ou desativar dias de atendimento

## Funcionalidades Admin

- Cadastrar barbeiros
- Validar nome, telefone e e-mail no cadastro
- Impedir cadastro duplicado de telefone e e-mail
- Visualizar barbeiros cadastrados
- Excluir barbeiros da equipe
- Consultar horários de trabalho dos barbeiros
- Visualizar a agenda geral
- Concluir atendimentos pela agenda geral
- Cancelar atendimentos pela agenda geral