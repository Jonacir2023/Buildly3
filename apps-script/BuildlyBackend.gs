/**
 * BUILDLy Premium — Backend único (Google Apps Script)
 *
 * Recriado em 2026-08-21 porque o projeto Apps Script original foi apagado
 * por engano durante a limpeza da obra encerrada. Todo o contrato abaixo
 * (nomes de path/action, formato do JSON de entrada e saída) foi reconstruído
 * lendo os `fetch()` de pauta.html, Check-in.html, rdo.html e
 * buildly-completo.html — nunca vi o código-fonte original, então os NOMES
 * das colunas da planilha são escolha minha (o front-end não depende deles,
 * só do JSON que este script devolve).
 *
 * NÃO TESTADO contra o Google de verdade — o ambiente onde este arquivo foi
 * escrito não tem acesso a script.google.com. Antes de confiar nele:
 * 1. Cole este código em Extensões → Apps Script (na planilha Buildly3).
 * 2. Implantar → Nova implantação → Web app → Executar como: Eu → Quem pode
 *    acessar: Qualquer pessoa.
 * 3. Copie a URL /exec e cole no lugar da APPS_SCRIPT_URL(_PAUTA/_DIARIO) nos
 *    5 HTMLs (todos apontam pra a mesma URL hoje).
 * 4. Teste: crie um assunto na Pauta e clique em atualizar — se salvar e
 *    voltar sem erro, tá funcionando.
 *
 * FORA DO ESCOPO (não implementado aqui, decisão pendente):
 * - path=ia&action=perguntar — respondia perguntas cruzando os dados da
 *   planilha via algum modelo de IA. Precisa decidir qual API usar e como
 *   guardar a chave; não dá pra reconstruir isso sem o código original.
 * - path=custos&action=* — custos.html declara a URL mas não chama nenhum
 *   endpoint ainda (nunca foi ligado no front-end), então não há contrato
 *   pra reconstruir. Ver README.md do repo pra estrutura de dados pretendida.
 */

const SHEET_ID = '19SDuzU_CLzDRfbNZWJZQzchLDCeQYHgiSC_FxDSdhOw';
const SHEET_PAUTA = 'Pauta';
const SHEET_CHECKIN = 'CheckIn';
const SHEET_DIARIO = 'Diario';
const DRIVE_ROOT_FOLDER = 'Buildly3-Dados'; // pasta no Drive de quem implantar o script

// ============================================================
// ROTEAMENTO
// ============================================================

function doGet(e) {
  const path = e.parameter.path || '';
  const action = e.parameter.action || '';

  try {
    if (path === 'pauta' && action === 'listar') return listarPautas();
    if (path === 'checkin' && action === 'historico') return listarCheckins();
    if (path === 'backup' && action === 'buscar-ultimo') return buscarUltimoBackup(e.parameter.obra || 'Obra');
    if (path === 'foto' && action === 'base64') return fotoBase64(e.parameter.fileId);
    return errorResponse('Endpoint não encontrado: GET ' + path + '/' + action);
  } catch (err) {
    return errorResponse(err.message);
  }
}

function doPost(e) {
  let data = {};
  try {
    data = JSON.parse(e.postData.contents);
  } catch (err) {
    return errorResponse('JSON inválido no corpo do POST');
  }

  // pauta/checkin/diario mandam path+action na query string; backup e foto
  // mandam só "path" dentro do corpo (sem action) — replicado como no
  // front-end atual (rdo.html: backupNuvem() e adicionarFotoDia()).
  const path = e.parameter.path || data.path || '';
  const action = e.parameter.action || '';

  try {
    if (path === 'pauta' && action === 'criar') return criarPauta(data);
    if (path === 'pauta' && action === 'atualizar-status') return atualizarStatusPauta(data);
    if (path === 'checkin' && action === 'salvar') return salvarCheckin(data);
    if (path === 'diario' && action === 'salvar') return salvarDiario(data);
    if (path === 'backup') return salvarBackup(data);
    if (path === 'foto') return salvarFoto(data);
    return errorResponse('Endpoint não encontrado: POST ' + path + '/' + action);
  } catch (err) {
    return errorResponse(err.message);
  }
}

