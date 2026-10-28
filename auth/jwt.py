# Importa o sistema operacional para acessar as configurações.
import os

from fastapi import Depends, HTTPException, status

# Importa funções para trabalhar com datas e horários.
from datetime import datetime, timedelta, timezone

# Importa funções para criar e verificar tokens JWT.
from jose import jwt

# Importa ferramentas do FastAPI para receber o token.
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Define que o sistema receberá um token de autenticação.
seguranca = HTTPBearer()


# Chave secreta usada para proteger os tokens.
# Em um projeto real, ela deve ficar protegida em uma variável de ambiente.
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "chave-temporaria-do-projeto")

# Define o algoritmo usado para criar o token.
ALGORITHM = "HS256"

# Define por quanto tempo o token será válido.
TEMPO_TOKEN_MINUTOS = 30


# Cria um token para identificar o usuário conectado.
def criar_token(id_usuario):

    # Define o momento em que o token irá expirar.
    expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=TEMPO_TOKEN_MINUTOS
    )

    # Guarda o ID do usuário e o prazo de validade dentro do token.
    dados = {
        "sub": str(id_usuario),
        "exp": expiracao
    }

    # Cria o token usando os dados e a chave secreta.
    token = jwt.encode(
        dados,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    # Retorna o token criado.
    return token

# Verifica se um token é válido e retorna os dados dele.

def verificar_token(token):
    try:
        dados = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        print("JWT válido:", dados)
        return dados

    except Exception as erro:
        print("ERRO REAL DO JWT:", repr(erro))
        return None

# Cria uma função que identifica o usuário pelo token.

def obter_usuario_token(
    credenciais: HTTPAuthorizationCredentials = Depends(seguranca)
):
    token = credenciais.credentials
    dados = verificar_token(token)

    if dados is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado."
        )

    try:
        return int(dados["sub"])
    except (KeyError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não contém um ID de usuário válido."
        )


    # Pega o token enviado pelo usuário.
    token = credenciais.credentials

    # Verifica se o token é válido.
    dados = verificar_token(token)

    # Se o token for inválido, informa que não há usuário autenticado.
    if dados is None:
        return None

    # Retorna o ID do usuário encontrado no token.
    return int(dados["sub"])