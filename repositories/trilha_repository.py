from database.conexao import conectar_banco


def criar_trilha(fk_usuario, trilha):
    banco = conectar_banco()
    cursor = None

    try:
        cursor = banco.cursor()

        comando = """
            INSERT INTO trilhas (
                fk_usuario,
                titulo,
                descricao
            )
            VALUES (%s, %s, %s)
            RETURNING id_trilha
        """

        valores = (
            fk_usuario,
            trilha.titulo,
            trilha.descricao
        )

        cursor.execute(comando, valores)

        id_trilha = cursor.fetchone()[0]

        banco.commit()

        return id_trilha

    except Exception:
        banco.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        banco.close()