// ============================================================
// PAUTA
// Colunas: A id | B assunto | C descricao | D criador | E responsavel |
//          F setor | G prioridade | H status | I data_lancamento |
//          J data_termino | K criado_em | L atualizado_em
// ============================================================

function criarPauta(data) {
  const sheet = getOrCreateSheet(SHEET_PAUTA, [
    'id', 'assunto', 'descricao', 'criador', 'responsavel', 'setor',
    'prioridade', 'status', 'data_lancamento', 'data_termino',
    'criado_em', 'atualizado_em'
  ]);

  const id = String(data.id || ('PAUTA-' + Date.now()));
  const agora = new Date().toISOString();

  sheet.appendRow([
    id,
    data.assunto || '',
    data.descricao || '',
    data.criador || '',
    data.responsavel || '',
    data.setor || '',
    data.prioridade || 'Média',
    'Aberta',
    data.data_lancamento || new Date().toISOString().slice(0, 10),
    data.data_termino || '',
    agora,
    agora
  ]);

  return successResponse({ ok: true, id: id, status: 'Aberta' });
}

function atualizarStatusPauta(data) {
  const sheet = getOrCreateSheet(SHEET_PAUTA, [
    'id', 'assunto', 'descricao', 'criador', 'responsavel', 'setor',
    'prioridade', 'status', 'data_lancamento', 'data_termino',
    'criado_em', 'atualizado_em'
  ]);

  const id = String(data.id || '');
  const novoStatus = data.novo_status || '';
  const values = sheet.getDataRange().getValues();

  for (let i = 1; i < values.length; i++) {
    if (String(values[i][0]) === id) {
      sheet.getRange(i + 1, 8).setValue(novoStatus);              // status
      sheet.getRange(i + 1, 12).setValue(new Date().toISOString()); // atualizado_em
      return successResponse({ ok: true, status: novoStatus });
    }
  }

  return errorResponse('Pauta não encontrada: ' + id);
}

// GET listar — formato exigido pelo front-end (pauta.html, Check-in.html,
// buildly-completo.html): { dados: [ {id, assunto, desc, criador, resp,
// setor, prioridade, status, dataLanc, dataTerm, 'Criado Em'} ] }
function listarPautas() {
  const sheet = getOrCreateSheet(SHEET_PAUTA, [
    'id', 'assunto', 'descricao', 'criador', 'responsavel', 'setor',
    'prioridade', 'status', 'data_lancamento', 'data_termino',
    'criado_em', 'atualizado_em'
  ]);

  const values = sheet.getDataRange().getValues();
  const pautas = [];
  for (let i = 1; i < values.length; i++) {
    const row = values[i];
    if (!row[0]) continue;
    pautas.push({
      id: String(row[0]),
      assunto: row[1],
      desc: row[2],
      criador: row[3],
      resp: row[4],
      setor: row[5],
      prioridade: row[6],
      status: row[7],
      dataLanc: formatarDataOuTexto(row[8]),
      dataTerm: formatarDataOuTexto(row[9]),
      'Criado Em': formatarIsoOuTexto(row[10])
    });
  }

  return successResponse({ dados: pautas, pautas: pautas });
}

// ============================================================
// CHECKIN
// Colunas: A id | B data | C hora | D obra | E assuntos_json | F resumo |
//          G criado_em
// ============================================================

function salvarCheckin(data) {
  const sheet = getOrCreateSheet(SHEET_CHECKIN, [
    'id', 'data', 'hora', 'obra', 'assuntos_json', 'resumo', 'criado_em'
  ]);

  const id = 'CHECKIN-' + Date.now();
  const agora = new Date().toISOString();

  sheet.appendRow([
    id,
    data.data || '',
    data.hora || '',
    data.obra || '',
    JSON.stringify(data.assuntos || []),
    data.resumo || '',
    agora
  ]);

  return successResponse({ ok: true, id: id });
}

