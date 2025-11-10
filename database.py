import sqlite3
import pandas as pd

class Database:
    def __init__(self, db_path="realoca_ai.db"):
        self.db_path = db_path
        self.criar_tabelas()

    def conectar(self):
        return sqlite3.connect(self.db_path)

    def execute(self, query, params=(), fetchone=False, fetchall=False, commit=False):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute(query, params)

        result = None
        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()

        if commit:
            conn.commit()

        conn.close()
        return result
    
    def criar_tabelas(self):
        conn = self.conectar()
        cursor = conn.cursor()

        # Usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                nome TEXT
            )
        """)

        #Estado
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                sigla TEXT NOT NULL UNIQUE
            )
        """)

        # Cidades
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cidades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                estado_id INTEGER NOT NULL,
                UNIQUE(nome, estado_id),
                FOREIGN KEY (estado_id) REFERENCES estados (id)
            )
        """)

        # Tipos de transporte (municipal/intermunicipal)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tipos_transporte (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT UNIQUE NOT NULL
            )
        """)

        # Linhas de ônibus
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS linhas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT NOT NULL,
                nome TEXT NOT NULL,
                tarifa REAL NOT NULL,
                cidade_origem_id INTEGER,
                cidade_destino_id INTEGER,
                tipo_transporte_id INTEGER,
                FOREIGN KEY (cidade_origem_id) REFERENCES cidades (id),
                FOREIGN KEY (cidade_destino_id) REFERENCES cidades (id),
                FOREIGN KEY (tipo_transporte_id) REFERENCES tipos_transporte (id)
            )
        """)

        # Bairros
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bairros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_bairro TEXT NOT NULL,
                cidade_id INTEGER NOT NULL,
                FOREIGN KEY (cidade_id) REFERENCES cidades (id),
                UNIQUE(nome_bairro, cidade_id)
            )
        """)

        # Endereços
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enderecos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                logradouro TEXT,
                numero TEXT,
                id_bairro INTEGER NOT NULL,
                cep TEXT,
                latitude REAL,
                longitude REAL,
                FOREIGN KEY (id_bairro) REFERENCES bairros (id)
            )
        """)


        # Filiais
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS filiais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_filial TEXT NOT NULL,
                id_endereco INTEGER,
                FOREIGN KEY (id_endereco) REFERENCES enderecos (id)
            )
        """)

        # Funcionários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                id_endereco INTEGER,
                id_filial INTEGER,
                mt TEXT UNIQUE,            
                centro_custo TEXT, 
                ativo INTEGER DEFAULT 1,
                FOREIGN KEY (id_endereco) REFERENCES enderecos (id),
                FOREIGN KEY (id_filial) REFERENCES filiais (id)
            )
        """)

        # Rotas por bairro (bairro - filial - linha)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rotas_bairro (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_bairro INTEGER NOT NULL,              -- Bairro de origem (do funcionário)
                id_filial INTEGER NOT NULL,              -- Filial de destino
                id_linha INTEGER,                        -- Linha de transporte utilizada
                distancia_km REAL,
                tempo_estimado_min INTEGER,
                custo_estimado REAL,
                ordem INTEGER,                           -- 1ª, 2ª ou 3ª melhor rota
                FOREIGN KEY (id_bairro) REFERENCES bairros (id),
                FOREIGN KEY (id_filial) REFERENCES filiais (id),
                FOREIGN KEY (id_linha) REFERENCES linhas (id)
            )
        """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_func_endereco ON funcionarios(id_endereco)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_func_filial ON funcionarios(id_filial)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_rotas_bairro_bairro ON rotas_bairro(id_bairro)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_rotas_bairro_filial ON rotas_bairro(id_filial)")


        conn.commit()
        conn.close()

    def validar_usuario(self, username, senha):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM usuarios WHERE username=? AND senha=?", (username, senha))
        result = cursor.fetchone()
        conn.close()
        return result

    def cadastrar_usuario(self, username, senha, nome):
        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (username, senha, nome) VALUES (?, ?, ?)", (username, senha, nome))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def obter_id_cidade(self, nome):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM cidades WHERE nome=?", (nome,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None  
    def get_or_create_estado(self, nome, sigla):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM estados WHERE sigla = ?", (sigla,))
        estado = cursor.fetchone()
        if estado:
            estado_id = estado[0]
        else:
            cursor.execute("INSERT INTO estados (nome, sigla) VALUES (?, ?)", (nome, sigla))
            estado_id = cursor.lastrowid
            conn.commit()
        conn.close()
        return estado_id

    def get_or_create_cidade(self, nome, estado_id):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM cidades WHERE nome = ? AND estado_id = ?", (nome, estado_id))
        cidade = cursor.fetchone()
        if cidade:
            cidade_id = cidade[0]
        else:
            cursor.execute("INSERT INTO cidades (nome, estado_id) VALUES (?, ?)", (nome, estado_id))
            cidade_id = cursor.lastrowid
            conn.commit()
        conn.close()
        return cidade_id

    def get_or_create_bairro(self, nome_bairro, cidade_id):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM bairros WHERE nome_bairro = ? AND cidade_id = ?", (nome_bairro, cidade_id))
        bairro = cursor.fetchone()
        if bairro:
            bairro_id = bairro[0]
        else:
            cursor.execute("INSERT INTO bairros (nome_bairro, cidade_id) VALUES (?, ?)", (nome_bairro, cidade_id))
            bairro_id = cursor.lastrowid
            conn.commit()
        conn.close()
        return bairro_id

    def get_or_create_endereco(self, logradouro, numero, cep, bairro_id):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM enderecos
            WHERE logradouro = ? AND numero = ? AND id_bairro = ? AND cep = ?
        """, (logradouro, numero, bairro_id, cep))
        end = cursor.fetchone()
        if end:
            end_id = end[0]
        else:
            cursor.execute("""
                INSERT INTO enderecos (logradouro, numero, id_bairro, cep)
                VALUES (?, ?, ?, ?)
            """, (logradouro, numero, bairro_id, cep))
            end_id = cursor.lastrowid
            conn.commit()
        conn.close()
        return end_id

    def get_or_create_filial(self, nome_filial, id_endereco):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM filiais WHERE nome_filial = ?", (nome_filial,))
        filial = cursor.fetchone()
        if filial:
            filial_id = filial[0]
        else:
            cursor.execute("INSERT INTO filiais (nome_filial, id_endereco) VALUES (?, ?)", (nome_filial, id_endereco))
            filial_id = cursor.lastrowid
            conn.commit()
        conn.close()
        return filial_id

    def get_or_create_tipo_transporte(self, tipo: str):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tipos_transporte WHERE tipo = ?", (tipo,))
        result = cursor.fetchone()
        if result:
            tipo_id = result[0]
        else:
            cursor.execute("INSERT INTO tipos_transporte (tipo) VALUES (?)", (tipo,))
            tipo_id = cursor.lastrowid
            conn.commit()
        conn.close()
        return tipo_id
    
    def cadastrar_funcionario(self, nome, id_endereco, id_filial, mt=None, centro_custo=None):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO funcionarios (nome, id_endereco, id_filial, mt, centro_custo)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, id_endereco, id_filial, mt, centro_custo))
        conn.commit()
        conn.close()

    def get_or_create_funcionario(self, nome, id_endereco, id_filial, mt=None, centro_custo=None):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM funcionarios WHERE mt = ?
        """, (mt,))
        resultado = cursor.fetchone()

        if resultado:
            funcionario_id = resultado[0]
            cursor.execute("""
                UPDATE funcionarios
                SET id_endereco = ?, id_filial = ?, centro_custo = ?, nome = ?
                WHERE id = ?
            """, (id_endereco, id_filial, centro_custo, nome, funcionario_id))
            conn.commit()
            conn.close()
            return funcionario_id 
        
        cursor.execute("""
            INSERT INTO funcionarios (nome, id_endereco, id_filial, mt, centro_custo)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, id_endereco, id_filial, mt, centro_custo))
        conn.commit()

        funcionario_id = cursor.lastrowid
        conn.close()
        return funcionario_id

    def get_funcionarios_por_mt(self, lista_mt):
        conn = self.conectar()
        cursor = conn.cursor()

        placeholders = ', '.join(['?'] * len(lista_mt))

        query = f"""
            SELECT f.id, f.nome,f.id_endereco,f.id_filial,f.mt,f.centro_custo
            FROM funcionarios f
            JOIN enderecos e ON f.id_endereco = e.id
            JOIN filiais fi ON f.id_filial = fi.id
            WHERE f.mt IN ({placeholders}) AND f.ativo = 1
        """

        cursor.execute(query, lista_mt)
        rows = cursor.fetchall()

        conn.close()
        return rows
    
    def get_filiais(self) -> pd.DataFrame:
        """Retorna todas as filiais com latitude, longitude e cidade."""
        conn = self.conectar()
        query = """
            SELECT f.id, f.nome_filial, e.latitude, e.longitude, c.nome AS cidade
            FROM filiais f
            JOIN enderecos e ON f.id_endereco = e.id
            JOIN bairros b ON e.id_bairro = b.id
            JOIN cidades c ON c.id = b.cidade_id
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def get_funcionarios(self) -> pd.DataFrame:
        """Retorna todos os funcionários com endereço, filial e cidade."""
        conn = self.conectar()
        query = """
            SELECT func.id, func.nome, func.ativo, func.centro_custo, func.mt,
                   f.nome_filial, e.latitude, e.longitude, c.nome AS cidade
            FROM funcionarios func
            LEFT JOIN filiais f ON f.id = func.id_filial
            LEFT JOIN enderecos e ON e.id = func.id_endereco
            LEFT JOIN bairros b ON b.id = e.id_bairro
            LEFT JOIN cidades c ON c.id = b.cidade_id
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    def deletar_funcionarios_sem_filial(self):
        """Deleta todos os funcionários que não possuem filial associada."""
        conn = self.conectar()
        cursor = conn.cursor()

        # Primeiro, exibe quantos serão removidos (para controle)
        cursor.execute("""
            SELECT COUNT(*) 
            FROM funcionarios 
            WHERE id_filial IS NULL
            OR id_filial NOT IN (SELECT id FROM filiais);
        """)
        qtd = cursor.fetchone()[0]

        if qtd > 0:
            # Executa o delete
            cursor.execute("""
                DELETE FROM funcionarios
                WHERE id_filial IS NULL
                OR id_filial NOT IN (SELECT id FROM filiais);
            """)
            conn.commit()
            print(f"✅ {qtd} funcionário(s) sem filial foram deletados com sucesso.")
        else:
            print("ℹ️ Nenhum funcionário sem filial encontrado.")

        conn.close()
