# Importa o datetime para podermos registrar a data e a hora.
from datetime import datetime


# Cria a classe que representa um usuário do Entretempos.
class Usuario:

    # O __init__ é executado quando criamos um novo usuário.
    def __init__(self, nome_usuario, email, senha, data_nascimento=None):

        # Guarda o nome do usuário.
        self.nome_usuario = nome_usuario

        # Guarda o e-mail do usuário.
        self.email = email

        # Guarda a senha recebida.
        # Mais para frente, vamos proteger essa senha com hash
        # antes de ela ser salva no banco de dados.
        self.senha = senha

        # Registra automaticamente o momento em que o usuário foi criado.
        self.data_cadastro = datetime.now()

        # Guarda a data de nascimento.
        # Ela é opcional neste primeiro momento.
        self.data_nascimento = data_nascimento