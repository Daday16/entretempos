# Importa o FastAPI para criar nossa aplicação.
from fastapi import FastAPI

# Importa as rotas de usuários.
from routes.usuarios import router as usuarios_router

# Importa as rotas de perfis.
from routes.perfis import router as perfis_router

# Importa as rotas de tarefas.
from routes.tarefas import router as tarefas_router

# Importa as rotas de grupos.
from routes.grupos import router as grupos_router

# Importa as rotas de Pomodoro.
from routes.pomodoros import router as pomodoros_router

# Importa as rotas de recuperação de senha.
from routes.recuperacao import router as recuperacao_router


# Cria a aplicação principal do Entretempos.
app = FastAPI()


# Conecta as rotas de usuários à aplicação.
app.include_router(usuarios_router)

# Conecta as rotas de perfil à aplicação.
app.include_router(perfis_router)

# Conecta as rotas de tarefas à aplicação.
app.include_router(tarefas_router)

# Conecta as rotas de grupos à aplicação.
app.include_router(grupos_router)

# Conecta as rotas de Pomodoro à aplicação.
app.include_router(pomodoros_router)

# Conecta as rotas de recuperação de senha à aplicação.
app.include_router(recuperacao_router)


# Rota principal usada para testar se o backend está funcionando.
@app.get("/")
def inicio():
    # Retorna uma mensagem quando acessamos a página inicial.
    return {"mensagem": "Entretempos funcionando!"}