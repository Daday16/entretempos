
# Importa a função que cria a conexão com o PostgreSQL.
from database.conexao import conectar_banco

from psycopg2.extras import RealDictCursor


# Lista todos os usuários cadastrados.
def listar_usuarios():

    banco = conectar_banco()

    try:
        cursor = banco.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM usuarios")

        usuarios = cursor.fetchall()

        return usuarios

    finally:
        cursor.close()
        banco.close()


# Salva um novo usuário no banco.
def criar_usuario(usuario):

    banco = conectar_banco()

    try:
        cursor = banco.cursor()

        comando = """
            INSERT INTO usuarios
            (nome_usuario, email, senha, data_cadastro, data_nascimento)
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            usuario.nome_usuario,
            usuario.email,
            usuario.senha,
            usuario.data_cadastro,
            usuario.data_nascimento
        )

        cursor.execute(comando, valores)

        banco.commit()

    except Exception:
        banco.rollback()
        raise

    finally:
        cursor.close()
        banco.close()


# Busca um usuário pelo e-mail.
def buscar_por_email(email):

    banco = conectar_banco()

    try:
        cursor = banco.cursor(cursor_factory=RealDictCursor)

        comando = """
            SELECT *
            FROM usuarios
            WHERE email = %s
        """

        cursor.execute(comando, (email,))

        usuario = cursor.fetchone()

        return usuario

    finally:
        cursor.close()
        banco.close()


# Atualiza a senha de um usuário.
def atualizar_senha(id_usuario, nova_senha):

    banco = conectar_banco()

    try:
        cursor = banco.cursor()

        comando = """
            UPDATE usuarios
            SET senha = %s
            WHERE id_usuario = %s
        """

        valores = (
            nova_senha,
            id_usuario
        )

        cursor.execute(comando, valores)

        banco.commit()

        quantidade_alterada = cursor.rowcount

        return quantidade_alterada

    except Exception:
        banco.rollback()
        raise

    finally:
        cursor.close()
        banco.close()
