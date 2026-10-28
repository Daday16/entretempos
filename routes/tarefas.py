# Importa as ferramentas para criar rotas e acessar o usuário conectado.
from fastapi import APIRouter, Depends

# Importa a função que identifica o usuário pelo token.
from auth.jwt import obter_usuario_token

# Importa o modelo Tarefa.
from models.tarefa import Tarefa

# Importa o Service responsável pelas tarefas.
from services.tarefa_service import TarefaService


# Cria uma instância do Service.
tarefa_service = TarefaService()


# Cria o grupo de rotas das tarefas.
router = APIRouter(
    prefix="/tarefas",
    tags=["Tarefas"]
)


# Cria uma rota para cadastrar uma tarefa.
@router.post("/")
def cadastrar_tarefa(
    titulo: str,
    descricao: str = "",
    dthr_prazo: str = "",
    frequencia: int = 0,
    fk_grupo: int = None,
    fk_usuario: int = Depends(obter_usuario_token)
):

    # Cria um objeto Tarefa com os dados recebidos.
    tarefa = Tarefa(
        titulo=titulo,
        descricao=descricao,
        dthr_prazo=dthr_prazo,
        frequencia=frequencia,
        fk_grupo=fk_grupo
    )

    # Envia a tarefa e o usuário para o Service.
    resultado = tarefa_service.criar_tarefa(
        tarefa,
        fk_usuario
    )

    # Verifica se o título está vazio.
    if resultado == "titulo_invalido":
        return {
            "mensagem": "O título não pode ficar vazio."
        }

    # Verifica se o grupo não pertence ao usuário.
    if resultado == "grupo_sem_permissao":
        return {
            "mensagem": "Você não tem permissão para usar este grupo."
        }

    # Verifica se a tarefa não recebeu um grupo.
    if resultado == "grupo_obrigatorio":
        return {
        "mensagem": "Você precisa escolher um grupo para criar a tarefa."
    }

    # Retorna mensagem de sucesso.
    return {
        "mensagem": "Tarefa cadastrada com sucesso!"
    }

# Cria a rota para consultar as tarefas de um grupo.
@router.get("/grupo/{fk_grupo}")
def consultar_tarefas_por_grupo(
    fk_grupo: int,
    fk_usuario: int = Depends(obter_usuario_token)
):

    # Busca as tarefas verificando o grupo e o usuário conectado.
    tarefas = tarefa_service.buscar_tarefas_por_grupo(
        fk_grupo,
        fk_usuario
    )

    # Retorna as tarefas encontradas.
    return tarefas

# Cria a rota responsável por editar uma tarefa.
@router.put("/{id_tarefa}")
def atualizar_tarefa(
    id_tarefa: int,
    titulo: str,
    descricao: str = "",
    fk_usuario: int = Depends(obter_usuario_token)
):

    # Envia os dados para o Service editar a tarefa.
    resultado = tarefa_service.editar_tarefa(
        id_tarefa,
        titulo,
        descricao,
        fk_usuario
    )

    # Verifica se o título está vazio.
    if resultado == "titulo_invalido":
        return {
            "mensagem": "O título não pode ficar vazio."
        }

    # Verifica se nenhuma tarefa foi alterada.
    if resultado == 0:
        return {
            "mensagem": "Tarefa não encontrada ou sem permissão."
        }

    # Informa que a tarefa foi editada.
    return {
        "mensagem": "Tarefa editada com sucesso!"
    }

# Cria a rota responsável por excluir uma tarefa.
@router.delete("/{id_tarefa}")
def remover_tarefa(
    id_tarefa: int,
    fk_usuario: int = Depends(obter_usuario_token)
):

    # Envia os dados para o Service excluir a tarefa.
    resultado = tarefa_service.excluir_tarefa(
        id_tarefa,
        fk_usuario
    )

    # Verifica se nenhuma tarefa foi excluída.
    if resultado == 0:
        return {
            "mensagem": "Tarefa não encontrada ou sem permissão."
        }

    # Informa que a tarefa foi excluída com sucesso.
    return {
        "mensagem": "Tarefa excluída com sucesso!"
    }

# Cria a rota responsável por concluir uma tarefa.
@router.put("/concluir/{id_tarefa}")
def marcar_tarefa_concluida(
    id_tarefa: int,
    fk_usuario: int = Depends(obter_usuario_token)
):

    # Envia os dados para o Service atualizar o status.
    resultado = tarefa_service.concluir_tarefa(
        id_tarefa,
        fk_usuario
    )

    # Verifica se nenhuma tarefa foi alterada.
    if resultado == 0:
        return {
            "mensagem": "Tarefa não encontrada ou sem permissão."
        }

    # Informa que a tarefa foi concluída.
    return {
        "mensagem": "Tarefa concluída com sucesso!"
    }