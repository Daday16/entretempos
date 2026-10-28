# Importa o APIRouter para criar as rotas.
# Depends permite buscar o usuário pelo token.
from fastapi import APIRouter, Depends

# Importa o modelo Grupo.
from models.grupo import Grupo

# Importa o Service responsável pelos grupos.
from services.grupo_service import GrupoService

# Importa a função que identifica o usuário pelo token.
from auth.jwt import obter_usuario_token


# Cria uma instância do Service.
grupo_service = GrupoService()


# Cria o grupo de rotas dos grupos.
router = APIRouter(
    prefix="/grupos",
    tags=["Grupos"]
)


# Cria a rota para cadastrar um novo grupo.
@router.post("/")
def cadastrar_grupo(
    titulo: str,
    fk_usuario: int = Depends(obter_usuario_token)
):
    # Cria um objeto Grupo com o título e o dono.
    grupo = Grupo(
        titulo=titulo,
        fk_usuario=fk_usuario
    )

    # Envia o grupo para o Service validar e salvar.
    resultado = grupo_service.criar_grupo(grupo)

    # Verifica se o título é inválido.
    if resultado == "titulo_invalido":

        # Retorna uma mensagem de erro.
        return {
            "mensagem": "O título não pode ficar vazio."
        }

    # Retorna uma mensagem de sucesso.
    return {
        "mensagem": "Grupo cadastrado com sucesso!"
    }


# Cria a rota para consultar os grupos do usuário conectado.
@router.get("/")
def consultar_grupos(
    fk_usuario: int = Depends(obter_usuario_token)
):
    # Busca os grupos pertencentes ao usuário autenticado.
    grupos = grupo_service.buscar_grupos(fk_usuario)

    # Retorna os grupos encontrados.
    return grupos