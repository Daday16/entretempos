
"""
Agente local de apoio do Pipo.
Não utiliza APIs externas nem armazena conversas.
"""
import random
import re


class AgenteApoioService:

    CATEGORIAS = {
        "ansiedade": [
            "ansioso", "ansiosa", "ansiedade", "nervoso",
            "nervosa", "preocupado", "preocupada",
            "aflito", "aflita"
        ],
        "desanimo": [
            "desanimado", "desanimada", "desmotivado",
            "desmotivada", "sem vontade", "incapaz",
            "fracassei", "fracasso"
        ],
        "frustracao": [
            "frustrado", "frustrada", "irritado",
            "irritada", "com raiva", "deu errado",
            "não deu certo", "falhei"
        ],
        "cansaco": [
            "cansado", "cansada", "exausto", "exausta",
            "esgotado", "esgotada", "sem energia",
            "sobrecarregado", "sobrecarregada"
        ],
        "solidao": [
            "sozinho", "sozinha", "solitário",
            "solitária", "ninguém me entende",
            "não tenho ninguém"
        ],
        "medo": [
            "medo de falhar", "medo de errar",
            "tenho medo", "receio", "inseguro",
            "insegura"
        ],
        "foco": [
            "procrastinando", "procrastinação",
            "não consigo focar", "sem foco",
            "distraído", "distraída",
            "não consigo começar"
        ],
        "felicidade": [
            "feliz", "consegui", "conquista",
            "orgulhoso", "orgulhosa", "animado",
            "animada", "empolgado", "empolgada"
        ],
        "confusao": [
            "confuso", "confusa", "não entendi",
            "perdido", "perdida",
            "não sei por onde começar"
        ]
    }

    RESPOSTAS = {
        "ansiedade": [
            "Parece que sua cabeça está tentando resolver muitas coisas ao mesmo tempo. Vamos com calma: você não precisa dar conta de tudo agora.",
            "Sinto muito que esse momento esteja tão agitado. Que tal fazer uma pausa, respirar devagar e escolher só o próximo passo?",
            "Quando a preocupação cresce, tudo pode parecer urgente. Vamos separar o que precisa ser resolvido hoje do que pode esperar?"
        ],

        "desanimo": [
            "Um momento difícil não apaga tudo o que você já construiu. Talvez hoje o passo possível seja bem pequeno, e tudo bem.",
            "Você não precisa estar motivado o tempo todo para continuar. Às vezes, descansar e recomeçar devagar já é bastante.",
            "Não transforme uma dificuldade em uma definição sobre quem você é. Vamos pensar em uma coisa pequena que esteja ao seu alcance?"
        ],

        "frustracao": [
            "É compreensível ficar frustrado quando algo não sai como você esperava. Quer me contar o que aconteceu para tentarmos olhar por outro ângulo?",
            "Errar ou precisar tentar de novo faz parte do processo. Vamos descobrir qual pedacinho pode ser ajustado, sem cobrança?",
            "Parece que isso mexeu com você. Antes de tentar resolver, talvez valha dar um minuto para essa frustração baixar."
        ],

        "cansaco": [
            "Seu descanso também faz parte do progresso. Talvez seu corpo esteja pedindo uma pausa, não mais cobrança.",
            "Quando a energia acaba, até tarefas simples pesam. Que tal escolher entre descansar um pouco ou fazer só uma etapa curtinha?",
            "Você não precisa transformar todo minuto em produtividade. Pausar também é cuidar do caminho."
        ],

        "solidao": [
            "Deve ser difícil sentir que está passando por isso sem companhia. Obrigado por dividir um pouco comigo. Existe alguém de confiança com quem você poderia conversar também?",
            "Você merece ser ouvido e acolhido. Posso te escutar nesta conversa, e também pode ajudar procurar alguém em quem confie.",
            "Sentir-se só pode pesar bastante. Quer me contar o que tem feito você se sentir assim?"
        ],

        "medo": [
            "Ter medo não significa que você não é capaz. Podemos diminuir o tamanho do desafio e pensar no primeiro passo mais seguro.",
            "Você não precisa ter certeza de tudo para começar. O que seria uma tentativa pequena, que não precise sair perfeita?",
            "Às vezes a possibilidade de errar parece maior do que realmente é. Vamos entender o que exatamente está te preocupando?"
        ],

        "foco": [
            "Começar costuma ser a parte mais difícil. Que tal combinar apenas cinco minutos com uma única tarefa, sem compromisso de terminar tudo?",
            "Vamos deixar o caminho mais simples: escolha uma tarefa, afaste uma distração e faça só o primeiro pedacinho.",
            "Talvez não seja falta de capacidade, mas excesso de coisas competindo pela sua atenção. O que mais está te distraindo agora?"
        ],

        "felicidade": [
            "Que notícia boa! 🌰✨ Reconheça essa conquista: você colocou esforço nisso e merece comemorar.",
            "O Pipo está comemorando com você! Cada avanço merece ser notado. O que foi a melhor parte dessa conquista?",
            "Que orgulho desse passinho! Guarde essa sensação para lembrar que seu esforço pode render frutos."
        ],

        "confusao": [
            "Tudo bem ainda não ter clareza. Vamos organizar juntos: qual é a parte que parece mais confusa neste momento?",
            "Quando tudo parece misturado, ajuda separar em partes menores. Qual é a primeira dúvida que você gostaria de resolver?",
            "Você não precisa entender tudo de uma vez. Me conte o que já conseguiu compreender e onde começou a dúvida."
        ],

        "acolhimento": [
            "Obrigado por compartilhar isso comigo. Não precisa encontrar as palavras perfeitas; podemos ir com calma.",
            "Estou aqui para te ouvir nesta conversa. O que está pesando mais para você neste momento?",
            "Faz sentido querer um pouco de acolhimento. Quer me contar um pouco mais sobre como foi seu dia?"
        ]
    }

    PERGUNTAS = {
        "ansiedade": "O que está deixando você mais preocupado(a) agora?",
        "desanimo": "Aconteceu alguma coisa hoje que trouxe esse sentimento?",
        "frustracao": "O que aconteceu? Podemos pensar juntos em uma alternativa.",
        "cansaco": "Você sente que precisa descansar ou tem algo específico te sobrecarregando?",
        "solidao": "Tem alguém de confiança com quem você gostaria de conversar sobre isso?",
        "medo": "Qual é a parte que mais dá medo neste desafio?",
        "foco": "Qual tarefa você gostaria de tentar começar por cinco minutos?",
        "felicidade": "Quer me contar como conseguiu essa conquista?",
        "confusao": "Qual é a primeira parte que você gostaria de organizar?"
    }

    SINAIS_DE_RISCO = [
        r"\b(quero|vou|penso em|pensando em) (me )?(matar|suicidar|suicidio|tirar minha vida)\b",
        r"\b(nao quero) mais viver\b",
        r"\b(me )?(machucar|ferir)\b",
        r"\b(acabar com|tirar) (a )?minha vida\b",
        r"\bseria melhor se eu nao existisse\b"
    ]

    def responder(self, mensagem: str, historico=None):

        texto = self._normalizar(mensagem)

        # Prioriza mensagens que indicam risco à segurança.
        if any(
            re.search(padrao, texto)
            for padrao in self.SINAIS_DE_RISCO
        ):
            return {
                "categoria": "seguranca",
                "resposta": (
                    "Sinto muito que você esteja passando por algo tão doloroso. "
                    "Obrigado por me contar. Sua segurança é importante e você "
                    "não precisa lidar com isso sozinho(a). Se houver risco imediato, "
                    "procure um serviço de emergência ou vá a uma UPA/pronto-socorro. "
                    "No Brasil, você também pode ligar para o CVV no 188, "
                    "gratuitamente, 24 horas. Se puder, aproxime-se agora de alguém "
                    "de confiança e conte como está se sentindo."
                ),
                "pergunta": (
                    "Você está em perigo imediato ou pensando em se machucar agora?"
                ),
                "prioridade_humana": True
            }

        categoria = self._identificar_categoria(texto)

        # Mantém o tema recente quando a resposta é curta.
        if categoria == "acolhimento" and historico:
            for item in reversed(historico[-6:]):
                anterior = item.get("categoria")

                if anterior in self.RESPOSTAS and anterior != "acolhimento":
                    categoria = anterior
                    break

        resposta = random.choice(self.RESPOSTAS[categoria])

        return {
            "categoria": categoria,
            "resposta": resposta,
            "pergunta": self.PERGUNTAS.get(
                categoria,
                "Quer me contar um pouco mais sobre o que está acontecendo?"
            ),
            "prioridade_humana": False
        }

    def _identificar_categoria(self, texto):

        for categoria, palavras in self.CATEGORIAS.items():

            if any(
                self._normalizar(palavra) in texto
                for palavra in palavras
            ):
                return categoria

        return "acolhimento"

    @staticmethod
    def _normalizar(texto):

        texto = str(texto or "").lower().strip()

        tabela = str.maketrans(
            "áàãâéêíóôõúç",
            "aaaaeeiooouc"
        )

        return texto.translate(tabela)
