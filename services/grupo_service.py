# Importa as funções que trabalham com grupos no banco de dados.
from repositories.grupo_repository import (
    criar_grupo,
    buscar_grupos_por_usuario
)


# Cria a classe responsável pelas regras dos grupos.
class GrupoService:

    # Cria a função responsável por cadastrar um grupo.
    def criar_grupo(self, grupo):

        # Remove espaços do começo e do final do título.
        titulo_limpo = grupo.titulo.strip()

        # Verifica se o título ficou vazio.
        if titulo_limpo == "":

            # Informa que o título não é válido.
            return "titulo_invalido"

        # Salva o grupo no banco de dados.
        criar_grupo(grupo)

        # Informa que o grupo foi criado com sucesso.
        return True

    # Cria a função responsável por buscar os grupos de um usuário.
    def buscar_grupos(self, fk_usuario):

        # Busca os grupos no banco usando o ID do usuário.
        grupos = buscar_grupos_por_usuario(fk_usuario)

        # Retorna os grupos encontrados.
        return grupos