import os
import psycopg2
from psycopg2.extras import RealDictCursor

from database.config import NOME_BANCO


def conectar_banco():
    conexao = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME", NOME_BANCO),
        sslmode="require"
    )

    return conexao

