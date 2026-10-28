# Importa a função que cria a conexão com o nosso banco MySQL.
from database.conexao import conectar_banco


# Cria uma função responsável por buscar todos os usuários.
def listar_usuarios():

    # Abre uma conexão com o banco de dados.
    banco = conectar_banco()

    # Cria um cursor que retorna os resultados como dicionários.
    cursor = banco.cursor(dictionary=True)

    # Envia para o MySQL um comando pedindo todos os usuários.
    cursor.execute("SELECT * FROM usuarios")

    # Guarda os usuários encontrados.
    usuarios = cursor.fetchall()

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão com o banco.
    banco.close()

    # Devolve os usuários encontrados.
    return usuarios


# Cria uma função responsável por salvar um novo usuário no banco.
def criar_usuario(usuario):

    # Abre uma conexão com o banco de dados.
    banco = conectar_banco()

    # Cria um cursor para enviar comandos SQL ao MySQL.
    cursor = banco.cursor()

    # Comando SQL que insere um novo usuário na tabela.
    comando = """
        INSERT INTO usuarios
        (nome_usuario, email, senha, data_cadastro, data_nascimento)
        VALUES (%s, %s, %s, %s, %s)
    """

    # Os valores são enviados separadamente do comando SQL.
    valores = (
        usuario.nome_usuario,
        usuario.email,
        usuario.senha,
        usuario.data_cadastro,
        usuario.data_nascimento
    )

    # Executa o comando.
    cursor.execute(comando, valores)

    # Confirma a alteração no banco de dados.
    banco.commit()

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão com o banco.
    banco.close()


# Cria uma função para procurar um usuário pelo e-mail.
def buscar_por_email(email):

    # Abre uma conexão com o banco de dados.
    banco = conectar_banco()

    # Cria um cursor que retorna o resultado como dicionário.
    cursor = banco.cursor(dictionary=True)

    # Comando SQL para procurar o usuário pelo e-mail.
    comando = """
        SELECT *
        FROM usuarios
        WHERE email = %s
    """

    # Executa o comando usando o e-mail recebido.
    cursor.execute(comando, (email,))

    # Pega o primeiro usuário encontrado.
    usuario = cursor.fetchone()

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão com o banco.
    banco.close()

    # Devolve o usuário encontrado.
    return usuario


# Cria uma função para atualizar a senha de um usuário.
def atualizar_senha(id_usuario, nova_senha):

    # Abre uma conexão com o banco de dados.
    banco = conectar_banco()

    # Cria um cursor para enviar o comando SQL.
    cursor = banco.cursor()

    # Comando SQL que troca a senha do usuário.
    comando = """
        UPDATE usuarios
        SET senha = %s
        WHERE id_usuario = %s
    """

    # Valores que serão enviados para o MySQL.
    valores = (
        nova_senha,
        id_usuario
    )

    # Executa a atualização.
    cursor.execute(comando, valores)

    # Confirma a alteração no banco.
    banco.commit()

    # Guarda quantas linhas foram alteradas.
    quantidade_alterada = cursor.rowcount

    # Fecha o cursor.
    cursor.close()

    # Fecha a conexão com o banco.
    banco.close()

    # Devolve a quantidade de usuários alterados.
    return quantidade_alterada