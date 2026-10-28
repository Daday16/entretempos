# Importa BaseModel para criar um modelo de dados.
from pydantic import BaseModel


# Representa uma etapa individual da trilha de estudos.
class EtapaTrilha(BaseModel):

    # Nome da etapa de estudo.
    titulo: str

    # Explica o que a pessoa vai aprender nessa etapa.
    descricao: str

    # Lista dos assuntos que serão estudados.
    assuntos: list[str]


# Representa a trilha completa criada pela IA.
class TrilhaEstudos(BaseModel):

    # Nome geral da trilha.
    titulo: str

    # Pequena explicação sobre a trilha criada.
    descricao: str

    # Lista de etapas que a pessoa deverá seguir.
    etapas: list[EtapaTrilha]