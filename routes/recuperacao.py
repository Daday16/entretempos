# Importa o APIRouter para criar as rotas.
from fastapi import APIRouter

# Importa o serviço de recuperação de senha.
from services.recuperacao_service import RecuperacaoService

# Importa a função que envia o código por e-mail.
from utils.email import enviar_codigo_email


# Cria as rotas de recuperação de senha.
router = APIRouter(
    prefix="/recuperacao",
    tags=["Recuperação de senha"]
)


# Cria uma instância do serviço.
recuperacao_service = RecuperacaoService()


@router.post("/solicitar")
def solicitar_recuperacao(email: str):

    # Procura o usuário pelo e-mail informado.
    usuario = recuperacao_service.buscar_usuario_por_email(email)

    # Se o e-mail não existir, mostramos a mesma mensagem.
    if usuario is None:
        return {
            "mensagem": "Se o e-mail estiver cadastrado, você receberá as instruções para recuperar sua senha."
        }

    # Cria um código de recuperação e salva no banco.
    recuperacao = recuperacao_service.criar(
        usuario["id_usuario"]
    )

    # Envia o código para o e-mail do usuário.
    enviar_codigo_email(
        email,
        recuperacao["codigo"]
    )

    # Não mostramos o código na resposta da API.
    return {
        "mensagem": "Se o e-mail estiver cadastrado, você receberá as instruções para recuperar sua senha."
    }


@router.post("/validar")
def validar_codigo(
    id_usuario: int,
    codigo: str
):

    # Verifica se o código informado é válido.
    resultado = recuperacao_service.validar_codigo(
        id_usuario,
        codigo
    )

    # Verifica se o código é inválido.
    if resultado == "codigo_invalido":
        return {
            "mensagem": "Código inválido."
        }

    # Verifica se o código expirou.
    if resultado == "codigo_expirado":
        return {
            "mensagem": "Código expirado."
        }

    # Se chegou aqui, o código é válido.
    return {
        "mensagem": "Código válido!",
        "id_recuperacao": resultado["id_recuperacao"]
    }


@router.post("/redefinir")
def redefinir_senha(
    id_usuario: int,
    id_recuperacao: int,
    nova_senha: str
):

    # Troca a senha do usuário e marca o código como usado.
    resultado = recuperacao_service.redefinir_senha(
        id_usuario,
        id_recuperacao,
        nova_senha
    )

    # Verifica se a senha não pôde ser alterada.
    if resultado is False:
        return {
            "mensagem": "Não foi possível alterar a senha."
        }

    # Informa que a senha foi alterada.
    return {
        "mensagem": "Senha alterada com sucesso!"
    }