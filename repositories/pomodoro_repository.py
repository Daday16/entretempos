# Importa a função que conecta ao banco de dados.
from database.conexao import conectar_banco


# Cria uma nova sessão de Pomodoro no banco.
def iniciar_pomodoro(pomodoro):

    # Abre a conexão com o banco.
    banco = conectar_banco()

    # Cria um cursor para executar comandos SQL.
    cursor = banco.cursor()

    # Comando SQL para salvar o Pomodoro.
    comando = """
        INSERT INTO pomodoros
        (
            duracao,
            dthr_inicio,
            dthr_termino,
            fk_usuario
        )
        VALUES (%s, %s, %s, %s)
    """

    # Separa os valores que serão enviados ao banco.
    valores = (
        pomodoro.duracao,
        pomodoro.dthr_inicio,
        pomodoro.dthr_termino,
        pomodoro.fk_usuario
    )

    # Executa o comando usando os valores.
    cursor.execute(comando, valores)

    # Confirma a alteração no banco.
    banco.commit()

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão com o banco.
    banco.close()

# Verifica se o usuário possui um Pomodoro em andamento.
def buscar_pomodoro_ativo(fk_usuario):

    # Abre a conexão com o banco.
    banco = conectar_banco()

    # Cria um cursor que retorna os dados como dicionário.
    cursor = banco.cursor(dictionary=True)

    # Procura um Pomodoro que ainda não terminou.
    comando = """
        SELECT *
        FROM pomodoros
        WHERE fk_usuario = %s
        AND dthr_termino IS NULL
        LIMIT 1
    """

    # Executa a consulta usando o ID do usuário.
    cursor.execute(comando, (fk_usuario,))

    # Pega o Pomodoro encontrado, ou None se não existir.
    pomodoro = cursor.fetchone()

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão com o banco.
    banco.close()

    # Retorna o resultado da busca.
    return pomodoro

# Finaliza um Pomodoro que está em andamento.
def finalizar_pomodoro(id_pomodoro, fk_usuario, dthr_termino):

    # Abre a conexão com o banco.
    banco = conectar_banco()

    # Cria um cursor para executar comandos SQL.
    cursor = banco.cursor()

    # Atualiza o horário de término do Pomodoro.
    comando = """
        UPDATE pomodoros
        SET dthr_termino = %s
        WHERE id_pomodoro = %s
        AND fk_usuario = %s
        AND dthr_termino IS NULL
    """

    # Organiza os valores que serão enviados ao banco.
    valores = (
        dthr_termino,
        id_pomodoro,
        fk_usuario
    )

    # Executa a atualização.
    cursor.execute(comando, valores)

    # Confirma a alteração no banco.
    banco.commit()

    # Guarda quantos registros foram alterados.
    quantidade_alterada = cursor.rowcount

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão.
    banco.close()

    # Retorna a quantidade de registros alterados.
    return quantidade_alterada

# Adiciona moedas ao saldo do usuário.
def adicionar_moedas(fk_usuario, quantidade):

    # Abre a conexão com o banco.
    banco = conectar_banco()

    # Cria um cursor para executar comandos SQL.
    cursor = banco.cursor()

    # Comando SQL para aumentar o saldo de moedas.
    comando = """
        UPDATE usuarios
        SET moedas = moedas + %s
        WHERE id_usuario = %s
    """

    # Organiza os valores que serão enviados ao banco.
    valores = (
        quantidade,
        fk_usuario
    )

    # Executa o comando usando os valores.
    cursor.execute(comando, valores)

    # Confirma a alteração no banco.
    banco.commit()

    # Guarda quantos usuários foram alterados.
    quantidade_alterada = cursor.rowcount

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão.
    banco.close()

    # Retorna a quantidade de registros alterados.
    return quantidade_alterada

# Busca o saldo de moedas do usuário.
def consultar_moedas(fk_usuario):

    # Abre a conexão com o banco.
    banco = conectar_banco()

    # Cria um cursor que retorna os dados como dicionário.
    cursor = banco.cursor(dictionary=True)

    # Busca as moedas do usuário.
    comando = """
        SELECT moedas
        FROM usuarios
        WHERE id_usuario = %s
    """

    # Executa a consulta usando o ID do usuário.
    cursor.execute(comando, (fk_usuario,))

    # Pega o resultado encontrado.
    resultado = cursor.fetchone()

    # Fecha o cursor e a conexão.
    cursor.close()
    banco.close()

    # Retorna o saldo encontrado.
    return resultado