
import random
import re
import unicodedata


class AgenteApoioService:

    CATEGORIAS = {
        "ansiedade": [
            "ansioso", "ansiosa", "ansiedade", "nervoso",
            "nervosa", "preocupado", "preocupada",
            "aflito", "aflita", "preocupacao", "agoniado"
        ],
        "desanimo": [
            "desanimado", "desanimada", "desmotivado",
            "desmotivada", "sem vontade", "incapaz",
            "fracassei", "fracasso", "sem motivacao"
        ],
        "frustracao": [
            "frustrado", "frustrada", "irritado",
            "irritada", "com raiva", "deu errado",
            "nao deu certo", "falhei"
        ],
        "cansaco": [
            "cansado", "cansada", "exausto", "exausta",
            "esgotado", "esgotada", "sem energia",
            "sobrecarregado", "sobrecarregada"
        ],
        "solidao": [
            "sozinho", "sozinha", "solitario",
            "solitaria", "ninguem me entende",
            "nao tenho ninguem"
        ],
        "medo": [
            "medo de falhar", "medo de errar",
            "tenho medo", "receio", "inseguro",
            "insegura"
        ],
        "foco": [
            "procrastinando", "procrastinacao",
            "nao consigo focar", "sem foco",
            "distraido", "distraida", "nao consigo comecar",
            "nao consigo terminar"
        ],
        "felicidade": [
            "feliz", "consegui", "conquista",
            "orgulhoso", "orgulhosa", "animado",
            "animada", "empolgado", "empolgada"
        ],
        "confusao": [
            "confuso", "confusa", "nao entendi",
            "perdido", "perdida",
            "nao sei por onde comecar"
        ],
        "sobrecarga": [
            "muita coisa", "muitas coisas",
            "coisas demais", "nao dou conta",
            "tudo acumulado", "tarefas acumuladas",
            "estou sobrecarregado", "estou sobrecarregada"
        ]
    }

    RESPOSTAS = {
        "ansiedade": [
            "Parece que sua cabeca esta tentando resolver muitas coisas ao mesmo tempo. Vamos por partes.",
            "Quando tudo parece urgente, fica dificil pensar. Vamos identificar o que realmente precisa de atencao agora.",
            "Respire um pouco. Voce nao precisa resolver tudo de uma vez. Vamos pensar apenas no proximo passo."
        ],
        "desanimo": [
            "Um dia dificil nao apaga tudo o que voce ja conquistou. Que tal comecar com algo bem pequeno?",
            "Voce nao precisa estar motivado o tempo todo. Um pequeno passo ja pode ajudar a retomar o ritmo.",
            "Nao transforme uma dificuldade em uma definicao sobre voce. Vamos tentar de outro jeito?"
        ],
        "frustracao": [
            "Entendo que isso tenha sido frustrante. Vamos descobrir o que pode ser ajustado para tentar novamente.",
            "Nem sempre as coisas saem como planejamos. O importante agora e entender o que aconteceu.",
            "Tudo bem precisar tentar de novo. Qual parte voce gostaria de resolver primeiro?"
        ],
        "cansaco": [
            "Seu descanso tambem faz parte do progresso. Talvez seja hora de fazer uma pausa.",
            "Quando a energia acaba, ate tarefas simples pesam. Vamos diminuir o ritmo?",
            "Voce nao precisa transformar todo minuto em produtividade. Pausar tambem e importante."
        ],
        "solidao": [
            "Deve ser dificil sentir que esta passando por isso sem companhia. Quer me contar um pouco mais?",
            "Voce merece ser ouvido e acolhido. Existe alguem de confianca com quem possa conversar?",
            "Obrigado por dividir isso comigo. Podemos conversar com calma, sem pressa."
        ],
        "medo": [
            "Ter medo nao significa que voce nao e capaz. Podemos dividir esse desafio em etapas menores.",
            "Voce nao precisa ter certeza de tudo para comecar. Qual seria um primeiro passo seguro?",
            "Vamos entender o que esta causando esse receio e pensar em uma forma de lidar com isso."
        ],
        "foco": [
            "Vamos facilitar: escolha uma tarefa e dedique apenas cinco minutos a ela.",
            "Tente afastar uma distracao e comece pela menor parte da atividade. Nao precisa terminar tudo agora.",
            "Comecar pode ser a parte mais dificil. Qual tarefa podemos dividir em pequenas etapas?"
        ],
        "felicidade": [
            "Que noticia boa! Cada conquista merece ser reconhecida. Parabens pelo seu esforco!",
            "O Pipo esta comemorando com voce! O que foi mais especial nessa conquista?",
            "Que orgulho desse avancao! Valorize cada passo que voce conseguiu dar."
        ],
        "confusao": [
            "Tudo bem ainda nao ter clareza. Vamos organizar as ideias uma de cada vez.",
            "Quando tudo parece misturado, ajuda separar em partes menores. O que precisa ser resolvido primeiro?",
            "Voce nao precisa entender tudo de uma vez. Vamos comecar pela sua principal duvida."
        ],
        "sobrecarga": [
            "Parece que tem coisa demais acontecendo ao mesmo tempo. Vamos listar tudo e escolher apenas uma prioridade?",
            "Quando muitas tarefas se acumulam, fica dificil saber por onde comecar. Vamos separar o urgente do que pode esperar?",
            "Nao precisamos resolver tudo agora. Escolha uma tarefa pequena e vamos avancar passo a passo."
        ],
        "acolhimento": [
            "Estou aqui para te ouvir. O que esta pesando mais neste momento?",
            "Obrigado por compartilhar isso comigo. Podemos conversar com calma.",
            "Vamos por partes. Me conte um pouco mais sobre o que esta acontecendo."
        ]
    }

    PERGUNTAS = {
        "ansiedade": "O que esta deixando voce mais preocupado agora?",
        "desanimo": "Qual seria uma pequena coisa que voce conseguiria fazer hoje?",
        "frustracao": "O que aconteceu? Podemos pensar juntos em uma alternativa.",
        "cansaco": "Voce sente que precisa descansar ou tem algo especifico te sobrecarregando?",
        "solidao": "Tem alguem de confianca com quem voce gostaria de conversar?",
        "medo": "Qual e a parte que mais da medo nesse desafio?",
        "foco": "Qual tarefa voce gostaria de tentar comecar por cinco minutos?",
        "felicidade": "Quer me contar como conseguiu essa conquista?",
        "confusao": "Qual e a primeira coisa que precisamos organizar?",
        "sobrecarga": "Quais tarefas estao acumuladas? Podemos definir uma prioridade juntos."
    }

    SINAIS_DE_RISCO = [
        r"\b(quero|vou|penso em|pensando em) (me )?(matar|suicidar|suicidio|tirar minha vida)\b",
        r"\b(quero|vou|penso em|pensando em) morrer\b",
        r"\bnao quero mais viver\b",
        r"\b(me )?(machucar|ferir)\b",
        r"\b(acabar com|tirar) (a )?minha vida\b",
        r"\bseria melhor se eu nao existisse\b"
    ]

    def responder(self, mensagem: str, historico=None):

        texto = self._normalizar(mensagem)
        historico = historico if isinstance(historico, list) else []

        # Identifica mensagens que indicam risco a seguranca.
        if any(
            re.search(padrao, texto)
            for padrao in self.SINAIS_DE_RISCO
        ):
            return {
                "categoria": "seguranca",
                "resposta": (
                    "Sinto muito que voce esteja passando por algo tao doloroso. "
                    "Obrigado por me contar. Sua seguranca e importante e voce "
                    "nao precisa lidar com isso sozinho(a). Se houver risco imediato, "
                    "procure um servico de emergencia ou va a uma UPA/pronto-socorro. "
                    "No Brasil, voce tambem pode ligar para o CVV no 188, "
                    "gratuitamente, 24 horas. Se puder, aproxime-se agora de alguem "
                    "de confianca e conte como esta se sentindo."
                ),
                "pergunta": (
                    "Voce esta em perigo imediato ou pensando em se machucar agora?"
                ),
                "prioridade_humana": True
            }

        categoria = self._identificar_categoria(texto)

        # Aproveita o contexto em respostas curtas.
        if categoria == "acolhimento" and len(texto.split()) <= 5:
            for item in reversed(historico[-6:]):
                anterior = item.get("categoria")

                if anterior in self.RESPOSTAS and anterior != "acolhimento":
                    categoria = anterior
                    break

        respostas = self.RESPOSTAS[categoria]

        # Evita repetir as respostas mais recentes.
        respostas_recentes = [
            item.get("resposta")
            for item in historico[-3:]
            if isinstance(item, dict)
        ]

        alternativas = [
            resposta for resposta in respostas
            if resposta not in respostas_recentes
        ]

        resposta = random.choice(alternativas or respostas)

        return {
            "categoria": categoria,
            "resposta": resposta,
            "pergunta": self.PERGUNTAS.get(
                categoria,
                "Quer me contar um pouco mais sobre o que esta acontecendo?"
            ),
            "prioridade_humana": False
        }

    def _identificar_categoria(self, texto):

        for categoria, palavras in self.CATEGORIAS.items():
            for palavra in palavras:
                palavra = self._normalizar(palavra)

                if re.search(
                    r"\b" + re.escape(palavra) + r"\b",
                    texto
                ):
                    return categoria

        return "acolhimento"

    @staticmethod
    def _normalizar(texto):

        texto = str(texto or "").lower().strip()

        texto = unicodedata.normalize("NFD", texto)

        texto = "".join(
            caractere for caractere in texto
            if unicodedata.category(caractere) != "Mn"
        )

        return texto
