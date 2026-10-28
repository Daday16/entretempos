# Cria a classe que representa um grupo de tarefas do Entretempos.
class Grupo:

    # O __init__ é executado quando criamos um novo grupo.
    def __init__(self, titulo, fk_usuario):

        # Guarda o título do grupo.
        self.titulo = titulo

        # Guarda o ID do usuário dono do grupo.
        self.fk_usuario = fk_usuario