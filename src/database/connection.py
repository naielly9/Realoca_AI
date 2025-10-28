import sqlite3
import os
from database import Database
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