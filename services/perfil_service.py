# Importa as funções que trabalham com perfis no banco de dados.
from repositories.perfil_repository import (
    criar_perfil,
    buscar_perfil_por_usuario,
    editar_perfil
)


# Cria a classe responsável pelas regras do perfil.
class PerfilService:

    # Cria a função responsável por cadastrar um perfil.
    def criar_perfil(self, perfil, fk_usuario):

        # Remove os espaços do começo e do final do objetivo.
        objetivo_limpo = perfil.objetivo.strip()

        # Verifica se o objetivo ficou vazio.
        if objetivo_limpo == "":
            return "objetivo_invalido"

        # Verifica se o tempo de estudo é maior que zero.
        if perfil.tempo_diario <= 0:
            return "tempo_invalido"

        # Lista os níveis de conhecimento aceitos.
        niveis_validos = [
            "Nenhum",
            "Iniciante",
            "Básico",
            "Intermediário",
            "Avançado"
        ]

        # Verifica se o nível informado é válido.
        if perfil.nivel_conhecimento not in niveis_validos:
            return "nivel_invalido"

        # Lista os dias da semana aceitos.
        dias_validos = [
            "segunda",
            "terça",
            "quarta",
            "quinta",
            "sexta",
            "sábado",
            "domingo"
        ]

        # Divide os dias enviados pela pessoa usando a vírgula.
        dias_escolhidos = [
            dia.strip().lower()
            for dia in perfil.dias_disponiveis.split(",")
        ]

        # Verifica se nenhum dia foi escolhido.
        if dias_escolhidos == [""]:
            return "dias_invalidos"

        # Verifica se existe algum dia inválido.
        if any(dia not in dias_validos for dia in dias_escolhidos):
            return "dias_invalidos"

        # Envia o perfil para o Repository salvar no MySQL.
        criar_perfil(perfil, fk_usuario)

        # Informa que o perfil foi criado com sucesso.
        return True


    # Cria a função responsável por buscar o perfil do usuário.
    def buscar_perfil(self, fk_usuario):

        # Busca o perfil no banco de dados usando o ID do usuário.
        perfil = buscar_perfil_por_usuario(fk_usuario)

        # Verifica se nenhum perfil foi encontrado.
        if perfil is None:
            return "perfil_nao_encontrado"

        # Retorna os dados do perfil encontrado.
        return perfil


    # Cria a função responsável por editar o perfil.
    def editar_perfil(
        self,
        fk_usuario,
        objetivo,
        nivel_conhecimento,
        tempo_diario,
        dias_disponiveis,
        dificuldade_foco
    ):

        # Remove espaços do começo e do final do objetivo.
        objetivo_limpo = objetivo.strip()

        # Verifica se o objetivo ficou vazio.
        if objetivo_limpo == "":
            return "objetivo_invalido"

        # Verifica se o tempo diário é maior que zero.
        if tempo_diario <= 0:
            return "tempo_invalido"

        # Lista os níveis de conhecimento aceitos.
        niveis_validos = [
            "Nenhum",
            "Iniciante",
            "Básico",
            "Intermediário",
            "Avançado"
        ]

        # Verifica se o nível informado é válido.
        if nivel_conhecimento not in niveis_validos:
            return "nivel_invalido"

        # Lista os dias da semana aceitos.
        dias_validos = [
            "segunda",
            "terça",
            "quarta",
            "quinta",
            "sexta",
            "sábado",
            "domingo"
        ]

        # Divide os dias enviados usando a vírgula.
        dias_escolhidos = [
            dia.strip().lower()
            for dia in dias_disponiveis.split(",")
        ]

        # Verifica se nenhum dia foi escolhido.
        if dias_escolhidos == [""]:
            return "dias_invalidos"

        # Verifica se existe algum dia inválido.
        if any(dia not in dias_validos for dia in dias_escolhidos):
            return "dias_invalidos"

        # Envia os dados para o Repository editar o perfil.
        quantidade_alterada = editar_perfil(
            fk_usuario,
            objetivo_limpo,
            nivel_conhecimento,
            tempo_diario,
            dias_disponiveis,
            dificuldade_foco
        )

        # Retorna a quantidade de registros alterados.
        return quantidade_alterada