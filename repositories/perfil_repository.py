# Importa a função que abre a conexão com o banco de dados.
from database.conexao import conectar_banco


# Cria a função responsável por salvar um perfil no MySQL.
def criar_perfil(perfil, fk_usuario):

    # Abre uma conexão com o banco de dados.
    banco = conectar_banco()

    # Cria um cursor para executar comandos SQL.
    cursor = banco.cursor()

    # Comando SQL que adiciona um novo perfil na tabela perfis.
    # Mantemos nivel_programacao porque esse é o nome atual da coluna no MySQL.
    comando = """
        INSERT INTO perfis
        (
            fk_usuario,
            objetivo,
            nivel_programacao,
            tempo_diario,
            dias_disponiveis,
            dificuldade_foco
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    # Coloca os dados do objeto Perfil na mesma ordem dos campos acima.
    valores = (
        fk_usuario,
        perfil.objetivo,
        perfil.nivel_conhecimento,
        perfil.tempo_diario,
        perfil.dias_disponiveis,
        perfil.dificuldade_foco
    )

    # Envia o comando e os dados para o MySQL.
    cursor.execute(comando, valores)

    # Confirma a alteração para salvar o perfil.
    banco.commit()

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão com o banco.
    banco.close()


# Cria a função responsável por buscar o perfil de um usuário.
def buscar_perfil_por_usuario(fk_usuario):

    # Abre uma conexão com o banco de dados.
    banco = conectar_banco()

    # Cria um cursor que retorna os resultados como dicionários.
    cursor = banco.cursor(dictionary=True)

    # Busca apenas o perfil mais recente do usuário.
    comando = """
        SELECT *
        FROM perfis
        WHERE fk_usuario = %s
        ORDER BY id_perfil DESC
        LIMIT 1
    """

    # Envia o comando e o ID do usuário para o MySQL.
    cursor.execute(comando, (fk_usuario,))

    # Guarda o perfil encontrado.
    perfil = cursor.fetchone()

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão com o banco.
    banco.close()

    # Retorna o perfil encontrado.
    return perfil


# Cria a função responsável por editar o perfil do usuário.
def editar_perfil(
    fk_usuario,
    objetivo,
    nivel_conhecimento,
    tempo_diario,
    dias_disponiveis,
    dificuldade_foco
):

    # Abre uma conexão com o banco de dados.
    banco = conectar_banco()

    # Cria um cursor para executar comandos SQL.
    cursor = banco.cursor()

    # Atualiza o perfil pertencente ao usuário.
    # Mantemos nivel_programacao porque esse é o nome atual da coluna no MySQL.
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

    # Organiza os valores na mesma ordem do comando SQL.
    valores = (
        objetivo,
        nivel_conhecimento,
        tempo_diario,
        dias_disponiveis,
        dificuldade_foco,
        fk_usuario
    )

    # Executa a atualização.
    cursor.execute(comando, valores)

    # Confirma a alteração no banco.
    banco.commit()

    # Guarda a quantidade de registros alterados.
    quantidade_alterada = cursor.rowcount

    # Fecha o cursor e a conexão.
    cursor.close()
    banco.close()

    # Retorna a quantidade de registros alterados.
    return quantidade_alterada