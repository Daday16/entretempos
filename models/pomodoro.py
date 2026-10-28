# Importa o datetime para registrar data e hora.
from datetime import datetime


# Cria a classe que representa uma sessão de Pomodoro.
class Pomodoro:

    # O __init__ é executado quando criamos uma nova sessão.
    def __init__(
        self,
        duracao,
        fk_usuario,
        dthr_inicio=None,
        dthr_termino=None
    ):

        # Guarda a duração planejada da sessão em minutos.
        self.duracao = duracao

        # Guarda o ID do usuário dono do Pomodoro.
        self.fk_usuario = fk_usuario

        # Guarda o momento em que o Pomodoro começou.
        self.dthr_inicio = dthr_inicio

        # Guarda o momento em que o Pomodoro terminou.
        self.dthr_termino = dthr_termino