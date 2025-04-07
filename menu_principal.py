from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QFormLayout, QLabel
from acesso_conta import TelaAcessoConta
from cadastro_cliente import TelaCadastroCliente
from database.controle_banco import GerenciamentoBanco
import sys

class MenuPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        banco = GerenciamentoBanco()
        banco.set_logado(False)
        self.setWindowTitle("Menu Principal")
        self.setGeometry(400, 400, 600, 400)

        # Widget central
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        # Layout principal
        layout_principal = QFormLayout()
        layout_principal.setSpacing(20)  # Espaçamento entre os widgets
        layout_principal.setContentsMargins(50, 50, 80, 50)  # Margens do layout

        # Título
        titulo = QLabel("Menu Principal")
        titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333333;
        """)
        layout_principal.addRow(titulo)

        # Botão Cadastrar
        self.botao_cadastro = QPushButton("Cadastrar")
        self.botao_cadastro.setStyleSheet("""
            QPushButton {
                font-size: 22px;
                background-color: #0078D7;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """)
        self.botao_cadastro.clicked.connect(self.mostrar_telacadastro)
        layout_principal.addRow(self.botao_cadastro)

        # Botão Acessar Conta
        self.botao_acessar_conta = QPushButton("Acessar Conta")
        self.botao_acessar_conta.setStyleSheet("""
            QPushButton {
                font-size: 22px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.botao_acessar_conta.clicked.connect(self.mostrar_tela_acesso)
        layout_principal.addRow(self.botao_acessar_conta)

        # Define o layout no widget central
        widget_central.setLayout(layout_principal)

    def mostrar_telacadastro(self):
        self.tela_cadastro = TelaCadastroCliente()
        self.tela_cadastro.show()

    def mostrar_tela_acesso(self):
        self.tela_acesso = TelaAcessoConta()
        self.tela_acesso.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = MenuPrincipal()
    menu.show()
    sys.exit(app.exec_())