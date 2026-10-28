# Biblioteca para gerar códigos aleatórios de forma segura.
import secrets

# Importa ferramentas para trabalhar com datas e tempo.
from datetime import datetime, timedelta

# Importa as funções que conversam com o banco de dados.
from repositories.recuperacao_repository import (
    criar_recuperacao,
    buscar_recuperacao,
    marcar_como_usada
)

# Importa a função que atualiza a senha do usuário.
from repositories.usuario_repository import atualizar_senha

# Importa o serviço responsável pelos usuários.
from services.usuario_service import UsuarioService

# Importa o bcrypt para proteger a nova senha.
import bcrypt


class RecuperacaoService:

    def __init__(self):

        # Cria uma instância do serviço de usuários.
        self.usuario_service = UsuarioService()

    def buscar_usuario_por_email(self, email):

        # Procura um usuário usando o endereço de e-mail.
        usuario = self.usuario_service.buscar_por_email(email)

        # Retorna o usuário encontrado ou None.
        return usuario

    def gerar_codigo(self):

        # Gera um número aleatório entre 0 e 999999.
        numero = secrets.randbelow(1000000)

        # Transforma o número em um código de 6 dígitos.
        codigo = f"{numero:06d}"

        # Retorna o código gerado.
        return codigo

    def criar(self, fk_usuario):

        # Gera um novo código de recuperação.
        codigo = self.gerar_codigo()

        # Define que o código vai expirar daqui a 10 minutos.
        expira_em = datetime.now() + timedelta(minutes=10)

        # Salva o código no banco de dados.
        criar_recuperacao(
            fk_usuario,
            codigo,
            expira_em
        )

        # Retorna as informações da recuperação.
        return {
            "codigo": codigo,
            "expira_em": expira_em
        }

    def validar_codigo(self, fk_usuario, codigo):

        # Procura no banco um código válido e ainda não utilizado.
        recuperacao = buscar_recuperacao(
            fk_usuario,
            codigo
        )

        # Se não encontrou, o código é inválido.
        if recuperacao is None:
            return "codigo_invalido"

        # Pega a data de expiração do código.
        expira_em = recuperacao["expira_em"]

        # Verifica se o código já passou do prazo.
        if datetime.now() > expira_em:
            return "codigo_expirado"

        # Se chegou aqui, o código é válido.
        return recuperacao

    def redefinir_senha(self, id_usuario, id_recuperacao, nova_senha):

        # Transforma a nova senha em bytes.
        senha_bytes = nova_senha.encode("utf-8")

        # Cria uma versão protegida da senha usando bcrypt.
        senha_hash = bcrypt.hashpw(
            senha_bytes,
            bcrypt.gensalt()
        )

        # Converte o hash para texto antes de salvar no banco.
        senha_hash = senha_hash.decode("utf-8")

        # Atualiza a senha do usuário.
        quantidade_alterada = atualizar_senha(
            id_usuario,
            senha_hash
        )

        # Se nenhum usuário foi alterado, algo deu errado.
        if quantidade_alterada == 0:
            return False

        # Marca o código de recuperação como utilizado.
        marcar_como_usada(id_recuperacao)

        # Informa que a senha foi alterada.
        return True

    def finalizar_recuperacao(self, id_recuperacao):

        # Marca o código como usado no banco.
        marcar_como_usada(id_recuperacao)

        # Informa que a operação terminou.
        return True