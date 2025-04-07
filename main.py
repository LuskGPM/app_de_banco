from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QApplication
)
from database.controle_banco import GerenciamentoBanco
from modulos.gerais import FuncoesGerais 
from transacao import JanelaTransferencia  
from depositar import JanelaDeposito  
from saque import JanelaSaque  

class TelaPrincipal(QWidget):
    def __init__(self, cpf):
        super().__init__()
        self.setWindowTitle("Tela Principal")
        self.setGeometry(400, 300, 800, 600)

        # Instancia o banco de dados
        self.banco = GerenciamentoBanco()
        self.cpf = cpf

        if self.banco.get_logado():
            # Carrega os dados do cliente e da conta
            self.carregar_dados_cliente(cpf)
            self.carregar_dados_conta(cpf)

            # Variável para controlar se os dados estão escondidos
            self.dados_escondidos = True  # Inicia com os dados escondidos por segurança

            # Layout principal
            layout_principal = QVBoxLayout()

            # Layout superior (nome, CPF e saldo)
            layout_superior = QHBoxLayout()

            # Bloco do canto superior esquerdo (nome e CPF)
            bloco_esquerdo = QVBoxLayout()
            self.label_nome = QLabel(f"Nome: {self.dados_cliente['nome']}")
            self.label_cpf = QLabel(f"CPF: {FuncoesGerais.formatar_cpf(self.dados_cliente['cpf'], self.dados_escondidos)}")
            bloco_esquerdo.addWidget(self.label_nome)
            bloco_esquerdo.addWidget(self.label_cpf)

            # Bloco do canto superior direito (saldo)
            bloco_direito = QVBoxLayout()
            self.label_saldo_titulo = QLabel("Saldo")
            self.label_saldo = QLabel("R$ ***.**")  # Saldo escondido por padrão
            self.botao_atualizar_saldo = QPushButton("Atualizar Saldo")
            self.botao_atualizar_saldo.clicked.connect(self.atualizar_saldo)  # Conecta o botão de atualizar saldo
            bloco_direito.addWidget(self.label_saldo_titulo)
            bloco_direito.addWidget(self.label_saldo)
            bloco_direito.addWidget(self.botao_atualizar_saldo)

            # Adiciona os blocos ao layout superior
            layout_superior.addLayout(bloco_esquerdo)
            layout_superior.addLayout(bloco_direito)

            # Botão para esconder/exibir dados
            self.botao_esconder_dados = QPushButton("Exibir Dados")
            self.botao_esconder_dados.clicked.connect(self.alternar_dados)
            layout_principal.addWidget(self.botao_esconder_dados)

            # Layout central (botões de ações)
            layout_central = QHBoxLayout()
            self.botao_sacar = QPushButton("Sacar Dinheiro")
            self.botao_depositar = QPushButton("Depósito")
            self.botao_sacar.clicked.connect(self.realizar_saque)  # Conecta o botão de saque
            self.botao_depositar.clicked.connect(self.realizar_deposito)  # Conecta o botão de depósito
            self.botao_transferencia = QPushButton("Transferência Bancária")

            # Conecta os botões às funções
            self.botao_sacar.clicked.connect(self.realizar_saque)
            self.botao_depositar.clicked.connect(self.realizar_deposito)
            self.botao_transferencia.clicked.connect(self.realizar_transferencia)

            # Adiciona os botões ao layout central
            for botao in [self.botao_sacar, self.botao_depositar, self.botao_transferencia]:
                layout_central.addWidget(botao)

            # Layout inferior (número do cartão e CVV)
            layout_inferior = QVBoxLayout()
            self.label_cartao = QLabel("Número do Cartão: **** **** **** ****")  # Número do cartão escondido por padrão
            self.label_cvv = QLabel("CVV: ***")  # CVV escondido por padrão
            layout_inferior.addWidget(self.label_cartao)
            layout_inferior.addWidget(self.label_cvv)

            # Adiciona os layouts ao layout principal
            layout_principal.addLayout(layout_superior)
            layout_principal.addLayout(layout_central)
            layout_principal.addLayout(layout_inferior)

            self.setLayout(layout_principal)

            self.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    font-weight: bold;
                    font-family: Arial, sans-serif;
                    background-color: #0078D7;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #005A9E;
                    cursor: pointer;
                }
                QLabel {
                    font-size: 18px;
                    color: #333333;
                    padding: 5px;
                }
            """)

        else:
            # Se o cliente não estiver logado, exibe uma mensagem de erro
            QMessageBox.critical(self, "Erro", "Cliente não logado.")
            self.close()

    def carregar_dados_cliente(self, cpf):
        """Carrega os dados do cliente."""
        self.dados_cliente = self.banco.buscar_dados_como_dicionario(cpf) or {
            "nome": "Não encontrado",
            "cpf": "Não encontrado"
        }

    def carregar_dados_conta(self, cpf):
        """Carrega os dados da conta."""
        self.dados_conta = self.banco.buscar_dados_conta(cpf) or {
            "saldo": 0.0,
            "numero_cartao": "0000 0000 0000 0000",
            "codigo_de_segurança_do_cartao": "000"
        }

    def alternar_dados(self):
        """Alterna entre exibir e esconder os dados do CPF, saldo, número do cartão e CVV."""
        self.dados_escondidos = not self.dados_escondidos

        # Atualiza os dados exibidos
        self.label_cpf.setText(f"CPF: {FuncoesGerais.formatar_cpf(self.dados_cliente['cpf'], self.dados_escondidos)}")
        self.label_saldo.setText("R$ ***.**" if self.dados_escondidos else f"R$ {self.dados_conta['saldo']:.2f}")
        self.label_cartao.setText(
            f"Número do Cartão: {FuncoesGerais.esconder_cartao(self.dados_conta['numero_cartao'])}" if self.dados_escondidos
            else f"Número do Cartão: {FuncoesGerais.formatar_cartao(self.dados_conta['numero_cartao'])}"
        )
        self.label_cvv.setText("CVV: ***" if self.dados_escondidos else f"CVV: {self.dados_conta['codigo_de_segurança_do_cartao']}")
        self.botao_esconder_dados.setText("Exibir Dados" if self.dados_escondidos else "Esconder Dados")

    def realizar_saque(self):
        QMessageBox.information(self, "Saque", "Função de saque ainda não implementada.")

    def realizar_deposito(self):
        QMessageBox.information(self, "Depósito", "Função de depósito ainda não implementada.")

    def realizar_transferencia(self):
        """Abre a janela de transferência bancária."""
        self.janela_transferencia = JanelaTransferencia(self.cpf)  # Passa o CPF do remetente
        self.janela_transferencia.show()
        
    def realizar_deposito(self):
        """Abre a janela de depósito."""
        self.janela_deposito = JanelaDeposito(self.cpf)  # Passa o CPF do remetente
        self.janela_deposito.show()
        
    def atualizar_saldo(self):
        """Atualiza o saldo exibido na interface."""
        try:
            # Busca o saldo atualizado no banco de dados
            saldo_atualizado = self.banco.get_cursor().execute(
                "SELECT saldo FROM Contas WHERE cpf = ?", (self.cpf,)
            ).fetchone()

            if saldo_atualizado is None:
                QMessageBox.critical(self, "Erro", "Conta não encontrada.")
                return

            # Atualiza o saldo na variável de dados da conta
            self.dados_conta['saldo'] = saldo_atualizado[0]

            # Atualiza o rótulo do saldo com base no estado de exibição (escondido ou visível)
            if self.dados_escondidos:
                self.label_saldo.setText("R$ ***.**")
            else:
                self.label_saldo.setText(f"R$ {self.dados_conta['saldo']:.2f}")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar saldo: {e}")
            
    def realizar_saque(self):
        """Abre a janela de saque."""
        self.janela_saque = JanelaSaque(self.cpf, self.atualizar_saldo)  # Passa o CPF e o callback para atualizar o saldo
        self.janela_saque.show()
                
"""if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    tela_principal = TelaPrincipal("12561898474")  # Exemplo de CPF
    tela_principal.show()
    sys.exit(app.exec_())"""