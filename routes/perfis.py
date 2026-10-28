# Importa as ferramentas para criar rotas e proteger com token.
from fastapi import APIRouter, Depends, Query

# Importa Enum para criar opções fixas no Swagger.
from enum import Enum

# Importa a função que identifica o usuário pelo token.
from auth.jwt import obter_usuario_token

# Importa o modelo Perfil.
from models.perfil import Perfil

# Importa o Service responsável pelas regras do perfil.
from services.perfil_service import PerfilService


# Cria uma lista de opções fixas para o nível de conhecimento.
class NivelConhecimento(str, Enum):

    # Pessoa que ainda não possui conhecimento.
    NENHUM = "Nenhum"

    # Pessoa que está começando a aprender.
    INICIANTE = "Iniciante"

    # Pessoa com conhecimento básico.
    BASICO = "Básico"

    # Pessoa com conhecimento intermediário.
    INTERMEDIARIO = "Intermediário"

    # Pessoa com conhecimento avançado.
    AVANCADO = "Avançado"


# Cria uma instância do Service.
perfil_service = PerfilService()


# Cria o grupo de rotas dos perfis.
router = APIRouter(
    prefix="/perfis",
    tags=["Perfis"]
)


# Cria a rota responsável por cadastrar um perfil.
@router.post("/")
def cadastrar_perfil(
    objetivo: str,
    nivel_conhecimento: NivelConhecimento,
    dias_disponiveis: str,
    tempo_diario: int = Query(
        ...,
        description="Minutos disponíveis por dia. Ex: 15, 30 ou 60."
    ),
    dificuldade_foco: str = "",
    fk_usuario: int = Depends(obter_usuario_token)
):

    # Cria um objeto Perfil com as respostas do onboarding.
    perfil = Perfil(
        objetivo,
        nivel_conhecimento.value,
        tempo_diario,
        dias_disponiveis,
        dificuldade_foco
    )

    # Envia o perfil para o Service salvar no banco.
    resultado = perfil_service.criar_perfil(
        perfil,
        fk_usuario
    )

    # Verifica se o objetivo não foi preenchido.
    if resultado == "objetivo_invalido":
        return {
            "mensagem": "O objetivo não pode ficar vazio."
        }

    # Verifica se o tempo diário não é válido.
    if resultado == "tempo_invalido":
        return {
            "mensagem": "O tempo diário deve ser maior que zero."
        }

    # Verifica se o nível de conhecimento não é válido.
    if resultado == "nivel_invalido":
        return {
            "mensagem": "Escolha um nível de conhecimento válido."
        }

    # Verifica se os dias disponíveis não são válidos.
    if resultado == "dias_invalidos":
        return {
            "mensagem": "Escolha pelo menos um dia válido para estudar."
        }

    # Retorna uma mensagem informando que deu certo.
    return {
        "mensagem": "Perfil cadastrado com sucesso!"
    }


# Cria uma rota GET para consultar o próprio perfil.
@router.get("/")
def consultar_perfil(
    fk_usuario: int = Depends(obter_usuario_token)
):

    # Pede ao Service para buscar o perfil do usuário conectado.
    resultado = perfil_service.buscar_perfil(fk_usuario)

    # Verifica se o usuário não possui um perfil cadastrado.
    if resultado == "perfil_nao_encontrado":
        return {
            "mensagem": "Perfil não encontrado."
        }

    # Retorna os dados do perfil encontrado.
    return resultado


# Cria a rota responsável por editar o perfil do usuário.
@router.put("/")
def atualizar_perfil(
    objetivo: str,
    nivel_conhecimento: NivelConhecimento,
    tempo_diario: int,
    dias_disponiveis: str,
    dificuldade_foco: str = "",
    fk_usuario: int = Depends(obter_usuario_token)
):

    # Envia os dados para o Service editar o perfil.
    resultado = perfil_service.editar_perfil(
        fk_usuario,
        objetivo,
        nivel_conhecimento.value,
        tempo_diario,
        dias_disponiveis,
        dificuldade_foco
    )

    # Verifica se o objetivo está vazio.
    if resultado == "objetivo_invalido":
        return {
            "mensagem": "O objetivo não pode ficar vazio."
        }

    # Verifica se o tempo diário é válido.
    if resultado == "tempo_invalido":
        return {
            "mensagem": "O tempo diário deve ser maior que zero."
        }

    # Verifica se o nível de conhecimento é válido.
    if resultado == "nivel_invalido":
        return {
            "mensagem": "Escolha um nível de conhecimento válido."
        }

    # Verifica se os dias disponíveis são inválidos.
    if resultado == "dias_invalidos":
        return {
            "mensagem": "Escolha pelo menos um dia válido para estudar."
        }

    # Verifica se nenhum perfil foi alterado.
    if resultado == 0:
        return {
            "mensagem": "Perfil não encontrado."
        }

    # Informa que o perfil foi editado.
    return {
        "mensagem": "Perfil editado com sucesso!"
    }