// GET historico — formato exigido pelo front-end: { dados: [...] }
function listarCheckins() {
  const sheet = getOrCreateSheet(SHEET_CHECKIN, [
    'id', 'data', 'hora', 'obra', 'assuntos_json', 'resumo', 'criado_em'
  ]);

  const values = sheet.getDataRange().getValues();
  const checkins = [];
  for (let i = 1; i < values.length; i++) {
    const row = values[i];
    if (!row[0]) continue;
    let assuntos = [];
    try { assuntos = JSON.parse(row[4] || '[]'); } catch (e) {}
    checkins.push({
      id: String(row[0]),
      data: row[1],
      hora: row[2],
      obra: row[3],
      assuntos: assuntos,
      resumo: row[5],
      'Criado Em': formatarIsoOuTexto(row[6])
    });
  }

  return successResponse({ dados: checkins, checkins: checkins });
}

// ============================================================
// DIÁRIO (RDO)
// Upsert por (obra + data): rdo.html chama "salvar" toda vez que o usuário
// salva o dia, não só uma vez — sem upsert a aba encheria de linhas
// duplicadas pro mesmo dia.
// ============================================================

function salvarDiario(data) {
  const headers = [
    'id', 'rdoNum', 'data', 'diaSemana', 'obra', 'empresa', 'local',
    'descricaoObra', 'tempo', 'jornada', 'dssHorario', 'dssMinistrou',
    'dssTema', 'atividades', 'efetivoTotal', 'efetivoPorFuncao',
    'colaboradoresPresentes', 'equipamentos', 'veiculosLeves',
    'veiculosParados', 'eventosSeguranca', 'eventosMeioAmbiente',
    'observacoes', 'apontador', 'localObra', 'descricaoLocal', 'fotos',
    'criado_em', 'atualizado_em'
  ];
  const sheet = getOrCreateSheet(SHEET_DIARIO, headers);

  const obra = data.obra || '';
  const dataRdo = data.data || '';
  const agora = new Date().toISOString();
  const values = sheet.getDataRange().getValues();

  const linha = [
    '', // id preenchido abaixo
    data.rdoNum || '',
    dataRdo,
    data.diaSemana || '',
    obra,
    data.empresa || '',
    data.local || '',
    data.descricaoObra || '',
    data.tempo || '',
    data.jornada || '',
    data.dssHorario || '',
    data.dssMinistrou || '',
    data.dssTema || '',
    data.atividades || '',
    data.efetivoTotal || 0,
    data.efetivoPorFuncao || '',
    data.colaboradoresPresentes || '',
    data.equipamentos || '',
    data.veiculosLeves || '',
    data.veiculosParados || '',
    data.eventosSeguranca || '',
    data.eventosMeioAmbiente || '',
    data.observacoes || '',
    data.apontador || '',
    data.localObra || '',
    data.descricaoLocal || '',
    data.fotos || '',
    '', // criado_em preenchido abaixo
    agora
  ];

  for (let i = 1; i < values.length; i++) {
    if (String(values[i][4]) === obra && String(values[i][2]) === dataRdo) {
      const linhaExistente = i + 1;
      linha[0] = values[i][0];               // mantém o id original
      linha[27] = values[i][27] || agora;     // mantém criado_em original
      sheet.getRange(linhaExistente, 1, 1, linha.length).setValues([linha]);
      return successResponse({ ok: true, id: linha[0] });
    }
  }

  linha[0] = 'RDO-' + Date.now();
  linha[27] = agora;
  sheet.appendRow(linha);
  return successResponse({ ok: true, id: linha[0] });
}

// ============================================================
// BACKUP (snapshot completo do RDO no Drive, por obra)
// POST body: { path:'backup', obra, conteudo }  (sem "action")
// GET: ?path=backup&action=buscar-ultimo&obra=X
// ============================================================

