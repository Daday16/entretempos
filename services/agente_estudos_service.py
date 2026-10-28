# Importa o cliente oficial do Google Gemini.
from google import genai

# Importa o modelo estruturado da trilha.
from models.trilha import TrilhaEstudos

# Importa o serviço responsável por salvar a trilha.
from services.trilha_service import TrilhaService

# Importa o os para acessar as variáveis de ambiente.
import os

# Importa a função que carrega as informações do arquivo .env.
from dotenv import load_dotenv


# Carrega as configurações salvas no arquivo .env.
load_dotenv()


# Cria o cliente do Gemini usando a chave armazenada no .env.
cliente_gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Cria uma instância do serviço responsável pelas trilhas.
trilha_service = TrilhaService()


# Cria a classe responsável pelo agente de estudos.
class AgenteEstudosService:

    # Cria a função que gera e salva uma trilha personalizada.
    def criar_trilha(
        self,
        fk_usuario,
        objetivo,
        nivel_conhecimento,
        tempo_diario,
        dias_disponiveis,
        dificuldade_foco
    ):
        # Junta as informações do perfil do usuário.
        informacoes_usuario = f"""
        Objetivo: {objetivo}
        Nível de conhecimento: {nivel_conhecimento}
        Tempo disponível por dia: {tempo_diario} minutos
        Dias disponíveis: {dias_disponiveis}
        Dificuldade de foco: {dificuldade_foco}
        """

        # Envia as informações para o Gemini através da Interactions API.
        resposta = cliente_gemini.interactions.create(
            # Modelo atual utilizado pelo agente.
            model="gemini-3.7-flash",

            # Envia as informações do usuário e explica a função do agente.
            input=f"""
            Você é o agente de estudos do Entretempos.

            Sua função é criar uma trilha de estudos personalizada
            para cada usuário.

            Considere:
            - objetivo;
            - nível de conhecimento;
            - tempo disponível;
            - dias disponíveis;
            - dificuldade de foco.

            Organize os conteúdos em uma ordem lógica,
            começando pelos conhecimentos necessários antes
            de avançar para assuntos mais complexos.

            A trilha deve ser realista para o tempo disponível
            e adequada ao nível do usuário.

            Informações do usuário:

            {informacoes_usuario}
            """,

            # Define que a IA deve retornar um JSON seguindo
            # exatamente a estrutura do modelo TrilhaEstudos.
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": TrilhaEstudos.model_json_schema()
            }
        )

        # Converte o JSON retornado pela IA para o modelo TrilhaEstudos.
        trilha = TrilhaEstudos.model_validate_json(
            resposta.output_text
        )

        # Envia a trilha criada para o TrilhaService salvar no banco.
        resultado = trilha_service.criar_trilha(
            fk_usuario,
            trilha
        )

        # Retorna o resultado do salvamento.
        return resultado


# Cria uma função simples para testar o agente.
def teste_agente():

    # Cria uma instância do nosso agente.
    agente = AgenteEstudosService()

    # Pede uma trilha de teste para a IA.
    trilha = agente.criar_trilha(
        fk_usuario=1,
        objetivo="Aprender Python do zero",
        nivel_conhecimento="Iniciante",
        tempo_diario=60,
        dias_disponiveis="segunda, quarta e sexta",
        dificuldade_foco="Tenho dificuldade para manter o foco por muito tempo"
    )

    # Mostra o resultado retornado pelo banco.
    print("\nRESULTADO:")

    # Mostra o ID da trilha criada.
    print(f"ID da trilha criada: {trilha}")


# Executa o teste somente quando este arquivo for executado diretamente.
if __name__ == "__main__":
    teste_agente()