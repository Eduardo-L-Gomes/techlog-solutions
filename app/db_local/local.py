import sqlite3
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.getenv("DB_PATH")

class DBLocal():
    def __init__(self, file=db_path):
        self.file = file
        self.initialize_db()

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.file)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def initialize_db(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL,
                    telefone TEXT NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL,
                    senha TEXT NOT NULL
                )
            ''')
        print("Banco de dados iniciado.")