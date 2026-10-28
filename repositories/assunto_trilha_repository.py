# Importa a função responsável por abrir a conexão com o banco de dados.
from database.conexao import conectar_banco


# Cria a função responsável por salvar um assunto da trilha no banco.
def criar_assunto(fk_etapa, assunto, ordem):

    # Abre uma conexão com o banco de dados.
    banco = conectar_banco()

    # Cria um cursor para executar comandos SQL.
    cursor = banco.cursor()

    # Comando SQL que adiciona um assunto na tabela assuntos_trilha.
    comando = """
        INSERT INTO assuntos_trilha
        (
            fk_etapa,
            assunto,
            ordem
        )
        VALUES (%s, %s, %s)
    """

    # Organiza os valores que serão enviados para o banco.
    valores = (
        fk_etapa,
        assunto,
        ordem
    )

    # Executa o comando SQL com os valores do assunto.
    cursor.execute(comando, valores)

    # Confirma a alteração para salvar o assunto no banco.
    banco.commit()

    # Guarda o ID gerado para o novo assunto.
    id_assunto = cursor.lastrowid

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão com o banco.
    banco.close()

    # Retorna o ID do assunto criado.
    return id_assunto