# Banco Digital

Este é um projeto de um sistema bancário digital desenvolvido em Python utilizando a biblioteca PyQt5 para a interface gráfica e SQLite para o banco de dados. O sistema permite realizar operações como cadastro de clientes, acesso à conta, transferências, depósitos e saques.

## Funcionalidades

- **Cadastro de Clientes**: Permite cadastrar novos clientes com CPF, nome e senha.
- **Acesso à Conta**: Login seguro utilizando CPF e senha.
- **Depósito**: Realiza depósitos na conta do cliente.
- **Saque**: Permite saques da conta do cliente.
- **Transferência Bancária**: Realiza transferências entre contas cadastradas.
- **Exibição de Dados**: Mostra informações como saldo, CPF e número do cartão, com opção de esconder/exibir os dados.

## Requisitos

Antes de começar, certifique-se de ter os seguintes itens instalados em sua máquina:

- Python 3.8 ou superior
- Gerenciador de pacotes `pip`

## Instalação

Siga os passos abaixo para configurar o projeto em sua máquina:

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio

2. **Crie um ambiente virtual**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o projeto**:

   ```bash
   python menu_principal.py
   ```

## Estrutura do Projeto

```plaintext
.
├── acesso_conta.py          # Tela de acesso à conta
├── cadastro_cliente.py      # Tela de cadastro de clientes
├── depositar.py             # Tela de depósito
├── main.py                  # Tela principal do sistema
├── menu_principal.py        # Menu principal
├── saque.py                 # Tela de saque
├── transacao.py             # Tela de transferência bancária
├── database/
│   ├── controle_banco.py    # Gerenciamento do banco de dados
│   └── data/                # Arquivos do banco de dados SQLite
├── modulos/
│   ├── __init__.py
│   └── gerais.py            # Funções utilitárias
└── README.md                # Documentação do projeto
```

## Contribuição

Se você deseja contribuir com o projeto, fique à vontade para abrir um pull request ou relatar problemas. Sua contribuição é muito bem-vinda!

## Contato

Email: <lucasgpm00@gmail.com>
GitHub: LuskGPM
LinkedIn: <https://www.linkedin.com/in/lucasmelo00gpm/>
