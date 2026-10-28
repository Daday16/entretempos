# Importa a data e hora atuais.
from datetime import datetime

# Importa as funções do Repository do Pomodoro.
from repositories.pomodoro_repository import (
    iniciar_pomodoro,
    buscar_pomodoro_ativo,
    finalizar_pomodoro,
    adicionar_moedas,
    consultar_moedas
)

# Importa o modelo do Pomodoro.
from models.pomodoro import Pomodoro


# Cria a classe responsável pelas regras do Pomodoro.
class PomodoroService:

    # Inicia uma nova sessão de Pomodoro.
    def iniciar(self, duracao, fk_usuario):

        # Verifica se a duração é válida.
        if duracao <= 0:
            return "duracao_invalida"

        # Procura se o usuário já possui um Pomodoro ativo.
        pomodoro_ativo = buscar_pomodoro_ativo(fk_usuario)

        # Impede o início de dois Pomodoros ao mesmo tempo.
        if pomodoro_ativo is not None:
            return "pomodoro_ativo"

        # Registra o momento atual como início.
        dthr_inicio = datetime.now()

        # Cria o Pomodoro sem horário de término.
        pomodoro = Pomodoro(
            duracao=duracao,
            fk_usuario=fk_usuario,
            dthr_inicio=dthr_inicio,
            dthr_termino=None
        )

        # Salva o Pomodoro no banco de dados.
        iniciar_pomodoro(pomodoro)

        # Informa que o cadastro foi realizado.
        return True

    # Finaliza uma sessão de Pomodoro.
    def finalizar(self, id_pomodoro, fk_usuario):

        # Registra o momento atual como horário de término.
        dthr_termino = datetime.now()

        # Atualiza o Pomodoro no banco de dados.
        quantidade_alterada = finalizar_pomodoro(
            id_pomodoro,
            fk_usuario,
            dthr_termino
        )

        # Verifica se algum Pomodoro foi encontrado e finalizado.
        if quantidade_alterada == 0:
            return "pomodoro_nao_encontrado"

        # Informa que a finalização deu certo.
        return True

    # Busca o Pomodoro que está em andamento.
    def consultar_ativo(self, fk_usuario):

        # Procura o Pomodoro ativo desse usuário no banco.
        pomodoro_ativo = buscar_pomodoro_ativo(fk_usuario)

        # Se não existir um Pomodoro ativo, retorna uma mensagem.
        if pomodoro_ativo is None:
            return "nenhum_pomodoro_ativo"

        # Pega o horário em que o Pomodoro começou.
        dthr_inicio = pomodoro_ativo["dthr_inicio"]

        # Descobre quanto tempo já passou desde o início.
        tempo_passado = datetime.now() - dthr_inicio

        # Converte o tempo passado para segundos.
        segundos_passados = int(tempo_passado.total_seconds())

        # Converte a duração planejada para segundos.
        duracao_segundos = pomodoro_ativo["duracao"] * 60

        # Calcula quantos segundos ainda faltam.
        tempo_restante = duracao_segundos - segundos_passados

        # Impede que o tempo restante fique negativo.
        if tempo_restante < 0:
            tempo_restante = 0

        # Verifica se o tempo do Pomodoro chegou ao fim.
        if tempo_restante == 0:

            # Registra o momento em que o Pomodoro terminou.
            dthr_termino = datetime.now()

            # Finaliza o Pomodoro no banco de dados.
            quantidade_alterada = finalizar_pomodoro(
                pomodoro_ativo["id_pomodoro"],
                fk_usuario,
                dthr_termino
            )

            # Verifica se o Pomodoro foi realmente finalizado.
            if quantidade_alterada > 0:

                # Calcula 2 moedas para cada 5 minutos completos.
                moedas = (pomodoro_ativo["duracao"] // 5) * 2

                # Adiciona as moedas ao saldo do usuário.
                adicionar_moedas(
                    fk_usuario,
                    moedas
                )

            # Informa que o Pomodoro foi concluído.
            return "pomodoro_concluido"

        # Adiciona o tempo restante aos dados do Pomodoro.
        pomodoro_ativo["tempo_restante_segundos"] = tempo_restante

        # Retorna os dados atualizados.
        return pomodoro_ativo

    # Consulta o saldo de moedas do usuário.
    def consultar_moedas(self, fk_usuario):

        # Busca as moedas no banco de dados.
        resultado = consultar_moedas(fk_usuario)

        # Retorna o saldo encontrado.
        return resultado