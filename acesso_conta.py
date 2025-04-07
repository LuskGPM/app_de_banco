from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox, QApplication
import bcrypt
from database.controle_banco import GerenciamentoBanco  # Classe para gerenciar o banco de dados
from main import TelaPrincipal  # Importa a tela principal

class TelaAcessoConta(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Acesso à Conta")
        self.setGeometry(400, 300, 600, 400)

        if GerenciamentoBanco().get_logado():
            # Layout principal        
            layout_principal = QFormLayout()
            layout_principal.setSpacing(10)  # Espaçamento entre os pares de widgets
            layout_principal.setContentsMargins(20, 70, 20, 20)  # Margens do layout

            # Título
            self.titulo = QLabel("Acesso à Conta")
            self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #333333; font-family: Calibri; margin-bottom: 20px;")
            layout_principal.addRow(self.titulo)

            # Campo CPF
            self.input_cpf = QLineEdit()
            self.input_cpf.setPlaceholderText("Digite seu CPF")
            layout_principal.addRow("CPF:", self.input_cpf)

            # Campo Senha
            self.input_senha = QLineEdit()
            self.input_senha.setEchoMode(QLineEdit.Password)
            self.input_senha.setPlaceholderText("Digite sua senha")
            layout_principal.addRow("Senha:", self.input_senha)

            # Botão Entrar
            self.botao_enter = QPushButton("Entrar")
            self.botao_enter.clicked.connect(self.confirmar_senha)
            layout_principal.addRow("", self.botao_enter)  # Adiciona o botão sem label

            self.setLayout(layout_principal)

            # Estilo
            self.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #333333;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 20px;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-weight: bold;
                    font-size: 18px;
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
        else:
            QMessageBox.critical(self, "Erro", "Você não está logado!")
            self.close()
            
    def confirmar_senha(self):
        cpf = self.input_cpf.text().strip()
        senha = self.input_senha.text().strip()

        if not cpf or not senha:
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos!")
            return

        try:
            # Instancia a classe de gerenciamento do banco de dados
            banco = GerenciamentoBanco()

            # Busca a senha armazenada no banco para o CPF fornecido
            senha_armazenada = banco.buscar_senha(cpf)
            nome_cliente = banco.buscar_dados_como_dicionario(cpf)
            if senha_armazenada:
                # Verifica se a senha fornecida corresponde ao hash armazenado
                if bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada):
                    self.abrir_tela_principal(cpf)
                else:
                    QMessageBox.critical(self, "Erro", "Senha incorreta!")
            else:
                QMessageBox.critical(self, "Erro", "Nenhuma conta encontrada para o CPF informado.")
        except Exception as erro:
            QMessageBox.critical(self, "Erro", f"Erro ao acessar o banco de dados: {erro}")

    def abrir_tela_principal(self, cpf):
        """Abre a tela principal e fecha todas as janelas abertas."""
        banco = GerenciamentoBanco()
        banco.set_logado(True)

        # Fecha todas as janelas abertas
        QApplication.instance().closeAllWindows()

        # Abre a tela principal
        self.tela_principal = TelaPrincipal(cpf)  # Passa o CPF para a tela principal
        self.tela_principal.show()