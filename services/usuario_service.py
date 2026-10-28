
# Importa bcrypt para gerar e verificar hashes de senhas.
import bcrypt

# Importa ferramentas para trabalhar com datas.
from datetime import date, datetime

# Importa as funções responsáveis pelo acesso ao banco de dados.
from repositories.usuario_repository import (
    listar_usuarios,
    criar_usuario,
    buscar_por_email,
)


# Classe que contém as regras de negócio dos usuários.
class UsuarioService:

    # Retorna todos os usuários cadastrados.
    def listar_usuarios(self):
        return listar_usuarios()

    # Busca um usuário pelo e-mail.
    def buscar_por_email(self, email):
        return buscar_por_email(email.strip())

    # Converte diferentes formatos de data para um objeto date.
    # Retorna None caso a data seja inválida.
    def converter_data(self, data_nascimento):

        # Se já for datetime, extrai apenas a data.
        if isinstance(data_nascimento, datetime):
            return data_nascimento.date()

        # Se já for date, retorna o valor diretamente.
        if isinstance(data_nascimento, date):
            return data_nascimento

        # Recusa valores que não sejam textos ou datas.
        if not isinstance(data_nascimento, str):
            return None

        # Remove espaços desnecessários.
        data_nascimento = data_nascimento.strip()

        # Formatos de data aceitos pelo sistema.
        formatos = (
            "%d/%m/%Y",  # 16/07/2004
            "%d%m%Y",    # 16072004
            "%Y-%m-%d",  # 2004-07-16
            "%Y%m%d",    # 20040716
        )

        # Tenta converter a data usando cada formato.
        for formato in formatos:
            try:
                return datetime.strptime(
                    data_nascimento,
                    formato,
                ).date()

            except ValueError:
                # Se falhar, tenta o próximo formato.
                continue

        # Nenhum formato correspondeu à data informada.
        return None

    # Verifica se a data de nascimento é válida.
    def data_nascimento_valida(self, data_nascimento):

        # Converte o valor recebido para uma data.
        data_convertida = self.converter_data(data_nascimento)

        # Recusa datas inválidas.
        if data_convertida is None:
            return False

        # Recusa datas futuras.
        if data_convertida > date.today():
            return False

        return True

    # Realiza o cadastro de um novo usuário.
    def criar_usuario(self, usuario):

        # Verifica se o nome foi informado.
        if (
            not usuario.nome_usuario
            or not usuario.nome_usuario.strip()
        ):
            raise ValueError("O nome de usuário é obrigatório.")

        # Verifica se o e-mail foi informado.
        if not usuario.email or not usuario.email.strip():
            raise ValueError("O e-mail é obrigatório.")

        # Verifica se a senha foi informada.
        if not usuario.senha:
            raise ValueError("A senha é obrigatória.")

        # Converte e valida a data de nascimento.
        data_convertida = self.converter_data(
            usuario.data_nascimento
        )

        if data_convertida is None:
            raise ValueError(
                "Data de nascimento inválida. "
                "Informe uma data válida."
            )

        # Impede o cadastro de uma data futura.
        if data_convertida > date.today():
            raise ValueError(
                "A data de nascimento não pode estar no futuro."
            )

        # Normaliza o e-mail para evitar diferenças por espaços.
        email = usuario.email.strip()

        # Verifica se o e-mail já está cadastrado.
        usuario_existente = buscar_por_email(email)

        if usuario_existente:
            raise ValueError("Este e-mail já está cadastrado.")

        # Converte a senha para bytes, como o bcrypt exige.
        senha_bytes = usuario.senha.encode("utf-8")

        
        # Gera o hash seguro da senha.
        senha_hash = bcrypt.hashpw(
            senha_bytes,
            bcrypt.gensalt(),
        )

        # Atualiza os dados do usuário antes de salvar.
        usuario.nome_usuario = usuario.nome_usuario.strip()
        usuario.email = email
        usuario.data_nascimento = data_convertida
        usuario.senha = senha_hash.decode("utf-8")

        # Salva o usuário no banco de dados.
        return criar_usuario(usuario)

    # Realiza o login de um usuário.
    def login(self, email, senha):
        # Busca o usuário pelo e-mail.
        usuario = self.buscar_por_email(email)

        if not usuario:
            raise ValueError("E-mail ou senha incorretos.")

        if isinstance(usuario, dict):
            senha_hash = usuario.get("senha")
        else:
            senha_hash = getattr(usuario, "senha", None)

        if not senha_hash:
            raise ValueError("E-mail ou senha incorretos.")

        try:
            hash_bytes = (
                senha_hash.encode("utf-8")
                if isinstance(senha_hash, str)
                else senha_hash
            )

            senha_correta = bcrypt.checkpw(
                senha.encode("utf-8"),
                hash_bytes,
            )
        except (ValueError, TypeError):
            raise ValueError("E-mail ou senha incorretos.")

        if not senha_correta:
            raise ValueError("E-mail ou senha incorretos.")

        return usuario
