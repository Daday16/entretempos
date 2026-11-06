
import json

from fastapi import APIRouter, Depends, HTTPException, Query

from auth.jwt import obter_usuario_token
from models.mensagem_apoio import MensagemApoio
from services.agente_apoio_service import AgenteApoioService


router = APIRouter(
    prefix="/apoio",
    tags=["Apoio do Pipo"]
)

agente_apoio = AgenteApoioService()


@router.post("/mensagem")
def enviar_mensagem_ao_pipo(

    mensagem: str = Query(
        ...,
        min_length=1,
        max_length=1000
    ),

    historico: str = Query(
        "[]",
        max_length=12000
    ),

    fk_usuario: int = Depends(obter_usuario_token)

):

    """
    Recebe uma mensagem e retorna uma resposta do Pipo.

    O histórico é temporário e enviado pelo navegador.
    Não é salvo no banco de dados.
    """

    try:

        historico_json = json.loads(historico)

        if not isinstance(historico_json, list):
            historico_json = []

    except (json.JSONDecodeError, TypeError):

        historico_json = []

    try:

        entrada = MensagemApoio(
            mensagem=mensagem,
            historico=historico_json[-8:]
        )

    except Exception as erro:

        raise HTTPException(
            status_code=422,
            detail="Mensagem inválida."
        ) from erro

    resultado = agente_apoio.responder(
        entrada.mensagem,
        entrada.historico
    )

    return resultado
