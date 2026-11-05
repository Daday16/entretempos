# Importa a função que abre a conexão com o banco de dados.
from database.conexao import conectar_banco
from psycopg2.extras import RealDictCursor


def criar_perfil(perfil, fk_usuario):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor()

        comando = """
            INSERT INTO perfis (
                fk_usuario,
                objetivo,
                nivel_programacao,
                tempo_diario,
                dias_disponiveis,
                dificuldade_foco
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        valores = (
            fk_usuario,
            perfil.objetivo,
            perfil.nivel_conhecimento,
            perfil.tempo_diario,
            perfil.dias_disponiveis,
            perfil.dificuldade_foco
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


def buscar_perfil_por_usuario(fk_usuario):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor(cursor_factory=RealDictCursor)

        comando = """
            SELECT *
            FROM perfis
            WHERE fk_usuario = %s
            ORDER BY id_perfil DESC
            LIMIT 1
        """

        cursor.execute(comando, (fk_usuario,))
        perfil = cursor.fetchone()

        return perfil

    finally:
        if cursor:
            cursor.close()
        banco.close()


def editar_perfil(
    fk_usuario,
    objetivo,
    nivel_conhecimento,
    tempo_diario,
    dias_disponiveis,
    dificuldade_foco
):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor()

        comando = """
            UPDATE perfis
            SET
                objetivo = %s,
                nivel_programacao = %s,
                tempo_diario = %s,
                dias_disponiveis = %s,
                dificuldade_foco = %s
            WHERE fk_usuario = %s
        """

        valores = (
            objetivo,
            nivel_conhecimento,
            tempo_diario,
            dias_disponiveis,
            dificuldade_foco,
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