# Entretempos — Front-end web

Interface responsiva baseada na referência enviada: tons de laranja, creme e pêssego, com Pipo como mascote. Inclui login/cadastro, Ninho do Foco, A Trilha (grupos e tarefas), Modo Foco, Loja do Pipo e perfil de estudos.

## Executar
1. Inicie o backend na raiz do projeto com o comando que já utiliza:
   `python -m uvicorn main:app --app-dir backend --reload`
2. Em outro terminal, entre nesta pasta `frontend` e execute:
   `python -m http.server 5500`
3. Abra `http://127.0.0.1:5500`.

A API padrão é `http://127.0.0.1:8000`. Para alterá-la, abra o console do navegador e execute `localStorage.setItem('entretempos_api','http://127.0.0.1:8000')`, depois recarregue a página.

## Limites que dependem do backend
- O backend atual não tem rota de conclusão de tarefa; a interface avisa isso em vez de fingir que salvou.
- A loja é uma demonstração visual. Compras, inventário e itens equipados exigem rotas/tabelas próprias.
- O backend não devolve um ID de usuário no login, então a integração Pomodoro tenta consultar o registro ativo para finalizar a sessão.
- A recuperação de senha depende de SMTP configurado no `.env`.
- Se o navegador bloquear requisições por CORS, adicione `CORSMiddleware` no `backend/main.py` com origem `http://127.0.0.1:5500` e `http://localhost:5500`.
