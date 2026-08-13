// Buildly — shell base (login, navegação, seleção de obra)
// Autenticação e lista de obras via Supabase (js/supabase-client.js).

const MODULOS = [
  "tarefas", "atas", "planejamento", "orcamento",
  "rdo", "efetivo", "ged", "seguranca", "estoque",
  "equipes", "fornecedores", "terceiros",
];

const TITULOS_MODULO = {
  tarefas: "Gestão de Tarefas",
  atas: "Ata de Reunião",
  planejamento: "Planejamento de Obra",
  orcamento: "Orçamento",
  rdo: "Diário de Obras (RDO)",
  efetivo: "Efetivo",
  ged: "GED",
  seguranca: "Segurança do Trabalho",
  estoque: "Controle de Estoque",
  equipes: "Gestão de Equipes",
  fornecedores: "Fornecedores",
  terceiros: "Terceiros",
};

let obras = [];

const telaLogin = document.getElementById("tela-login");
const telaApp = document.getElementById("tela-app");
const formLogin = document.getElementById("form-login");
const loginErro = document.getElementById("login-erro");
const selectObra = document.getElementById("select-obra");
const obraAtivaNome = document.getElementById("obra-ativa-nome");
const tituloModulo = document.getElementById("titulo-modulo");
const areaModulo = document.getElementById("area-modulo");
const usuarioNome = document.getElementById("usuario-nome");
const btnLogout = document.getElementById("btn-logout");
const btnRecolherSidebar = document.getElementById("btn-recolher-sidebar");
const sidebar = document.querySelector(".sidebar");

async function carregarObras() {
  const { data, error } = await db
    .from("obra")
    .select("id, nome")
    .order("nome");

  if (error) {
    console.error("Erro ao carregar obras:", error);
    obras = [];
    return;
  }

  obras = data;
  selectObra.innerHTML = `<option value="">Selecionar obra…</option>`;
  for (const obra of obras) {
    const opt = document.createElement("option");
    opt.value = obra.id;
    opt.textContent = obra.nome;
    selectObra.appendChild(opt);
  }
}

function obraSelecionada() {
  return obras.find((o) => o.id === selectObra.value) || null;
}

function atualizarObraAtiva() {
  const obra = obraSelecionada();
  obraAtivaNome.textContent = obra ? obra.nome : "Nenhuma obra selecionada";
}

function renderModulo(modulo) {
  tituloModulo.textContent = TITULOS_MODULO[modulo] || "Dashboard";

  document.querySelectorAll(".nav-grupo a").forEach((a) => {
    a.classList.toggle("ativo", a.dataset.modulo === modulo);
  });

  const obra = obraSelecionada();
  if (!obra) {
    areaModulo.innerHTML = `<p class="placeholder-modulo">Selecione uma obra para acessar este módulo.</p>`;
    return;
  }

  if (modulo === "rdo") {
    renderRdoDashboard(areaModulo, obra, {
      onNovoRdo: () => renderModuloRDO(areaModulo, obra),
      onAbrirRdo: (id) => renderModuloRDO(areaModulo, obra, id),
    });
    return;
  }

  if (modulo === "efetivo") {
    renderModuloEfetivo(areaModulo, obra);
    return;
  }

  if (modulo === "equipes") {
    renderModuloEquipes(areaModulo);
    return;
  }

  // TODO: cada módulo vira seu próprio componente/arquivo conforme for implementado.
  areaModulo.innerHTML = `<p class="placeholder-modulo">Módulo "${TITULOS_MODULO[modulo]}" ainda não implementado — obra ativa: ${obra.nome}.</p>`;
}

function rotear() {
  const hash = window.location.hash.replace("#/", "");
  const modulo = MODULOS.includes(hash) ? hash : null;
  renderModulo(modulo);
}

async function entrarNoApp(usuario) {
  telaLogin.hidden = true;
  telaApp.hidden = false;
  usuarioNome.textContent = usuario.email;
  await carregarObras();
  atualizarObraAtiva();
  rotear();
}

function sairDoApp() {
  telaApp.hidden = true;
  telaLogin.hidden = false;
  formLogin.reset();
  window.location.hash = "";
}

formLogin.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  loginErro.hidden = true;

  const email = document.getElementById("login-email").value.trim();
  const senha = document.getElementById("login-senha").value;

  if (!email || !senha) {
    loginErro.textContent = "Informe e-mail e senha.";
    loginErro.hidden = false;
    return;
  }

  if (!db) {
    loginErro.textContent = "Falha ao carregar o sistema. Recarregue a página e tente novamente.";
    loginErro.hidden = false;
    return;
  }

  const { data, error } = await db.auth.signInWithPassword({
    email,
    password: senha,
  });

  if (error) {
    loginErro.textContent = "E-mail ou senha inválidos.";
    loginErro.hidden = false;
    return;
  }

  await entrarNoApp(data.user);
});

btnLogout.addEventListener("click", async () => {
  await db.auth.signOut();
  sairDoApp();
});

selectObra.addEventListener("change", () => {
  atualizarObraAtiva();
  rotear();
});

btnRecolherSidebar.addEventListener("click", () => {
  sidebar.classList.toggle("recolhida");
});

window.addEventListener("hashchange", rotear);

// Se já existir uma sessão válida (usuário recarregou a página), entra direto.
if (db) {
  db.auth.getSession().then(({ data }) => {
    if (data.session) {
      entrarNoApp(data.session.user);
    }
  });
}
