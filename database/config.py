
import os
from pathlib import Path
from dotenv import load_dotenv

# Localiza o .env na raiz do projeto.
RAIZ_PROJETO = Path(__file__).resolve().parents[2]
ARQUIVO_ENV = RAIZ_PROJETO / ".env"

load_dotenv(ARQUIVO_ENV, override=True)

NOME_BANCO = os.getenv("DB_NAME")
