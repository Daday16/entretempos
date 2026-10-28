
import mysql.connector
import os
from database.config import NOME_BANCO


def conectar_banco():
    conexao = mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=3306,
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=NOME_BANCO
    )

    return conexao
