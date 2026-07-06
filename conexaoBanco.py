import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

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
        telefone VARCHAR(20) UNIQUE,
        email VARCHAR(100) UNIQUE
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
        data DATE
    );
    ''')

    conexao.commit()
    return cursor, conexao