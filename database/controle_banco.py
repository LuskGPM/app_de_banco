import sqlite3
import os
import random
from datetime import datetime, timedelta
import bcrypt

class Banco_de_dados:
    
    def __init__(self):
        self.__con = self._conectar_banco()
        self.__cursor = self.__con.cursor()
        self.__logado = self.set_logado
              
    def set_logado(self, logado:bool = False) -> bool:
        self.__logado = logado
        
    def get_logado(self):
        return self.__logado
    
    def get_conexao(self):
        return self.__con
    
    def get_cursor(self):
        return self.__cursor
        
    def criar_tabelas(self):
        try:
            self.get_cursor().execute("""CREATE TABLE if not exists Clientes (
                cpf text PRIMARY KEY,
                nome TEXT NOT NULL,
                senha TEXT NOT NULL
                )""")
            self.get_cursor().execute("""CREATE TABLE IF NOT EXISTS Contas (
                id_conta INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf TEXT NOT NULL,
                saldo REAL NOT NULL DEFAULT 0,
                numero_cartao TEXT UNIQUE NOT NULL,
                codigo_de_segurança_do_cartao TEXT NOT NULL,
                data_de_validade_do_cartao TEXT NOT NULL,
                FOREIGN KEY (cpf) REFERENCES Clientes (cpf) ON DELETE CASCADE ON UPDATE CASCADE,
                UNIQUE (cpf)
                )""")
        except sqlite3.OperationalError as erro:
            print(f'Erro ao criar tabelas: {erro}')
            
    def _conectar_banco(self):
        try:
            caminho_database = os.path.join(os.path.dirname(__file__), 'data', 'banco_de_dados.db')
            os.makedirs(os.path.dirname(caminho_database), exist_ok=True)
            conexao = sqlite3.connect(caminho_database)
            self.banco_conectado = True
            return conexao
        except sqlite3.OperationalError as erro:
            print(f'Erro ao conectar no banco de dados: {erro}')
            raise

class GerenciamentoBanco(Banco_de_dados):
    
    def __init__(self):
        super().__init__()
    
    # Métodos de gerenciamento de clientes
    def cadastrar_cliente(self, cpf, nome, senha):
        try:
            Banco_de_dados.criar_tabelas(self)  # Garante que as tabelas existem
            senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            self.get_cursor().execute("INSERT INTO Clientes (cpf, nome, senha) VALUES (?, ?, ?)", (cpf, nome, senha_criptografada))
            self.get_conexao().commit()

            self.criar_conta(cpf)
            print(f"Cliente {nome} cadastrado com sucesso e conta criada!")
        except sqlite3.IntegrityError:
            print(f"Erro: O CPF {cpf} já está cadastrado.")
        except sqlite3.Error as erro:
            print(f"Erro ao cadastrar cliente: {erro}")
    
    def _gerar_numero_cartao(self):
        try:
            while True:
                # Gera um número de 16 dígitos
                numero_cartao = ''.join([str(random.randint(0, 9)) for _ in range(16)])

                # Verifica se o número já existe no banco de dados
                self.get_cursor().execute("SELECT 1 FROM Contas WHERE numero_cartao = ?", (numero_cartao,))
                if not self.get_cursor().fetchone():  # Se não existir, retorna o número
                    return numero_cartao
        except sqlite3.Error as erro:
            print(f'Erro ao gerar número do cartão: {erro}')
    
    def _gerar_codigo_seguranca(self, numero_cartao):
        try:
            while True:
                codigo_seguranca = ''.join([str(random.randint(0, 9)) for _ in range(3)])
                self.get_cursor().execute(
                    "SELECT 1 FROM Contas WHERE numero_cartao = ? AND codigo_de_segurança_do_cartao = ?",
                    (numero_cartao, codigo_seguranca)
                )
                if not self.get_cursor().fetchone():
                    return codigo_seguranca
        except sqlite3.Error as erro:
            print(f'Erro ao gerar código de segurança: {erro}')
    
    def _calcular_data_validade_cartao(self):
        data_atual = datetime.now()
        data_validade = data_atual + timedelta(days=365*5)
        return data_validade.strftime('%d-%m-%Y')
    
    def criar_conta(self, cpf):
        try:
            numero_cartao = self._gerar_numero_cartao()
            codigo_seguranca = self._gerar_codigo_seguranca(numero_cartao)
            data_validade = self._calcular_data_validade_cartao()
            
            self.get_cursor().execute("""INSERT INTO Contas (cpf, numero_cartao, codigo_de_segurança_do_cartao, data_de_validade_do_cartao)
                                    VALUES (?, ?, ?, ?)""", (cpf, numero_cartao, codigo_seguranca, data_validade))
            self.get_conexao().commit()
            print(f"Conta criada com sucesso para o CPF {cpf}.")
        except sqlite3.IntegrityError:
            print(f"Erro: O CPF {cpf} já possui uma conta.")
        except sqlite3.Error as erro:
            print(f"Erro ao criar conta: {erro}")
            
    def buscar_senha(self, cpf):
        try:
            # Busca a senha no banco de dados
            self.get_cursor().execute("SELECT senha FROM Clientes WHERE cpf = ?", (cpf,))
            resultado = self.get_cursor().fetchone()
            if resultado:
                return resultado[0]  # Retorna o hash da senha
            else:
                return None  # CPF não encontrado
        except sqlite3.Error as erro:
            print(f"Erro ao buscar senha: {erro}")
            return None
        
    def buscar_dados_como_dicionario(self, cpf):
        try:
            # Busca todos os dados do cliente no banco de dados
            self.get_cursor().execute("SELECT * FROM Clientes WHERE cpf = ?", (cpf,))
            resultado = self.get_cursor().fetchone()

            # Verifica se o cliente foi encontrado
            if resultado:
                # Mapeia os dados para um dicionário
                colunas = [col[0] for col in self.get_cursor().description]  # Obtém os nomes das colunas
                dados = dict(zip(colunas, resultado))  # Cria um dicionário com os nomes das colunas como chaves
                return dados
            else:
                return None  # CPF não encontrado
        except sqlite3.Error as erro:
            print(f"Erro ao buscar dados: {erro}")
            return None
        
    def buscar_dados_conta(self, cpf):
        try:
            # Busca todos os dados da conta no banco de dados
            self.get_cursor().execute("SELECT * FROM Contas WHERE cpf = ?", (cpf,))
            resultado = self.get_cursor().fetchone()

            # Verifica se a conta foi encontrada
            if resultado:
                # Mapeia os dados para um dicionário
                colunas = [col[0] for col in self.get_cursor().description]  # Obtém os nomes das colunas
                dados = dict(zip(colunas, resultado))  # Cria um dicionário com os nomes das colunas como chaves
                return dados
            else:
                return None  # Conta não encontrada
        except sqlite3.Error as erro:
            print(f"Erro ao buscar dados da conta: {erro}")
            return None

