# Importa a função que abre a conexão com o banco de dados.
from database.conexao import conectar_banco


# Cria a função responsável por salvar um grupo no MySQL.
def criar_grupo(grupo):

    # Abre uma conexão com o banco de dados.
    banco = conectar_banco()

    # Cria um cursor para executar comandos SQL.
    cursor = banco.cursor()

    # Comando SQL que adiciona um novo grupo na tabela grupos.
    comando = """
        INSERT INTO grupos
        (
            titulo,
            fk_usuario
        )
        VALUES (%s, %s)
    """

    # Coloca os dados do grupo na mesma ordem das colunas acima.
    valores = (
        grupo.titulo,
        grupo.fk_usuario
    )

    # Envia o comando e os dados para o MySQL.
    cursor.execute(comando, valores)

    # Confirma a alteração para salvar o grupo.
    banco.commit()

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão com o banco.
    banco.close()

# Cria a função responsável por buscar os grupos de um usuário.
def buscar_grupos_por_usuario(fk_usuario):

    # Abre uma conexão com o banco de dados.
    banco = conectar_banco()

    # Cria um cursor que retorna os dados como dicionário.
    cursor = banco.cursor(dictionary=True)

    # Comando SQL que busca somente os grupos do usuário informado.
    comando = """
        SELECT *
        FROM grupos
        WHERE fk_usuario = %s
    """

    # Executa a consulta usando o ID do usuário.
    cursor.execute(comando, (fk_usuario,))

    # Guarda todos os grupos encontrados.
    grupos = cursor.fetchall()

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão com o banco.
    banco.close()

    # Retorna os grupos encontrados.
    return grupos

# Cria uma função para verificar se um grupo pertence a um usuário.
def verificar_grupo_usuario(fk_grupo, fk_usuario):

    # Abre uma conexão com o banco de dados.
    banco = conectar_banco()

    # Cria um cursor para executar comandos SQL.
    cursor = banco.cursor(dictionary=True)

    # Comando SQL que procura o grupo pertencente ao usuário.
    comando = """
        SELECT *
        FROM grupos
        WHERE id_grupo = %s
        AND fk_usuario = %s
    """

    # Executa a consulta usando o ID do grupo e do usuário.
    cursor.execute(comando, (fk_grupo, fk_usuario))

    # Busca o grupo encontrado.
    grupo = cursor.fetchone()

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão com o banco.
    banco.close()

    # Retorna o grupo encontrado ou None.
    return grupo