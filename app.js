
const API_BASE = 'https://entretempos.onrender.com';

const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];

const state = {
    token: localStorage.getItem('entretempos_token'),
    name: localStorage.getItem('entretempos_name') || 'Estudante',
    groups: [],
    tasks: [],
    group: '',
    coins: 0,
    timer: null,
    seconds: 1500,
    total: 1500,
    minutes: 25,
    running: false,
    profileExists: false,

    // Conversa local com o Pipo
    pipoHistory: [],
    pipoSending: false
};

let toastTimer;

function toast(msg, error = false) {
    const el = $('#toast');
    if (!el) return;

    el.textContent = msg;
    el.style.background = error ? '#9b3e32' : '#33271f';

    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.textContent = '', 4200);
}

function esc(v) {
    return String(v ?? '').replace(/[&<>"']/g, c => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    }[c]));
}

function qs(data) {
    const p = new URLSearchParams();

    Object.entries(data || {}).forEach(([k, v]) => {
        if (v !== undefined && v !== null && v !== '') {
            p.set(k, v);
        }
    });

    return p.toString();
}

async function api(path, {
    method = 'GET',
    data = {},
    auth = true
} = {}) {
    let url = API_BASE + path;
    const query = qs(data);

    if (query) url += '?' + query;

    let res;

    try {
        res = await fetch(url, {
            method,
            headers: auth && state.token
                ? { Authorization: 'Bearer ' + state.token }
                : {}
        });
    } catch {
        throw Error(
            'Não consegui conectar à API. Confira se o FastAPI está rodando em ' +
            API_BASE + '.'
        );
    }

    let body;

    try {
        body = await res.json();
    } catch {
        body = {};
    }

    if (!res.ok) {
        throw Error(
            body.detail ||
            body.mensagem ||
            `Erro HTTP ${res.status}`
        );
    }

    if (
        body?.mensagem &&
        /(incorret|inválid|não encontrado|não foi|não pode|precisa|obrigat|expirad|já existe|sem permissão)/i.test(body.mensagem)
    ) {
        throw Error(body.mensagem);
    }

    return body;
}

// ==========================================
// AUTENTICAÇÃO E NAVEGAÇÃO
// ==========================================

function showAuth(tab = 'login') {
    $('#auth').classList.remove('hidden');
    $('#app').classList.add('hidden');

    $('#login').classList.toggle('hidden', tab !== 'login');
    $('#register').classList.toggle('hidden', tab !== 'register');

    $$('[data-tab]').forEach(b =>
        b.classList.toggle('selected', b.dataset.tab === tab)
    );
}

function enterApp() {
    $('#auth').classList.add('hidden');
    $('#app').classList.remove('hidden');

    $('#username').textContent = state.name;
    $('#helloName').textContent =
        state.name.split(' ')[0] || 'exploradora';

    $('#avatar').textContent =
        (state.name[0] || 'P').toUpperCase();

    $('#today').textContent = new Date().toLocaleDateString(
        'pt-BR',
        {
            weekday: 'long',
            day: 'numeric',
            month: 'long'
        }
    );

    navigate('home');
    refresh();
}

function logout() {
    state.token = null;

    localStorage.removeItem('entretempos_token');
    localStorage.removeItem('entretempos_name');

    showAuth();
}

function navigate(page) {
    $$('.page').forEach(p => p.classList.add('hidden'));

    $('#page-' + page)?.classList.remove('hidden');

    $$('[data-page]').forEach(b =>
        b.classList.toggle('active', b.dataset.page === page)
    );

    const heads = {
        home: 'Bem-vinda ao seu ninho! ✦',
        trilha: 'Vamos desenhar sua trilha ✦',
        focus: 'Seu momento de foco ✦',
        shop: 'Recompensas do Pipo ✦',
        profile: 'Seu perfil de estudos ✦'
    };

    $('#heading').textContent = heads[page] || 'Entretempos';

    if (page === 'trilha') renderTasks();
    if (page === 'profile') loadProfile();
}

// ==========================================
// GRUPOS E TAREFAS
// ==========================================

async function refresh() {
    await Promise.allSettled([
        loadGroups(),
        loadCoins()
    ]);

    await loadTasks();
    renderHome();
}

async function loadGroups() {
    try {
        const d = await api('/grupos/');

        state.groups = Array.isArray(d) ? d : [];

        const s = $('#groupSelect');
        const old = state.group || s.value;

        s.innerHTML =
            '<option value="">Selecione um grupo</option>' +
            state.groups.map(g =>
                `<option value="${g.id_grupo}">
          ${esc(g.titulo || 'Grupo ' + g.id_grupo)}
        </option>`
            ).join('');

        if (
            old &&
            state.groups.some(g => String(g.id_grupo) === String(old))
        ) {
            state.group = String(old);
        } else {
            state.group = state.groups.length
                ? String(state.groups[0].id_grupo)
                : '';
        }

        s.value = state.group;

    } catch (e) {
        toast(e.message, true);
    }
}

async function loadTasks() {
    if (!state.group) {
        state.tasks = [];
        renderTasks();
        renderHome();
        return;
    }

    try {
        const d = await api(
            '/tarefas/grupo/' + encodeURIComponent(state.group)
        );

        state.tasks = Array.isArray(d) ? d : [];

        renderTasks();
        renderHome();

    } catch (e) {
        state.tasks = [];

        renderTasks();
        renderHome();

        toast(e.message, true);
    }
}

async function loadCoins() {
    try {
        const d = await api('/pomodoros/moedas');

        state.coins = Number(
            typeof d === 'number'
                ? d
                : (
                    d.moedas ??
                    d.saldo ??
                    d.total_moedas ??
                    0
                )
        );

        $('#coins').innerHTML =
            `${state.coins} <small>nozes</small>`;

        $('#shopCoins').textContent = state.coins;

    } catch {
        // Não interrompe o carregamento da aplicação.
    }
}

function dateLabel(t) {
    if (!t.dthr_prazo) return 'Sem prazo';

    const d = new Date(t.dthr_prazo);

    return isNaN(d.getTime())
        ? 'Prazo: ' + t.dthr_prazo
        : 'Prazo: ' + d.toLocaleDateString(
            'pt-BR',
            {
                day: '2-digit',
                month: 'short'
            }
        );
}

function taskHTML(t) {
    const done = Boolean(
        t.concluida ||
        t.concluido ||
        t.status === 'concluida' ||
        t.status === 'concluído'
    );

    return `
    <article class="task ${done ? 'completed' : ''}">
      <button
        class="check ${done ? 'done' : ''}"
        data-act="complete"
        data-id="${t.id_tarefa}"
        aria-label="Concluir tarefa"
      >
        ${done ? '✓' : ''}
      </button>

      <div class="task-text">
        <strong>${esc(t.titulo || 'Tarefa sem título')}</strong>

        <small>
          ${esc(dateLabel(t))}
          ${t.descricao ? ' · ' + esc(t.descricao) : ''}
        </small>
      </div>

      <div class="task-actions">
        <button
          data-act="edit"
          data-id="${t.id_tarefa}"
          title="Editar"
        >✎</button>

        <button
          data-act="delete"
          data-id="${t.id_tarefa}"
          title="Excluir"
        >×</button>
      </div>
    </article>
  `;
}

function renderTasks() {
    const el = $('#taskList');
    if (!el) return;

    el.innerHTML = !state.group
        ? '<div class="empty">Crie um grupo para desenhar sua trilha.</div>'
        : state.tasks.length
            ? state.tasks.map(taskHTML).join('')
            : '<div class="empty">Essa trilha ainda está começando. Adicione sua primeira tarefa! 🌱</div>';

    $('#taskCount').textContent =
        `${state.tasks.length} tarefa(s)`;

    $('#taskTotal').textContent = state.tasks.length;
}

function renderHome() {
    const el = $('#homeTasks');
    if (!el) return;

    el.innerHTML = state.tasks.length
        ? state.tasks.slice(0, 4).map(taskHTML).join('')
        : '<div class="empty">Suas tarefas vão aparecer aqui. Crie um grupo e dê o primeiro passo!</div>';

    $('#taskTotal').textContent = state.tasks.length;
}

// ==========================================
// MODAIS
// ==========================================

function modal(title, desc, html, submit) {
    $('#modalTitle').textContent = title;
    $('#modalDesc').textContent = desc;
    $('#modalForm').innerHTML = html;

    $('#modal').classList.remove('hidden');

    $('#modalForm').onsubmit = async e => {
        e.preventDefault();

        const d = Object.fromEntries(
            new FormData(e.currentTarget).entries()
        );

        try {
            await submit(d);
            $('#modal').classList.add('hidden');
        } catch (err) {
            toast(err.message, true);
        }
    };
}

$('#closeModal').onclick = () =>
    $('#modal').classList.add('hidden');

$('#modal').addEventListener('click', e => {
    if (e.target.id === 'modal') {
        $('#modal').classList.add('hidden');
    }
});

// ==========================================
// CRIAR GRUPOS
// ==========================================

function createGroup() {
    modal(
        'Criar uma trilha',
        'Separe tarefas por matéria, projeto ou objetivo.',

        `
      <label>
        Nome do grupo

        <input
          name="titulo"
          maxlength="80"
          placeholder="Ex.: Estudos de programação"
          required
        >
      </label>

      <button class="primary">
        Criar grupo →
      </button>
    `,

        async d => {
            const r = await api('/grupos/', {
                method: 'POST',
                data: d
            });

            toast(r.mensagem || 'Grupo criado!');

            await loadGroups();

            $('#groupSelect').value = state.group;

            await loadTasks();
        }
    );
}

// ==========================================
// CRIAR E EDITAR TAREFAS
// ==========================================

function createTask(task = null) {
    if (!state.groups.length) {
        toast('Primeiro, crie um grupo para sua trilha.');
        createGroup();
        return;
    }

    const edit = !!task;

    const html = `
    <label>
      Título

      <input
        name="titulo"
        maxlength="150"
        value="${esc(task?.titulo || '')}"
        placeholder="Ex.: Ler capítulo 2"
        required
      >
    </label>

    <label>
      Descrição

      <textarea
        name="descricao"
        rows="3"
        placeholder="Detalhes opcionais"
      >${esc(task?.descricao || '')}</textarea>
    </label>

    <label>
      Prazo (opcional)

      <input
        type="datetime-local"
        name="dthr_prazo"
        value="${esc(
        task?.dthr_prazo
            ? String(task.dthr_prazo).replace(' ', 'T').slice(0, 16)
            : ''
    )}"
      >
    </label>

    ${edit
            ? ''
            : `
          <label>
            Grupo

            <select name="fk_grupo" required>
              ${state.groups.map(g => `
                  <option
                    value="${g.id_grupo}"
                    ${String(g.id_grupo) === state.group
                    ? 'selected'
                    : ''
                }
                  >
                    ${esc(g.titulo || 'Grupo ' + g.id_grupo)}
                  </option>
                `).join('')
            }
            </select>
          </label>
        `
        }

    <button class="primary">
      ${edit ? 'Salvar alterações' : 'Adicionar à trilha'} →
    </button>
  `;

    modal(
        edit ? 'Editar tarefa' : 'Nova tarefa',

        edit
            ? 'Ajuste os detalhes do seu próximo passo.'
            : 'Pequenos passos também contam.',

        html,

        async d => {
            const data = {
                titulo: d.titulo,
                descricao: d.descricao || ''
            };

            if (edit) {
                await api('/tarefas/' + task.id_tarefa, {
                    method: 'PUT',
                    data
                });

            } else {
                data.fk_grupo = d.fk_grupo;
                data.frequencia = 0;

                data.dthr_prazo = d.dthr_prazo
                    ? d.dthr_prazo.replace('T', ' ')
                    : '';

                state.group = String(d.fk_grupo);

                $('#groupSelect').value = state.group;

                await api('/tarefas/', {
                    method: 'POST',
                    data
                });
            }

            toast(
                edit
                    ? 'Tarefa atualizada!'
                    : 'Tarefa adicionada à trilha!'
            );

            await loadTasks();
        }
    );
}

async function taskAction(e) {
    const b = e.target.closest('[data-act]');
    if (!b) return;

    const id = Number(b.dataset.id);
    const t = state.tasks.find(x => Number(x.id_tarefa) === id);

    if (b.dataset.act === 'edit' && t) {
        createTask(t);
        return;
    }

    if (b.dataset.act === 'complete') {
        try {
            b.disabled = true;

            const r = await api(`/tarefas/concluir/${id}`, {
                method: 'PUT'
            });

            toast(r.mensagem || 'Tarefa concluída!');
            await loadTasks();
            await loadCoins();

        } catch (err) {
            toast(err.message || 'Não foi possível concluir a tarefa.', true);
        } finally {
            b.disabled = false;
        }

        return;
    }

    if (b.dataset.act === 'delete' && confirm('Deseja excluir esta tarefa?')) {
        try {
            const r = await api('/tarefas/' + id, {
                method: 'DELETE'
            });

            toast(r.mensagem || 'Tarefa excluída');
            await loadTasks();

        } catch (err) {
            toast(err.message, true);
        }
    }
}

async function loadProfile() {
    const f = $('#profileForm');
    if (!f) return;

    try {
        const p = await api('/perfis/');

        if (!p || p.mensagem === 'Perfil não encontrado.') {
            state.profileExists = false;
            return;
        }

        state.profileExists = true;
        for (const k of [
            'objetivo',
            'nivel_conhecimento',
            'tempo_diario',
            'dificuldade_foco'
        ]) {
            if (f.elements[k] && p[k] != null) {
                f.elements[k].value = p[k];
            }
        }

        if (p.dias_disponiveis) {
            const days = String(p.dias_disponiveis)
                .split(/[,;|]/)
                .map(s => s.trim());

            $$('.days input').forEach(c => {
                c.checked = days.includes(c.value);
            });
        }

    } catch (e) {
        toast(e.message, true);
    }
}

$('#profileForm').addEventListener('submit', async e => {
    e.preventDefault();

    const f = e.currentTarget;

    const d = Object.fromEntries(
        new FormData(f).entries()
    );

    d.dias_disponiveis = $$('.days input:checked')
        .map(c => c.value)
        .join(',');

    if (!d.dias_disponiveis) {
        toast('Escolha pelo menos um dia para estudar.', true);
        return;
    }

    try {
        const r = await api('/perfis/', {
            method: state.profileExists ? 'PUT' : 'POST',
            data: d
        });

        state.profileExists = true;

        toast(r.mensagem || 'Perfil salvo!');

    } catch (err) {
        toast(err.message, true);
    }
});

// ==========================================
// LOJA DO PIPO
// ==========================================

function shop() {
    const items = [
        ['🧥', 'Moletom do Pipo', 'Roupinhas', 120],
        ['🧢', 'Boné aventureiro', 'Chapéus', 120],
        ['👓', 'Óculos redondinhos', 'Acessórios', 50],
        ['🎒', 'Mochila de aventura', 'Acessórios', 150],
        ['🧣', 'Cachecol quentinho', 'Roupinhas', 90],
        ['🌼', 'Tiara de flores', 'Acessórios', 75],
        ['🎩', 'Chapéu de explorador', 'Chapéus', 130],
        ['⭐', 'Broche de estrela', 'Acessórios', 60]
    ];

    $('#shopGrid').innerHTML = items.map((it, i) => `
    <article class="shop-item">
      <div class="item-art">${it[0]}</div>
      <h3>${it[1]}</h3>
      <p>${it[2]}</p>
      <p>🌰 ${it[3]} nozes</p>

      <button class="primary" data-shop="${i}">
        Ver item
      </button>
    </article>
  `).join('');
}

$('#shopGrid').addEventListener('click', e => {
    const b = e.target.closest('[data-shop]');

    if (b) {
        toast(
            'A loja do Pipo ainda é visual: o backend precisa de rotas de compra e inventário para desbloquear itens.',
            true
        );
    }
});

// ==========================================
// POMODORO
// ==========================================

function formatTime(n) {
    return (
        `${String(Math.floor(n / 60)).padStart(2, '0')}:` +
        `${String(n % 60).padStart(2, '0')}`
    );
}

function setTimer(m) {
    state.minutes = m;
    state.seconds = m * 60;
    state.total = state.seconds;
    state.running = false;

    clearInterval(state.timer);
    state.timer = null;

    $('#timer').textContent = formatTime(state.seconds);

    $('#modeLabel').textContent =
        m === 5 ? 'TEMPO DE PAUSA' : 'TEMPO DE FOCO';

    $('#timerStatus').textContent =
        'O Pipo está aqui com você.';

    $('#startTimer').textContent = 'Começar foco';

    $$('.presets button').forEach(b => {
        b.classList.toggle(
            'chosen',
            Number(b.dataset.min) === m
        );
    });
}

async function finishTimer() {
    clearInterval(state.timer);

    state.timer = null;
    state.running = false;

    $('#startTimer').textContent = 'Começar novamente';

    $('#timerStatus').textContent =
        'Sessão concluída. Muito bem! ✨';

    toast('Você reservou um tempo para si. Parabéns!');

    if (state.minutes !== 5) {
        try {
            const d = await api('/pomodoros/ativo');

            if (d.id_pomodoro) {
                await api(
                    '/pomodoros/finalizar/' + d.id_pomodoro,
                    { method: 'PUT' }
                );
            }

        } catch {
            // A sessão visual termina mesmo se a API falhar.
        }

        await loadCoins();
    }
}

async function toggleTimer() {
    if (state.running) {
        state.running = false;

        clearInterval(state.timer);
        state.timer = null;

        $('#startTimer').textContent = 'Continuar';

        $('#timerStatus').textContent =
            'Pausa. Continue quando quiser.';

        return;
    }

    if (state.seconds <= 0) {
        setTimer(state.minutes);
    }

    if (state.minutes !== 5) {
        try {
            const d = await api('/pomodoros/iniciar', {
                method: 'POST',
                data: { duracao: state.minutes }
            });

            if (d.mensagem?.includes('andamento')) {
                const active = await api('/pomodoros/ativo');

                if (!active.id_pomodoro) {
                    throw Error(d.mensagem);
                }
            }

        } catch (e) {
            toast(e.message, true);
            return;
        }
    }

    state.running = true;

    $('#startTimer').textContent = 'Pausar';

    $('#timerStatus').textContent =
        'Um minuto de cada vez.';

    state.timer = setInterval(() => {
        state.seconds--;

        $('#timer').textContent =
            formatTime(Math.max(0, state.seconds));

        if (state.seconds <= 0) {
            finishTimer();
        }
    }, 1000);
}

// ==========================================
// CHAT DE ACOLHIMENTO DO PIPO
// ==========================================

function renderPipoMessage(text, type = 'bot') {
    const box = $('#pipoChatMessages');

    if (!box) return;

    const message = document.createElement('div');

    message.className = `pipo-message ${type}`;
    message.textContent = text;

    box.appendChild(message);
    box.scrollTop = box.scrollHeight;
}

async function sendPipoMessage(text) {
    if (state.pipoSending) return;

    state.pipoSending = true;

    renderPipoMessage(text, 'user');

    const historico = state.pipoHistory.slice(-8);

    const params = {
        mensagem: text,
        historico: JSON.stringify(historico)
    };

    try {
        const resposta = await api('/apoio/mensagem', {
            method: 'POST',
            data: params
        });

        renderPipoMessage(
            resposta.resposta || 'Estou aqui para te ouvir.'
        );

        if (resposta.pergunta) {
            renderPipoMessage(resposta.pergunta);
        }

        state.pipoHistory.push({
            mensagem: text,
            categoria: resposta.categoria,
            resposta: resposta.resposta
        });

        state.pipoHistory = state.pipoHistory.slice(-8);

        if (resposta.prioridade_humana) {
            renderPipoMessage(
                'Você não precisa passar por isso sozinho(a). Procure alguém de confiança ou um serviço de apoio humano. Se houver perigo imediato, procure um serviço de emergência.'
            );
        }

    } catch (error) {
        renderPipoMessage(
            'Não consegui responder agora. Tente novamente em instantes.'
        );

        toast(error.message, true);

    } finally {
        state.pipoSending = false;

        const input = $('#pipoChatInput');
        const button = $('#pipoChatForm button');

        if (input) {
            input.disabled = false;
            input.focus();
        }

        if (button) {
            button.disabled = false;
        }
    }
}

function setupPipoChat() {
    const form = $('#pipoChatForm');

    if (!form || form.dataset.initialized === 'true') {
        return;
    }

    form.dataset.initialized = 'true';

    form.addEventListener('submit', event => {
        event.preventDefault();

        const input = $('#pipoChatInput');

        if (!input) return;

        const texto = input.value.trim();

        if (!texto || state.pipoSending) return;

        input.value = '';
        input.disabled = true;

        const button = $('#pipoChatForm button');

        if (button) {
            button.disabled = true;
        }

        sendPipoMessage(texto);
    });
}

// ==========================================
// LOGIN
// ==========================================

$('#loginForm').addEventListener('submit', async e => {
    e.preventDefault();

    const d = Object.fromEntries(
        new FormData(e.currentTarget).entries()
    );

    try {
        const r = await api('/usuarios/login', {
            method: 'POST',
            data: d,
            auth: false
        });

        if (!r.token) {
            throw Error(
                r.mensagem || 'Confira seu e-mail e senha.'
            );
        }

        state.token = r.token;
        state.name = r.usuario || 'Estudante';

        localStorage.setItem(
            'entretempos_token',
            state.token
        );

        localStorage.setItem(
            'entretempos_name',
            state.name
        );

        enterApp();

        toast('Que bom ter você de volta!');

    } catch (err) {
        toast(err.message, true);
    }
});

// ==========================================
// CADASTRO
// ==========================================

$('#registerForm').addEventListener('submit', async e => {
    e.preventDefault();

    const d = Object.fromEntries(
        new FormData(e.currentTarget).entries()
    );

    d.data_nascimento = d.data_nascimento.replaceAll('-', '');

    try {
        const r = await api('/usuarios/cadastro', {
            method: 'POST',
            data: d,
            auth: false
        });

        if (!/cadastrado com sucesso/i.test(r.mensagem || '')) {
            throw Error(
                r.mensagem || 'Não foi possível criar a conta.'
            );
        }

        toast(
            'Conta criada! Agora entre com seu e-mail e senha.'
        );

        showAuth('login');

        $('#loginForm [name=email]').value = d.email;

    } catch (err) {
        toast(err.message, true);
    }
});

// ==========================================
// RECUPERAÇÃO DE SENHA
// ==========================================

$$('[data-tab]').forEach(b => {
    b.onclick = () => showAuth(b.dataset.tab);
});

$('#forgot').onclick = () => {
    modal(
        'Recuperar senha',
        'Informe o e-mail cadastrado para solicitar as instruções.',

        `
      <label>
        E-mail

        <input
          type="email"
          name="email"
          required
          placeholder="voce@email.com"
        >
      </label>

      <button class="primary">
        Solicitar recuperação →
      </button>
    `,

        async d => {
            const r = await api('/recuperacao/solicitar', {
                method: 'POST',
                data: d,
                auth: false
            });

            toast(
                r.mensagem || 'Confira sua caixa de entrada'
            );
        }
    );
};

// ==========================================
// EVENTOS GERAIS
// ==========================================

$('#logout').onclick = logout;

$$('[data-page]').forEach(b => {
    b.onclick = () => navigate(b.dataset.page);
});

$$('[data-go]').forEach(b => {
    b.onclick = () => navigate(b.dataset.go);
});

$('#newGroup').onclick = createGroup;

$('#newTask').onclick = () => createTask();

$('#groupSelect').onchange = e => {
    state.group = e.target.value;
    loadTasks();
};

$('#taskList').addEventListener('click', taskAction);

$('#homeTasks').addEventListener('click', taskAction);

$$('.presets button').forEach(b => {
    b.onclick = () => setTimer(Number(b.dataset.min));
});

$('#startTimer').onclick = toggleTimer;

$('#resetTimer').onclick = () => setTimer(state.minutes);

// ==========================================
// INICIALIZAÇÃO
// ==========================================

shop();
setTimer(25);
setupPipoChat();

if (state.token) {
    enterApp();
} else {
    showAuth();
}
