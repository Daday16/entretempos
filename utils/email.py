# Importa o módulo que permite acessar as configurações
# guardadas nas variáveis de ambiente.
import os

# Importa a biblioteca do próprio Python responsável
# por conversar com servidores de e-mail.
import smtplib

# Importa o formato usado para montar um e-mail.
from email.message import EmailMessage

# Importa a função que lê o arquivo .env.
from dotenv import load_dotenv


# Carrega as informações que estão dentro do arquivo .env.
load_dotenv()


# Pega o endereço de e-mail do Entretempos que está no .env.
SMTP_USER = os.getenv("SMTP_USER")

# Pega a senha de app do Google que está no .env.
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def enviar_codigo_email(email_destino, codigo):
    """
    Envia o código de recuperação de senha
    para o e-mail informado pelo usuário.
    """

    # Cria uma nova mensagem de e-mail.
    mensagem = EmailMessage()

    # Define quem está enviando o e-mail.
    mensagem["From"] = SMTP_USER

    # Define para qual endereço o e-mail será enviado.
    mensagem["To"] = email_destino

    # Define o assunto do e-mail.
    mensagem["Subject"] = "Código de recuperação de senha - Entretempos"

    # Define o conteúdo que aparecerá dentro do e-mail.
    mensagem.set_content(
        f"""
Olá!

Recebemos uma solicitação para recuperar a senha
da sua conta no Entretempos.

Seu código de recuperação é:

{codigo}

Esse código é válido por 10 minutos.

Se você não solicitou a recuperação de senha,
ignore este e-mail.

Equipe Entretempos
"""
    )

    # Abre uma conexão segura com o servidor do Gmail.
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:

        # Faz login no Gmail usando o e-mail e a senha de app.
        servidor.login(
            SMTP_USER,
            SMTP_PASSWORD
        )

        # Envia o e-mail.
        servidor.send_message(mensagem)