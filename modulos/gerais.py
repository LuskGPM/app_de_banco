import sqlite3
import bcrypt
from tkinter import messagebox


class FuncoesGerais():
    
    @staticmethod
    def verificar_senha(senha_fornecida, senha_armazenada):
        try:
            if bcrypt.checkpw(senha_fornecida.encode('utf-8'), senha_armazenada):
                return True
            else:
                return False
        except ValueError as erro:
            print(f'Erro ao verificar senha: {erro}')
            return False
        
    @staticmethod
    def validar_senha(entry_cpf, entry_senha, banco):
        try:
            cpf = entry_cpf.get()
            senha = entry_senha.get()

            # Busca a senha armazenada no banco de dados
            senha_armazenada = banco.buscar_senha(cpf)

            if senha_armazenada:
                # Verifica a senha usando a função verificar_senha
                if FuncoesGerais.verificar_senha(senha, senha_armazenada):
                    messagebox.showinfo("Sucesso", "Senha correta!")
                else:
                    messagebox.showerror("Erro", "Senha incorreta!")
            else:
                messagebox.showerror("Erro", "CPF não encontrado!")
        except Exception as erro:
            print(f"Erro ao validar senha: {erro}")
            
    @staticmethod
    def formatar_cpf(cpf, esconder=False):
        """Formata o CPF para exibir ou esconder os 6 números centrais."""
        return f"{cpf[:3]}.***.***-{cpf[-2:]}" if esconder else f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    
    @staticmethod
    def esconder_cartao(numero_cartao):
        """Formata o número do cartão para exibir apenas os 4 primeiros e os 4 últimos dígitos."""
        return f"{numero_cartao[:4]} **** **** {numero_cartao[-4:]}"
    
    @staticmethod
    def formatar_cartao(numero_cartao):
        """Formata o número do cartão para exibir com espaços."""
        return f"{numero_cartao[:4]} {numero_cartao[4:8]} {numero_cartao[8:12]} {numero_cartao[12:]}"
            