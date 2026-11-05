from database.conexao import conectar_banco


def criar_etapa(fk_trilha, etapa, ordem):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor()

        comando = """
            INSERT INTO etapas_trilha (
                fk_trilha,
                titulo,
                descricao,
                ordem
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id_etapa
        """

        valores = (
            fk_trilha,
            etapa.titulo,
            etapa.descricao,
            ordem
        )

        cursor.execute(comando, valores)

        id_etapa = cursor.fetchone()[0]

        banco.commit()

        return id_etapa

    except Exception:
        banco.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        banco.close()