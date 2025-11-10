import sqlite3
import os
from database import Database
import pandas as pd

DB_NAME = "realoca_ai.db"

def get_connection():
    db = Database()
    if not os.path.exists(DB_NAME):
        print(f"Banco '{DB_NAME}' não encontrado. Criando novo banco...")
        conn = sqlite3.connect(DB_NAME)
        db.criar_tabelas()
        print(f"Tabelas criadas")
    else:
        conn = sqlite3.connect(DB_NAME)
    return conn

def get_employees():
    query = """
        SELECT e.id, e.nome, en.logradouro, en.numero, b.nome AS bairro,
               c.nome AS cidade, es.sigla AS estado, en.cep
        FROM funcionarios e
        JOIN enderecos en ON e.endereco_id = en.id
        JOIN bairros b ON en.bairro_id = b.id
        JOIN cidades c ON en.cidade_id = c.id
        JOIN estados es ON c.estado_id = es.id
    """
    return pd.read_sql_query(query, get_connection())

def get_branches():
    query = """
        SELECT f.id, f.nome, en.logradouro, en.numero, b.nome AS bairro,
               c.nome AS cidade, es.sigla AS estado, en.cep
        FROM filiais f
        JOIN enderecos en ON f.endereco_id = en.id
        JOIN bairros b ON en.bairro_id = b.id
        JOIN cidades c ON en.cidade_id = c.id
        JOIN estados es ON c.estado_id = es.id
    """
    return pd.read_sql_query(query, get_connection())