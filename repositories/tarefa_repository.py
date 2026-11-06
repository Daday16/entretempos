from database.conexao import conectar_banco
from psycopg2.extras import RealDictCursor


def criar_tarefa(tarefa):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor()

        comando = """
            INSERT INTO tarefas (
                titulo,
                descricao,
                dthr_prazo,
                frequencia,
                fk_grupo
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            tarefa.titulo,
            tarefa.descricao,
            tarefa.dthr_prazo,
            tarefa.frequencia,
            tarefa.fk_grupo
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


def buscar_tarefas_por_grupo(fk_grupo, fk_usuario):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor(cursor_factory=RealDictCursor)

        comando = """
            SELECT tarefas.*
            FROM tarefas
            INNER JOIN grupos
                ON tarefas.fk_grupo = grupos.id_grupo
            WHERE tarefas.fk_grupo = %s
              AND grupos.fk_usuario = %s
        """

        cursor.execute(comando, (fk_grupo, fk_usuario))
        tarefas = cursor.fetchall()

        return tarefas

    finally:
        if cursor:
            cursor.close()
        banco.close()


def editar_tarefa(id_tarefa, titulo, descricao, fk_usuario):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor()

        comando = """
            UPDATE tarefas
            SET
                titulo = %s,
                descricao = %s
            FROM grupos
            WHERE tarefas.fk_grupo = grupos.id_grupo
              AND tarefas.id_tarefa = %s
              AND grupos.fk_usuario = %s
        """

        valores = (
            titulo,
            descricao,
            id_tarefa,
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


def excluir_tarefa(id_tarefa, fk_usuario):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor()

        comando = """
            DELETE FROM tarefas
            USING grupos
            WHERE tarefas.fk_grupo = grupos.id_grupo
              AND tarefas.id_tarefa = %s
              AND grupos.fk_usuario = %s
        """

        valores = (
            id_tarefa,
            fk_usuario
        )

        cursor.execute(comando, valores)
        quantidade_excluida = cursor.rowcount

        banco.commit()

        return quantidade_excluida

    except Exception:
        banco.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        banco.close()



def concluir_tarefa(id_tarefa, fk_usuario):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor()

        # Atualiza somente tarefas que ainda não foram concluídas.
        comando = """
            UPDATE tarefas
            SET status = 'CONCLUIDA'
            FROM grupos
            WHERE tarefas.fk_grupo = grupos.id_grupo
              AND tarefas.id_tarefa = %s
              AND grupos.fk_usuario = %s
              AND UPPER(COALESCE(tarefas.status, '')) NOT IN (
                  'CONCLUIDA',
                  'CONCLUÍDA'
              )
        """

        cursor.execute(comando, (id_tarefa, fk_usuario))
        quantidade_alterada = cursor.rowcount

        # Só credita as nozes se a tarefa foi concluída agora.
        if quantidade_alterada == 1:
            cursor.execute(
                """
                UPDATE usuarios
                SET moedas = COALESCE(moedas, 0) + 10
                WHERE id_usuario = %s
                """,
                (fk_usuario,)
            )

            if cursor.rowcount != 1:
                raise Exception("Não foi possível creditar as nozes.")

        banco.commit()

        return {
            "alterada": quantidade_alterada,
            "moedas_ganhas": 10 if quantidade_alterada == 1 else 0
        }

    except Exception:
        banco.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        banco.close()
