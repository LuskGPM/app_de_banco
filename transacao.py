from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from database.controle_banco import GerenciamentoBanco


class JanelaTransferencia(QWidget):
    def __init__(self, cpf_remetente):
        super().__init__()
        self.setWindowTitle("Transferência Bancária")
        self.setGeometry(400, 300, 400, 400)

        self.cpf_remetente = cpf_remetente
        self.banco = GerenciamentoBanco()

        # Layout principal
        layout_principal = QVBoxLayout()

        # Campo para número do cartão do remetente
        self.label_cartao_remetente = QLabel("Número do Cartão do Remetente:")
        self.input_cartao_remetente = QLineEdit()
        layout_principal.addWidget(self.label_cartao_remetente)
        layout_principal.addWidget(self.input_cartao_remetente)

        # Campo para CVV do remetente
        self.label_cvv_remetente = QLabel("CVV do Remetente:")
        self.input_cvv_remetente = QLineEdit()
        self.input_cvv_remetente.setEchoMode(QLineEdit.Password)
        layout_principal.addWidget(self.label_cvv_remetente)
        layout_principal.addWidget(self.input_cvv_remetente)

        # Campo para CPF do destinatário
        self.label_cpf_destinatario = QLabel("CPF do Destinatário:")
        self.input_cpf_destinatario = QLineEdit()
        layout_principal.addWidget(self.label_cpf_destinatario)
        layout_principal.addWidget(self.input_cpf_destinatario)

        # Campo para valor da transferência
        self.label_valor = QLabel("Valor da Transferência:")
        self.input_valor = QLineEdit()
        self.input_valor.setPlaceholderText("Ex: 100.00")
        layout_principal.addWidget(self.label_valor)
        layout_principal.addWidget(self.input_valor)

        # Campo para senha do remetente
        self.label_senha = QLabel("Senha do Remetente:")
        self.input_senha = QLineEdit()
        self.input_senha.setEchoMode(QLineEdit.Password)
        layout_principal.addWidget(self.label_senha)
        layout_principal.addWidget(self.input_senha)

        # Botão para realizar a transferência
        self.botao_transferir = QPushButton("Transferir")
        self.botao_transferir.clicked.connect(self.realizar_transferencia)
        layout_principal.addWidget(self.botao_transferir)

        self.setLayout(layout_principal)
        
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
                            cursor: pointer;
                        }
                        QLabel {
                            font-size: 22px;
                            font-weight: bold;
                            color: #333333;
                        }
                           """)

    def realizar_transferencia(self):
        # Obtém os dados inseridos pelo usuário
        numero_cartao_remetente = self.input_cartao_remetente.text()
        cvv_remetente = self.input_cvv_remetente.text()
        cpf_destinatario = self.input_cpf_destinatario.text()
        valor = self.input_valor.text()
        senha = self.input_senha.text()

        # Valida os campos
        if not numero_cartao_remetente or not cvv_remetente or not cpf_destinatario or not valor or not senha:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            valor = float(valor)
            if valor <= 0:
                QMessageBox.warning(self, "Erro", "O valor deve ser maior que zero.")
                return
        except ValueError:
            QMessageBox.warning(self, "Erro", "O valor deve ser numérico.")
            return

        # Verifica a senha do remetente
        senha_armazenada = self.banco.buscar_senha(self.cpf_remetente)
        if not senha_armazenada or not self.banco.verificar_senha(senha, senha_armazenada):
            QMessageBox.critical(self, "Erro", "Senha incorreta.")
            return

        # Verifica se o número do cartão e o CVV do remetente estão corretos
        dados_remetente = self.banco.get_cursor().execute(
            "SELECT cpf FROM Contas WHERE numero_cartao = ? AND codigo_de_segurança_do_cartao = ? AND cpf = ?",
            (numero_cartao_remetente, cvv_remetente, self.cpf_remetente)
        ).fetchone()

        if not dados_remetente:
            QMessageBox.critical(self, "Erro", "Número do cartão ou CVV do remetente incorretos.")
            return

        # Verifica se o CPF do destinatário existe
        dados_destinatario = self.banco.get_cursor().execute(
            "SELECT cpf FROM Contas WHERE cpf = ?", (cpf_destinatario,)
        ).fetchone()

        if not dados_destinatario:
            QMessageBox.critical(self, "Erro", "CPF do destinatário não encontrado.")
            return

        # Verifica se o remetente tem saldo suficiente
        if not self.verificar_saldo(valor):
            return

        # Realiza a transferência
        try:
            self.banco.get_cursor().execute(
                "UPDATE Contas SET saldo = saldo - ? WHERE cpf = ?", (valor, self.cpf_remetente)
            )
            self.banco.get_cursor().execute(
                "UPDATE Contas SET saldo = saldo + ? WHERE cpf = ?", (valor, cpf_destinatario)
            )
            self.banco.get_conexao().commit()
            QMessageBox.information(self, "Sucesso", "Transferência realizada com sucesso!")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao realizar transferência: {e}")

    def verificar_saldo(self, valor):
        """Verifica se o remetente tem saldo suficiente para realizar a transferência."""
        try:
            saldo_remetente = self.banco.get_cursor().execute(
                "SELECT saldo FROM Contas WHERE cpf = ?", (self.cpf_remetente,)
            ).fetchone()

            if saldo_remetente is None:
                QMessageBox.critical(self, "Erro", "Conta do remetente não encontrada.")
                return False

            if saldo_remetente[0] < valor:
                QMessageBox.warning(self, "Erro", "Saldo insuficiente para realizar a transferência.")
                return False

            return True
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao verificar saldo: {e}")
            return False