# Importa a função que verifica se o grupo pertence ao usuário.
from repositories.grupo_repository import verificar_grupo_usuario


# Importa as funções que trabalham com tarefas no banco de dados.
from repositories.tarefa_repository import (
    criar_tarefa,
    buscar_tarefas_por_grupo,
    editar_tarefa,
    excluir_tarefa,
    concluir_tarefa
)


# Cria a classe responsável pelas regras das tarefas.
class TarefaService:

    # Cria a função responsável por cadastrar uma tarefa.
    def criar_tarefa(self, tarefa, fk_usuario):

        # Remove espaços do começo e do final do título.
        titulo_limpo = tarefa.titulo.strip()

        # Verifica se o título ficou vazio.
        if titulo_limpo == "":
            return "titulo_invalido"

        # Verifica se a tarefa recebeu um grupo.
        if tarefa.fk_grupo is None:
            return "grupo_obrigatorio"

        # Verifica se o grupo pertence ao usuário conectado.
        grupo = verificar_grupo_usuario(
            tarefa.fk_grupo,
            fk_usuario
        )

        # Se o grupo não existir ou não pertencer ao usuário,
        # impede o cadastro da tarefa.
        if grupo is None:
            return "grupo_sem_permissao"

        # Atualiza o título da tarefa sem espaços desnecessários.
        tarefa.titulo = titulo_limpo

        # Salva a tarefa no banco de dados.
        criar_tarefa(tarefa)

        # Informa que a tarefa foi criada com sucesso.
        return True


    # Cria a função responsável por buscar tarefas de um grupo.
    # Recebe o ID do grupo e o ID do usuário conectado.
    def buscar_tarefas_por_grupo(self, fk_grupo, fk_usuario):

        # Busca as tarefas no banco usando os dois IDs.
        tarefas = buscar_tarefas_por_grupo(
            fk_grupo,
            fk_usuario
        )

        # Retorna as tarefas encontradas.
        return tarefas


    # Cria a função responsável por editar uma tarefa.
    def editar_tarefa(
        self,
        id_tarefa,
        titulo,
        descricao,
        fk_usuario
    ):

        # Remove espaços do começo e do final do título.
        titulo_limpo = titulo.strip()

        # Verifica se o título ficou vazio.
        if titulo_limpo == "":
            return "titulo_invalido"

        # Envia os dados para o Repository editar a tarefa.
        quantidade_alterada = editar_tarefa(
            id_tarefa,
            titulo_limpo,
            descricao,
            fk_usuario
        )

        # Retorna a quantidade de tarefas alteradas.
        return quantidade_alterada


    # Cria a função responsável por excluir uma tarefa.
    def excluir_tarefa(self, id_tarefa, fk_usuario):

        # Envia os dados para o Repository excluir a tarefa.
        quantidade_excluida = excluir_tarefa(
            id_tarefa,
            fk_usuario
        )

        # Retorna a quantidade de tarefas excluídas.
        return quantidade_excluida


    # Cria a função responsável por concluir uma tarefa.
    def concluir_tarefa(self, id_tarefa, fk_usuario):

        # Envia os dados para o Repository atualizar o status.
        quantidade_alterada = concluir_tarefa(
            id_tarefa,
            fk_usuario
        )

        # Retorna a quantidade de tarefas alteradas.
        return quantidade_alterada