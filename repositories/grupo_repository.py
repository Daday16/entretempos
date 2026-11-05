from database.conexao import conectar_banco
from psycopg2.extras import RealDictCursor


def criar_grupo(grupo):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor()

        comando = """
            INSERT INTO grupos (titulo, fk_usuario)
            VALUES (%s, %s)
        """

        valores = (
            grupo.titulo,
            grupo.fk_usuario
        )

        cursor.execute(comando, valores)
        banco.commit()

    except Exception:
        banco.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        banco.close()


def buscar_grupos_por_usuario(fk_usuario):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor(cursor_factory=RealDictCursor)

        comando = """
            SELECT *
            FROM grupos
            WHERE fk_usuario = %s
        """

        cursor.execute(comando, (fk_usuario,))
        grupos = cursor.fetchall()

        return grupos

    finally:
        if cursor:
            cursor.close()
        banco.close()


def verificar_grupo_usuario(fk_grupo, fk_usuario):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor(cursor_factory=RealDictCursor)

        comando = """
            SELECT *
            FROM grupos
            WHERE id_grupo = %s
              AND fk_usuario = %s
        """

        cursor.execute(comando, (fk_grupo, fk_usuario))
        grupo = cursor.fetchone()

        return grupo

    finally:
        if cursor:
            cursor.close()
        banco.close()