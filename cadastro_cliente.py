from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QFormLayout, QMessageBox
from database.controle_banco import GerenciamentoBanco

class TelaCadastroCliente(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Cliente")
        self.setGeometry(400, 300, 600, 400)

        # Layout principal
        layout_principal = QFormLayout()
        layout_principal.setSpacing(10)  # Espaçamento entre os widgets
        layout_principal.setContentsMargins(20, 20, 70, 20)  # Margens do layout

        # Campo CPF
        self.input_cpf = QLineEdit()
        self.input_cpf.setPlaceholderText("Digite seu CPF")
        layout_principal.addRow("CPF:", self.input_cpf)

        # Campo Nome
        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Digite seu Nome")
        layout_principal.addRow("Nome:", self.input_nome)

        # Campo Senha
        self.input_senha = QLineEdit()
        self.input_senha.setEchoMode(QLineEdit.Password)
        self.input_senha.setPlaceholderText("Digite sua Senha")
        layout_principal.addRow("Senha:", self.input_senha)

        # Campo Confirmar Senha
        self.input_confirmar_senha = QLineEdit()
        self.input_confirmar_senha.setEchoMode(QLineEdit.Password)
        self.input_confirmar_senha.setPlaceholderText("Confirme sua Senha")
        layout_principal.addRow("Confirmar Senha:", self.input_confirmar_senha)

        # Botão Salvar
        self.botao_salvar = QPushButton("Salvar")
        self.botao_salvar.clicked.connect(self.salvar_cliente)
        layout_principal.addRow("", self.botao_salvar)  # Adiciona o botão sem label

        self.setLayout(layout_principal)

        # Estilo
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #333333;
                border-radius: 5px;
                padding: 5px;
                font-size: 20px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #333333;
            }
        """)

    def salvar_cliente(self):
        cpf = self.input_cpf.text().replace(".", "").replace("-", "")  # Remove a formatação
        nome = self.input_nome.text()
        senha = self.input_senha.text()
        confirmar_senha = self.input_confirmar_senha.text()

        if not cpf or not nome or not senha or not confirmar_senha:
            QMessageBox.critical(self, "Erro", "Todos os campos são obrigatórios!")
            return

        if senha != confirmar_senha:
            QMessageBox.critical(self, "Erro", "As senhas não coincidem!")
            return

        try:
            banco = GerenciamentoBanco()
            banco.cadastrar_cliente(cpf, nome, senha)
            QMessageBox.information(self, "Sucesso", "Cliente cadastrado com sucesso!")
            self.close()  # Fecha a janela de cadastro
        except Exception as erro:
            QMessageBox.critical(self, "Erro", f"Erro ao cadastrar cliente: {erro}")