
from pydantic import BaseModel, Field


class MensagemApoio(BaseModel):

    mensagem: str = Field(
        min_length=1,
        max_length=1000
    )

    historico: list[dict] = Field(
        default_factory=list,
        max_length=8
    )
