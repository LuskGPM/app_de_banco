from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from database.controle_banco import GerenciamentoBanco


class JanelaSaque(QWidget):
    def __init__(self, cpf_remetente, atualizar_saldo_callback):
        super().__init__()
        self.setWindowTitle("Saque")
        self.setGeometry(400, 300, 400, 200)

        self.cpf_remetente = cpf_remetente
        self.banco = GerenciamentoBanco()
        self.atualizar_saldo_callback = atualizar_saldo_callback

        # Layout principal
        layout_principal = QVBoxLayout()

        # Campo para valor do saque
        self.label_valor = QLabel("Valor do Saque:")
        self.input_valor = QLineEdit()
        layout_principal.addWidget(self.label_valor)
        layout_principal.addWidget(self.input_valor)

        # Botão para realizar o saque
        self.botao_sacar = QPushButton("Sacar")
        self.botao_sacar.clicked.connect(self.realizar_saque)
        layout_principal.addWidget(self.botao_sacar)

        self.setLayout(layout_principal)
        
        self.setStyleSheet("""
                QLineEdit {
                border: 1px solid #333333;
                border-radius: 5px;
                padding: 5px;
                font-size: 20px;
            }
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

    def realizar_saque(self):
        # Obtém o valor inserido pelo usuário
        valor = self.input_valor.text()

        # Valida o valor
        try:
            valor = float(valor)
            if valor <= 0:
                QMessageBox.warning(self, "Erro", "O valor do saque deve ser maior que zero.")
                return
        except ValueError:
            QMessageBox.warning(self, "Erro", "O valor deve ser numérico.")
            return

        # Verifica se o saldo é suficiente
        saldo_atual = self.banco.get_cursor().execute(
            "SELECT saldo FROM Contas WHERE cpf = ?", (self.cpf_remetente,)
        ).fetchone()

        if saldo_atual is None:
            QMessageBox.critical(self, "Erro", "Conta não encontrada.")
            return

        if saldo_atual[0] < valor:
            QMessageBox.warning(self, "Erro", "Saldo insuficiente para realizar o saque.")
            return

        # Realiza o saque
        try:
            self.banco.get_cursor().execute(
                "UPDATE Contas SET saldo = saldo - ? WHERE cpf = ?", (valor, self.cpf_remetente)
            )
            self.banco.get_conexao().commit()
            QMessageBox.information(self, "Sucesso", "Saque realizado com sucesso!")
            self.atualizar_saldo_callback()  # Atualiza o saldo na interface principal
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao realizar saque: {e}")
            