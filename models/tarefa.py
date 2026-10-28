# Cria a classe que representa uma tarefa do Entretempos.
class Tarefa:

    # Cria uma nova tarefa com seus dados.
    def __init__(
        self,
        titulo,
        descricao=None,
        dthr_prazo=None,
        frequencia=0,
        fk_grupo=None
    ):

        # Guarda o título da tarefa.
        self.titulo = titulo

        # Guarda a descrição da tarefa.
        self.descricao = descricao

        # Guarda o prazo da tarefa.
        self.dthr_prazo = dthr_prazo

        # Guarda a frequência da tarefa.
        self.frequencia = frequencia

        # Guarda o ID do grupo ao qual a tarefa pertence.
        self.fk_grupo = fk_grupo