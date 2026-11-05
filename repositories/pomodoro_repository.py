from database.conexao import conectar_banco
from psycopg2.extras import RealDictCursor


def iniciar_pomodoro(pomodoro):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor()

        comando = """
            INSERT INTO pomodoros (
                duracao,
                dthr_inicio,
                dthr_termino,
                fk_usuario
            )
            VALUES (%s, %s, %s, %s)
        """

        valores = (
            pomodoro.duracao,
            pomodoro.dthr_inicio,
            pomodoro.dthr_termino,
            pomodoro.fk_usuario
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


def buscar_pomodoro_ativo(fk_usuario):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor(cursor_factory=RealDictCursor)

        comando = """
            SELECT *
            FROM pomodoros
            WHERE fk_usuario = %s
              AND dthr_termino IS NULL
            LIMIT 1
        """

        cursor.execute(comando, (fk_usuario,))
        pomodoro = cursor.fetchone()

        return pomodoro

    finally:
        if cursor:
            cursor.close()
        banco.close()


def finalizar_pomodoro(id_pomodoro, fk_usuario, dthr_termino):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor()

        comando = """
            UPDATE pomodoros
            SET dthr_termino = %s
            WHERE id_pomodoro = %s
              AND fk_usuario = %s
              AND dthr_termino IS NULL
        """

        valores = (
            dthr_termino,
            id_pomodoro,
            fk_usuario
        )

        cursor.execute(comando, valores)
        quantidade_alterada = cursor.rowcount

        banco.commit()

        return quantidade_alterada

    except Exception:
        banco.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        banco.close()


def adicionar_moedas(fk_usuario, quantidade):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor()

        comando = """
            UPDATE usuarios
            SET moedas = moedas + %s
            WHERE id_usuario = %s
        """

        valores = (
            quantidade,
            fk_usuario
        )

        cursor.execute(comando, valores)
        quantidade_alterada = cursor.rowcount

        banco.commit()

        return quantidade_alterada

    except Exception:
        banco.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        banco.close()


def consultar_moedas(fk_usuario):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor(cursor_factory=RealDictCursor)

        comando = """
            SELECT moedas
            FROM usuarios
            WHERE id_usuario = %s
        """

        cursor.execute(comando, (fk_usuario,))
        resultado = cursor.fetchone()

        return resultado

    finally:
        if cursor:
            cursor.close()
        banco.close()