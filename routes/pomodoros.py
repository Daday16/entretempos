# Importa o APIRouter para criar as rotas.
# Importa Depends para proteger as rotas com o token.
from fastapi import APIRouter, Depends

# Importa a função que identifica o usuário pelo token.
from auth.jwt import obter_usuario_token

# Importa o Service que contém as regras do Pomodoro.
from services.pomodoro_service import PomodoroService


# Cria o grupo de rotas do Pomodoro.
router = APIRouter(
    prefix="/pomodoros",
    tags=["Pomodoros"]
)

# Cria uma instância do Service.
pomodoro_service = PomodoroService()


# Rota responsável por iniciar um Pomodoro.
@router.post("/iniciar")
def iniciar_pomodoro(
    duracao: int,
    fk_usuario: int = Depends(obter_usuario_token)
):

    # Pede ao Service para iniciar o Pomodoro.
    resultado = pomodoro_service.iniciar(
        duracao,
        fk_usuario
    )

    # Verifica se a duração é inválida.
    if resultado == "duracao_invalida":
        return {
            "mensagem": "A duração deve ser maior que zero."
        }

    # Verifica se já existe um Pomodoro ativo.
    if resultado == "pomodoro_ativo":
        return {
            "mensagem": "Você já possui um Pomodoro em andamento."
        }

    # Retorna uma mensagem de sucesso.
    return {
        "mensagem": "Pomodoro iniciado com sucesso!"
    }

# Rota para finalizar um Pomodoro manualmente.
@router.put("/finalizar/{id_pomodoro}")
def finalizar_pomodoro(
    id_pomodoro: int,
    fk_usuario: int = Depends(obter_usuario_token)
):

    # Pede ao Service para finalizar o Pomodoro.
    resultado = pomodoro_service.finalizar(
        id_pomodoro,
        fk_usuario
    )

    # Verifica se o Pomodoro não foi encontrado.
    if resultado == "pomodoro_nao_encontrado":
        return {
            "mensagem": "Pomodoro não encontrado ou já finalizado."
        }

    # Retorna uma mensagem de sucesso.
    return {
        "mensagem": "Pomodoro finalizado sem recompensa."
    }

# Rota para consultar o Pomodoro ativo do usuário.
@router.get("/ativo")
def consultar_pomodoro_ativo(
    fk_usuario: int = Depends(obter_usuario_token)
):

    # Pede ao Service para buscar o Pomodoro ativo.
    resultado = pomodoro_service.consultar_ativo(
        fk_usuario
    )

    # Verifica se não existe um Pomodoro em andamento.
    if resultado == "nenhum_pomodoro_ativo":
        return {
            "mensagem": "Você não possui um Pomodoro ativo."
        }

    # Verifica se o Pomodoro terminou automaticamente.
    if resultado == "pomodoro_concluido":
        return {
            "mensagem": "Parabéns! Você concluiu seu Pomodoro! 🎉"
        }

    # Retorna os dados do Pomodoro encontrado.
    return resultado

# Rota para consultar o saldo de moedas do usuário.
@router.get("/moedas")
def consultar_moedas(
    fk_usuario: int = Depends(obter_usuario_token)
):
    # Pede ao Service o saldo de moedas do usuário.
    resultado = pomodoro_service.consultar_moedas(fk_usuario)

    # Retorna o saldo encontrado.
    return resultado