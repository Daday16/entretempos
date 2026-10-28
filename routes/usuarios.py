# Importa o APIRouter para criar nossas rotas.
from fastapi import APIRouter

# Importa o UsuarioService para usar as regras dos usuários.
from services.usuario_service import UsuarioService

# Importa o modelo Usuario.
# Ele representa um novo usuário que será cadastrado.
from models.usuario import Usuario

# Importa a função responsável por criar o token de autenticação.
from auth.jwt import criar_token

# Cria uma instância do serviço de usuários.
# É ela que vai cuidar das regras de login.
usuario_service = UsuarioService()

# Cria o "grupo de rotas" dos usuários.
router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


# Cria nossa primeira rota de usuário.
@router.get("/")
def listar_usuarios():
    # Por enquanto, estamos apenas testando a rota.
    return {"mensagem": "Rota de usuários funcionando!"}

# Cria a rota responsável pelo login.
# O método POST será usado porque estamos enviando dados para o backend.
@router.post("/login")
def login(email: str, senha: str):

    # Envia o e-mail e a senha para o Service verificar.
    usuario = usuario_service.login(email, senha)

    # Verifica se o login não foi autorizado.
    if usuario is None:

        # Retorna uma mensagem informando que os dados estão incorretos.
        return {"mensagem": "E-mail ou senha incorretos."}

    # Retorna uma mensagem de sucesso e o nome do usuário.
    # Não enviamos a senha/hash para o frontend.

    # Cria um token usando o ID do usuário.
    token = criar_token(usuario["id_usuario"])

    # Retorna a mensagem, o nome e o token para o frontend.
    return {
        "mensagem": "Login realizado com sucesso!",
        "usuario": usuario["nome_usuario"],
        "token": token
    }
    
# Cria a rota responsável pelo cadastro de um novo usuário.
# O método POST será usado porque estamos enviando novos dados.

@router.post("/cadastro")
def cadastrar_usuario(
    nome_usuario: str,
    email: str,
    senha: str,
    data_nascimento: str
):
    usuario = Usuario(
        nome_usuario=nome_usuario,
        email=email,
        senha=senha,
        data_nascimento=data_nascimento
    )

    resultado = usuario_service.criar_usuario(usuario)

    if resultado == "nome_invalido":
        return {"mensagem": "O nome não pode ficar vazio."}

    if resultado is False:
        return {"mensagem": "Este e-mail já está cadastrado."}

    if resultado == "email_invalido":
        return {"mensagem": "Digite um e-mail válido."}

    if resultado == "senha_invalida":
        return {
            "mensagem": "A senha deve ter pelo menos 8 caracteres, um número e um símbolo."
        }

    if resultado == "data_nascimento_invalida":
        return {
            "mensagem": "Data de nascimento inválida. Confira o formato e tente novamente."
        }

    if resultado is True:
        return {"mensagem": "Usuário cadastrado com sucesso!"}

    return {"mensagem": "Não foi possível cadastrar o usuário."}
