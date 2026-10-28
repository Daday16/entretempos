# Cria a classe que representa o perfil do usuário.
class Perfil:

    # Cria um novo perfil com as informações do onboarding.
    def __init__(
        self,
        objetivo,
        nivel_conhecimento,
        tempo_diario,
        dias_disponiveis,
        dificuldade_foco
    ):

        # Guarda o objetivo de aprendizagem da pessoa.
        self.objetivo = objetivo

        # Guarda o nível de conhecimento na área escolhida.
        self.nivel_conhecimento = nivel_conhecimento

        # Guarda quantos minutos a pessoa tem disponíveis por dia.
        self.tempo_diario = tempo_diario

        # Guarda os dias da semana em que a pessoa pode estudar.
        self.dias_disponiveis = dias_disponiveis

        # Guarda a principal dificuldade relacionada ao foco.
        self.dificuldade_foco = dificuldade_foco