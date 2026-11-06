
from repositories.grupo_repository import verificar_grupo_usuario

from repositories.tarefa_repository import (
    criar_tarefa,
    buscar_tarefas_por_grupo,
    editar_tarefa,
    excluir_tarefa,
    concluir_tarefa as concluir_tarefa_repository
)


class TarefaService:

    def criar_tarefa(self, tarefa, fk_usuario):
        titulo_limpo = tarefa.titulo.strip()

        if titulo_limpo == "":
            return "titulo_invalido"

        if tarefa.fk_grupo is None:
            return "grupo_obrigatorio"

        grupo = verificar_grupo_usuario(
            tarefa.fk_grupo,
            fk_usuario
        )

        if grupo is None:
            return "grupo_sem_permissao"

        tarefa.titulo = titulo_limpo
        criar_tarefa(tarefa)

        return True

    def buscar_tarefas_por_grupo(self, fk_grupo, fk_usuario):
        return buscar_tarefas_por_grupo(fk_grupo, fk_usuario)

    def editar_tarefa(self, id_tarefa, titulo, descricao, fk_usuario):
        titulo_limpo = titulo.strip()

        if titulo_limpo == "":
            return "titulo_invalido"

        return editar_tarefa(
            id_tarefa,
            titulo_limpo,
            descricao,
            fk_usuario
        )

    def excluir_tarefa(self, id_tarefa, fk_usuario):
        return excluir_tarefa(id_tarefa, fk_usuario)

    def concluir_tarefa(self, id_tarefa, fk_usuario):
        return concluir_tarefa_repository(id_tarefa, fk_usuario)
