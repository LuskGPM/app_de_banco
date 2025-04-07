from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from database.controle_banco import GerenciamentoBanco


class JanelaDeposito(QWidget):
    def __init__(self, cpf_remetente):
        super().__init__()
        self.setWindowTitle("Depósito")
        self.setGeometry(400, 300, 400, 200)

        self.cpf_remetente = cpf_remetente
        self.banco = GerenciamentoBanco()

        # Layout principal
        layout_principal = QVBoxLayout()

        # Campo para valor do depósito
        self.label_valor = QLabel("Valor do Depósito:")
        self.input_valor = QLineEdit()
        self.input_valor.setPlaceholderText("Ex: 100.00")
        layout_principal.addWidget(self.label_valor)
        layout_principal.addWidget(self.input_valor)

        # Botão para realizar o depósito
        self.botao_depositar = QPushButton("Depositar")
        self.botao_depositar.clicked.connect(self.realizar_deposito)
        layout_principal.addWidget(self.botao_depositar)

        self.setLayout(layout_principal)

    def realizar_deposito(self):
        # Obtém o valor inserido pelo usuário
        valor = self.input_valor.text()

        # Valida o valor
        try:
            valor = float(valor)
            if valor <= 0:
                QMessageBox.warning(self, "Erro", "O valor do depósito deve ser maior que zero.")
                return
        except ValueError:
            QMessageBox.warning(self, "Erro", "O valor deve ser numérico.")
            return

        # Realiza o depósito
        try:
            self.banco.get_cursor().execute(
                "UPDATE Contas SET saldo = saldo + ? WHERE cpf = ?", (valor, self.cpf_remetente)
            )
            self.banco.get_conexao().commit()
            QMessageBox.information(self, "Sucesso", "Depósito realizado com sucesso!")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao realizar depósito: {e}")