function salvarBackup(data) {
  const obra = data.obra || 'Obra';
  const conteudo = data.conteudo || '{}';
  const pasta = getOrCreateFolder(DRIVE_ROOT_FOLDER);
  const nomeArquivo = 'backup-' + slugify(obra) + '.json';

  const existentes = pasta.getFilesByName(nomeArquivo);
  if (existentes.hasNext()) {
    const arquivo = existentes.next();
    arquivo.setContent(conteudo);
  } else {
    pasta.createFile(nomeArquivo, conteudo, MimeType.PLAIN_TEXT);
  }

  return successResponse({ ok: true });
}

function buscarUltimoBackup(obra) {
  const pasta = getOrCreateFolder(DRIVE_ROOT_FOLDER);
  const nomeArquivo = 'backup-' + slugify(obra) + '.json';
  const existentes = pasta.getFilesByName(nomeArquivo);

  if (!existentes.hasNext()) {
    return successResponse({ ok: false, msg: 'Nenhum backup encontrado na nuvem' });
  }

  const arquivo = existentes.next();
  return successResponse({
    ok: true,
    conteudo: arquivo.getBlob().getDataAsString(),
    data: arquivo.getLastUpdated().toISOString()
  });
}

// ============================================================
// FOTO (upload/leitura de fotos do RDO via Drive)
// POST body: { path:'foto', data, obra, base64 } → { fileId, url }
// GET: ?path=foto&action=base64&fileId=X → { dataUri }
// ============================================================

function salvarFoto(data) {
  const obra = slugify(data.obra || 'Obra');
  const pastaRaiz = getOrCreateFolder(DRIVE_ROOT_FOLDER);
  const pastaFotos = getOrCreateSubfolder(pastaRaiz, 'Fotos');
  const pastaObra = getOrCreateSubfolder(pastaFotos, obra);

  const bytes = Utilities.base64Decode(data.base64);
  const blob = Utilities.newBlob(bytes, 'image/jpeg', (data.data || 'foto') + '-' + Date.now() + '.jpg');
  const arquivo = pastaObra.createFile(blob);
  arquivo.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);

  return successResponse({
    ok: true,
    fileId: arquivo.getId(),
    url: arquivo.getUrl()
  });
}

function fotoBase64(fileId) {
  if (!fileId) return errorResponse('fileId ausente');
  const arquivo = DriveApp.getFileById(fileId);
  const blob = arquivo.getBlob();
  const base64 = Utilities.base64Encode(blob.getBytes());
  const mimeType = blob.getContentType() || 'image/jpeg';

  return successResponse({
    ok: true,
    dataUri: 'data:' + mimeType + ';base64,' + base64,
    base64: base64,
    mimeType: mimeType
  });
}

// ============================================================
// Utils
// ============================================================

function getOrCreateSheet(nome, headers) {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  let sheet = ss.getSheetByName(nome);
  if (!sheet) {
    sheet = ss.insertSheet(nome);
    sheet.appendRow(headers);
  }
  return sheet;
}

function getOrCreateFolder(nome) {
  const pastas = DriveApp.getFoldersByName(nome);
  if (pastas.hasNext()) return pastas.next();
  return DriveApp.createFolder(nome);
}

function getOrCreateSubfolder(pastaPai, nome) {
  const pastas = pastaPai.getFoldersByName(nome);
  if (pastas.hasNext()) return pastas.next();
  return pastaPai.createFolder(nome);
}

function slugify(texto) {
  return String(texto || 'obra')
    .normalize('NFD').replace(/[̀-ͯ]/g, '')
    .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '') || 'obra';
}

function formatarDataOuTexto(valor) {
  if (valor instanceof Date) return Utilities.formatDate(valor, 'GMT', 'yyyy-MM-dd');
  return valor || '';
}

function formatarIsoOuTexto(valor) {
  if (valor instanceof Date) return valor.toISOString();
  return valor || '';
}

function successResponse(data) {
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}

function errorResponse(msg) {
  return ContentService.createTextOutput(JSON.stringify({ ok: false, error: msg }))
    .setMimeType(ContentService.MimeType.JSON);
}
