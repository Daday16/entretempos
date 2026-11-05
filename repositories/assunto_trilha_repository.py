from database.conexao import conectar_banco


def criar_assunto(fk_etapa, assunto, ordem):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor()

        comando = """
            INSERT INTO assuntos_trilha (
                fk_etapa,
                assunto,
                ordem
            )
            VALUES (%s, %s, %s)
            RETURNING id_assunto
        """

        valores = (
            fk_etapa,
            assunto,
            ordem
        )

        cursor.execute(comando, valores)

        id_assunto = cursor.fetchone()[0]

        banco.commit()

        return id_assunto

    except Exception:
        banco.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        banco.close()