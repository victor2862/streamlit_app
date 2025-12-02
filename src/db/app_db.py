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
            
            # Criação da tabela de projetos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projetos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cliente TEXT NOT NULL,
                    descricao TEXT
                    )
            ''')
            conn.commit()

            # Criação da tabela de contextos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contextos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    projeto_id INTEGER NOT NULL,
                    contexto TEXT NOT NULL,
                    FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE
                    )
            ''')
            conn.commit()


    ### Manipulação da tabela de projetos ---------------------------------------------------------

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
    def listar_projetos(self) -> pd.DataFrame:
        with self.connect() as conn:
            df = pd.read_sql_query("SELECT * FROM projetos", conn)
            df.set_index('id', inplace=True)
            return df
        
    # Deletar um projeto pelo ID
    def deletar_projeto(self, id_projeto):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM projetos WHERE id = ?', (id_projeto,))
            conn.commit()

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


    ### Manipulação da tabela de contextos ---------------------------------------------------------

    # Adicionar um novo contexto a um projeto
    def adicionar_contexto(self, projeto_id, contexto):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO contextos (projeto_id, contexto)
                VALUES (?, ?)
            ''', (projeto_id, contexto))
            conn.commit()
    
    # Listar contextos de um projeto
    def listar_contextos(self, projeto_id) -> pd.DataFrame:
        with self.connect() as conn:
            df = pd.read_sql_query('''
                SELECT * FROM contextos WHERE projeto_id = ?
            ''', conn, params=(projeto_id,))
            df.set_index('id', inplace=True)
            return df
        
    # Obter último contexto adicionado a um projeto
    def obter_ultimo_contexto(self, projeto_id) -> str:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT contexto FROM contextos
                WHERE projeto_id = ?
                ORDER BY id DESC LIMIT 1
            ''', (projeto_id,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
    
    # Deletar um contexto pelo ID
    def deletar_contexto(self, id_contexto):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM contextos WHERE id = ?', (id_contexto,))
            conn.commit()
            
    # Inserir contextos de exemplo em markdown para um projeto específico
    def inserir_contextos_exemplo(self):
        exemplos = [
            "# Contexto de exemplo 1\nEste é o contexto inicial de exemplo 1.\n\n- Item 1\n- Item 2",
            "# Contexto de exemplo 2\nEste é o contexto inicial de exemplo 2.\n\n1. Primeiro ponto\n2. Segundo ponto",
        ]
        with self.connect() as conn:
            cursor = conn.cursor()
            contagem = cursor.execute('SELECT id FROM projetos').fetchall()
            for i in contagem:
                projeto_id = i[0]
                for contexto in exemplos: self.adicionar_contexto(projeto_id, contexto)








if __name__ == "__main__":
    db = AppDB()
    db.inicializar_banco()
    db.inserir_projetos_exemplo()
    db.inserir_contextos_exemplo()
    
    # projetos = db.listar_projetos()
    # print(projetos)