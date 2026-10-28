# Importa a função responsável por salvar a trilha no banco.
from repositories.trilha_repository import criar_trilha

# Importa a função responsável por salvar cada etapa da trilha.
from repositories.etapa_trilha_repository import criar_etapa

# Importa a função responsável por salvar cada assunto da trilha.
from repositories.assunto_trilha_repository import criar_assunto


# Cria a classe responsável pelas regras das trilhas.
class TrilhaService:

    # Cria uma trilha para o usuário.
    def criar_trilha(self, fk_usuario, trilha):

        # Verifica se o título da trilha está vazio.
        if trilha.titulo.strip() == "":
            return "titulo_invalido"

        # Verifica se a trilha possui pelo menos uma etapa.
        if not trilha.etapas:
            return "etapas_invalidas"

        # Salva a trilha principal no banco de dados.
        id_trilha = criar_trilha(
            fk_usuario,
            trilha
        )

        # Percorre todas as etapas criadas pela IA.
        for ordem_etapa, etapa in enumerate(trilha.etapas, start=1):

            # Salva a etapa vinculada à trilha.
            id_etapa = criar_etapa(
                id_trilha,
                etapa,
                ordem_etapa
            )

            # Percorre todos os assuntos da etapa.
            for ordem_assunto, assunto in enumerate(etapa.assuntos, start=1):

                # Salva o assunto vinculado à etapa.
                criar_assunto(
                    id_etapa,
                    assunto,
                    ordem_assunto
                )

        # Retorna o ID da trilha criada.
        return id_trilha