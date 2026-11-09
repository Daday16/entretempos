
from fastapi import APIRouter

from services.usuario_service import UsuarioService
from models.usuario import Usuario
from auth.jwt import criar_token


# Instância do serviço de usuários.
usuario_service = UsuarioService()

# Grupo de rotas dos usuários.
router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


# Rota de teste.
@router.get("/")
def listar_usuarios():
    return {"mensagem": "Rota de usuários funcionando!"}


# Rota de login.
@router.post("/login")
def login(email: str, senha: str):

    try:
        usuario = usuario_service.login(email, senha)

        if usuario is None:
            return {"mensagem": "E-mail ou senha incorretos."}

        token = criar_token(usuario["id_usuario"])

        return {
            "mensagem": "Login realizado com sucesso!",
            "usuario": usuario["nome_usuario"],
            "token": token
        }

    except ValueError:
        return {"mensagem": "E-mail ou senha incorretos."}


# Rota de cadastro.
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

    try:
        resultado = usuario_service.criar_usuario(usuario)

        if resultado is True:
            return {
                "mensagem": "Usuário cadastrado com sucesso!"
            }

        return {
            "mensagem": "Não foi possível cadastrar o usuário."
        }

    except ValueError as erro:
        return {
            "mensagem": str(erro)
        }
