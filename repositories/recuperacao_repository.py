
# Importa a função responsável por conectar o sistema ao MySQL.
from database.conexao import conectar_banco


def criar_recuperacao(fk_usuario, codigo, expira_em):
    banco = conectar_banco()
    cursor = banco.cursor()

    try:
        comando = """
            INSERT INTO recuperacao_senha
            (fk_usuario, codigo, expira_em)
            VALUES (%s, %s, %s)
        """

        valores = (fk_usuario, codigo, expira_em)

        cursor.execute(comando, valores)
        banco.commit()

    except Exception:
        banco.rollback()
        raise

    finally:
        cursor.close()
        banco.close()


def buscar_recuperacao(fk_usuario, codigo):
    banco = conectar_banco()
    cursor = banco.cursor(dictionary=True)

    try:
        comando = """
            SELECT *
            FROM recuperacao_senha
            WHERE fk_usuario = %s
              AND codigo = %s
              AND usado = FALSE
            ORDER BY id_recuperacao DESC
            LIMIT 1
        """

        valores = (fk_usuario, codigo)
        cursor.execute(comando, valores)

        return cursor.fetchone()

    finally:
        cursor.close()
        banco.close()


def marcar_como_usada(id_recuperacao):
    banco = conectar_banco()
    cursor = banco.cursor()

    try:
        comando = """
            UPDATE recuperacao_senha
            SET usado = TRUE
            WHERE id_recuperacao = %s
        """

        cursor.execute(comando, (id_recuperacao,))
        banco.commit()

    except Exception:
        banco.rollback()
        raise

    finally:
        cursor.close()
        banco.close()
