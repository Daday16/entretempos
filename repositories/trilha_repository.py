# Importa a função responsável por abrir a conexão com o banco de dados.
from database.conexao import conectar_banco


# Cria a função responsável por salvar uma nova trilha no MySQL.
def criar_trilha(fk_usuario, trilha):

    # Abre uma conexão com o banco de dados.
    banco = conectar_banco()

    # Cria um cursor para executar comandos SQL.
    cursor = banco.cursor()

    # Comando SQL que adiciona a trilha na tabela trilhas.
    comando = """
        INSERT INTO trilhas
        (
            fk_usuario,
            titulo,
            descricao
        )
        VALUES (%s, %s, %s)
    """

    # Organiza os valores que serão enviados para o banco.
    valores = (
        fk_usuario,
        trilha.titulo,
        trilha.descricao
    )

    # Executa o comando SQL com os valores da trilha.
    cursor.execute(comando, valores)

    # Confirma a alteração para salvar a trilha no banco.
    banco.commit()

    # Guarda o ID gerado para a nova trilha.
    id_trilha = cursor.lastrowid

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão com o banco.
    banco.close()

    # Retorna o ID da trilha criada.
    return id_trilha