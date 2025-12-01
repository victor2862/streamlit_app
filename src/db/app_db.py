# Importações
import sqlite3 as sql
import pandas as pd


# Definição da classe AppDB
class AppDB:

    # Método de conexão com o banco de dados
    def connect(self):
        return sql.connect('src/db/app.db')

    # Inicialização do banco de dados
    def inicializar_banco(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projetos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cliente TEXT NOT NULL,
                    descricao TEXT
                    )
            ''')
            conn.commit()

    # Adicionar um novo projeto
    def adicionar_projeto(self, nome, cliente, descricao):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO projetos (nome, cliente, descricao)
                VALUES (?, ?, ?)
            ''', (nome, cliente, descricao))
            conn.commit()

    # Listar todos os projetos
    def listar_projetos(self):
        with self.connect() as conn:
            df = pd.read_sql_query("SELECT * FROM projetos", conn)
            df.set_index('id', inplace=True)
            return df

    # Inserir projetos de exemplo caso a base esteja vazia
    def inserir_projetos_exemplo(self):
        exemplos = [
            ("Projeto A", "Cliente X", "Descrição do Projeto A"),
            ("Projeto B", "Cliente Y", "Descrição do Projeto B"),
            ("Projeto C", "Cliente Z", ""),
        ]
        with self.connect() as conn:
            cursor = conn.cursor()
            contagem = cursor.execute('SELECT COUNT(*) FROM projetos').fetchone()[0]
            if not contagem:
                cursor.executemany('''
                    INSERT INTO projetos (nome, cliente, descricao)
                    VALUES (?, ?, ?)
                ''', exemplos)
                conn.commit()


if __name__ == "__main__":
    db = AppDB()
    db.inicializar_banco()
    db.inserir_projetos_exemplo()
    projetos = db.listar_projetos()
    print(projetos)