
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# Importa a rota do agente de apoio.
from routes.apoio import router as apoio_router


# Cria a aplicação principal do Entretempos.
app = FastAPI(
    title="Entretempos",
    description="API do Ninho do Foco",
    version="1.0.0"
)


# Configuração CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://entretempos-ivory.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Conecta todas as rotas à aplicação.
app.include_router(usuarios_router)
app.include_router(perfis_router)
app.include_router(tarefas_router)
app.include_router(grupos_router)
app.include_router(pomodoros_router)
app.include_router(recuperacao_router)
app.include_router(apoio_router)


# Rota principal para testar o funcionamento.
@app.get("/")
def inicio():
    return {"mensagem": "Entretempos funcionando!"}

