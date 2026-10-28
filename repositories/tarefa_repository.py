# Importa a função que abre a conexão com o banco de dados.
from database.conexao import conectar_banco


# Cria a função responsável por salvar uma tarefa no MySQL.
def criar_tarefa(tarefa):

    # Abre uma conexão com o banco de dados.
    banco = conectar_banco()

    # Cria um cursor para executar comandos SQL.
    cursor = banco.cursor()

    # Comando SQL que adiciona uma nova tarefa na tabela tarefas.
    comando = """
        INSERT INTO tarefas
        (
            titulo,
            descricao,
            dthr_prazo,
            frequencia,
            fk_grupo
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    # Coloca os dados da tarefa na mesma ordem das colunas acima.
    valores = (
        tarefa.titulo,
        tarefa.descricao,
        tarefa.dthr_prazo,
        tarefa.frequencia,
        tarefa.fk_grupo
    )

    # Envia o comando e os dados para o MySQL.
    cursor.execute(comando, valores)

    # Confirma a alteração para salvar a tarefa.
    banco.commit()

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão com o banco.
    banco.close()

# Cria a função responsável por buscar as tarefas de um grupo.
# Também verifica se o grupo pertence ao usuário conectado.
def buscar_tarefas_por_grupo(fk_grupo, fk_usuario):

    # Abre uma conexão com o banco de dados.
    banco = conectar_banco()

    # Cria um cursor que retorna os dados como dicionário.
    cursor = banco.cursor(dictionary=True)

    # Busca tarefas somente se o grupo pertencer ao usuário.
    comando = """
        SELECT tarefas.*
        FROM tarefas
        INNER JOIN grupos
            ON tarefas.fk_grupo = grupos.id_grupo
        WHERE tarefas.fk_grupo = %s
        AND grupos.fk_usuario = %s
    """

    # Executa a consulta usando o ID do grupo e do usuário.
    cursor.execute(comando, (fk_grupo, fk_usuario))

    # Guarda todas as tarefas encontradas.
    tarefas = cursor.fetchall()

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão com o banco.
    banco.close()

    # Retorna as tarefas encontradas.
    return tarefas

# Cria a função responsável por editar uma tarefa.
# Verifica se a tarefa pertence a um grupo do usuário conectado.
def editar_tarefa(id_tarefa, titulo, descricao, fk_usuario):

    # Abre uma conexão com o banco de dados.
    banco = conectar_banco()

    # Cria um cursor para executar comandos SQL.
    cursor = banco.cursor()

    # Atualiza a tarefa somente se o grupo pertencer ao usuário.
    comando = """
        UPDATE tarefas
        INNER JOIN grupos
            ON tarefas.fk_grupo = grupos.id_grupo
        SET
            tarefas.titulo = %s,
            tarefas.descricao = %s
        WHERE tarefas.id_tarefa = %s
        AND grupos.fk_usuario = %s
    """

    # Organiza os valores que serão enviados ao MySQL.
    valores = (
        titulo,
        descricao,
        id_tarefa,
        fk_usuario
    )

    # Executa o comando de atualização.
    cursor.execute(comando, valores)

    # Confirma a alteração no banco.
    banco.commit()

    # Guarda a quantidade de tarefas alteradas.
    quantidade_alterada = cursor.rowcount

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão com o banco.
    banco.close()

    # Retorna a quantidade de tarefas alteradas.
    return quantidade_alterada

# Cria a função responsável por excluir uma tarefa.
def excluir_tarefa(id_tarefa, fk_usuario):

    # Abre uma conexão com o banco de dados.
    banco = conectar_banco()

    # Cria um cursor para executar comandos SQL.
    cursor = banco.cursor()

    # Exclui a tarefa somente se ela pertencer ao usuário.
    comando = """
        DELETE tarefas
        FROM tarefas
        INNER JOIN grupos
            ON tarefas.fk_grupo = grupos.id_grupo
        WHERE tarefas.id_tarefa = %s
        AND grupos.fk_usuario = %s
    """

    # Envia os valores para o comando SQL.
    valores = (
        id_tarefa,
        fk_usuario
    )

    # Executa a exclusão.
    cursor.execute(comando, valores)

    # Confirma a alteração no banco.
    banco.commit()

    # Guarda a quantidade de tarefas excluídas.
    quantidade_excluida = cursor.rowcount

    # Fecha o cursor e a conexão.
    cursor.close()
    banco.close()

    # Retorna a quantidade excluída.
    return quantidade_excluida

# Cria a função responsável por concluir uma tarefa.
def concluir_tarefa(id_tarefa, fk_usuario):

    # Abre uma conexão com o banco de dados.
    banco = conectar_banco()

    # Cria um cursor para executar comandos SQL.
    cursor = banco.cursor()

    # Atualiza o status somente se a tarefa pertencer ao usuário.
    comando = """
        UPDATE tarefas
        INNER JOIN grupos
            ON tarefas.fk_grupo = grupos.id_grupo
        SET tarefas.status = 'CONCLUIDA'
        WHERE tarefas.id_tarefa = %s
        AND grupos.fk_usuario = %s
    """

    # Envia os valores para o comando SQL.
    valores = (
        id_tarefa,
        fk_usuario
    )

    # Executa a atualização.
    cursor.execute(comando, valores)

    # Confirma a alteração no banco.
    banco.commit()

    # Guarda a quantidade de tarefas alteradas.
    quantidade_alterada = cursor.rowcount

    # Fecha o cursor e a conexão.
    cursor.close()
    banco.close()

    # Retorna a quantidade de tarefas alteradas.
    return quantidade_alterada