# Importa a função responsável por abrir a conexão com o banco de dados.
from database.conexao import conectar_banco


# Cria a função responsável por salvar uma etapa da trilha no banco.
def criar_etapa(fk_trilha, etapa, ordem):

    # Abre uma conexão com o banco de dados.
    banco = conectar_banco()

    # Cria um cursor para executar comandos SQL.
    cursor = banco.cursor()

    # Comando SQL que adiciona uma etapa na tabela etapas_trilha.
    comando = """
        INSERT INTO etapas_trilha
        (
            fk_trilha,
            titulo,
            descricao,
            ordem
        )
        VALUES (%s, %s, %s, %s)
    """

    # Organiza os valores que serão enviados para o banco.
    valores = (
        fk_trilha,
        etapa.titulo,
        etapa.descricao,
        ordem
    )

    # Executa o comando SQL com os valores da etapa.
    cursor.execute(comando, valores)

    # Confirma a alteração para salvar a etapa no banco.
    banco.commit()

    # Guarda o ID gerado para a nova etapa.
    id_etapa = cursor.lastrowid

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão com o banco.
    banco.close()

    # Retorna o ID da etapa criada.
    return id_etapa