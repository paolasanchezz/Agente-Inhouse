/**
 * Pocket Event — formulario de solicitacao (BDs e SDRs) -> GitHub -> LP no ar.
 *
 * Este script mora na PLANILHA de respostas do formulario de solicitacao.
 * Ele nao decide nada sobre o conteudo da LP: so empacota a linha e entrega pro
 * workflow `pocket-event-novo.yml`, que valida e renderiza. Toda regra de
 * conteudo vive no repo (templates/pocket-event/config.json).
 *
 * ┌── PRIMEIRA VEZ ─────────────────────────────────────────────────────────┐
 * 1. Criar uma planilha nova no Drive ("Pocket Events - solicitacoes").
 * 2. Extensoes > Apps Script. Colar este arquivo inteiro em Codigo.gs.
 * 3. Configuracoes do projeto > Propriedades do script, criar tres:
 *      GITHUB_TOKEN  = PAT classico com escopo `repo` (o mesmo do POCKET_EVENT_PAT)
 *      GITHUB_REPO   = victorfmlopes/Agente-Inhouse
 *      POCKET_TOKEN  = senha longa inventada por voce (a mesma do secret
 *                      POCKET_SHEET_TOKEN no GitHub)
 * 4. Rodar `criarFormulario` e aceitar as permissoes. Ele cria o Form com as
 *    listas certas, amarra na planilha e imprime a URL de resposta no log.
 * 5. Rodar `configurar`. Instala o gatilho de envio e cria as colunas de status.
 * 6. Implantar > Nova implantacao > Aplicativo da Web
 *      Executar como: Eu | Quem tem acesso: Qualquer pessoa
 *    Colar a URL /exec no secret POCKET_SHEET_URL do GitHub.
 * └─────────────────────────────────────────────────────────────────────────┘
 *
 * MUDOU O CODIGO DEPOIS DE PUBLICAR? Salvar nao basta: Implantar > Gerenciar
 * implantacoes > editar (lapis) > Versao: "Nova versao". A URL /exec nao muda.
 *
 * MUDOU A LISTA DE NICHOS, MODULOS, HORARIOS OU SPEAKERS NO REPO?
 *   py landing-pages/build/render_pocket_event.py --form-spec
 * e colar a saida em OPCOES abaixo, depois rodar `atualizarOpcoes`.
 * As listas TEM que bater com o config.json: valor fora da lista e recusado pelo
 * workflow, e a LP nao e criada.
 */

// ===== Opcoes do formulario (espelho de config.json + speakers.json) ========
// Gerado por: py landing-pages/build/render_pocket_event.py --form-spec
var OPCOES = {
  nichos: [
    'Agência', 'Agronegócios', 'Alimentos (produtos)',
    'Alimentos (varejo)', 'Bebidas alcoólicas', 'Bebidas (produtos)',
    'Bebidas (varejo)', 'Consultoria', 'Pets',
    'Roupas, Calçados e Acessórios', 'Artigos esportivos', 'Times Esportivos',
    'Jogos e brinquedos', 'E-commerce', 'Comércio (atacado e varejo)',
    'Comunicação', 'Gráfica', 'Financeiro',
    'Administração', 'Advocacia', 'Contabilidade',
    'RH', 'Seguros', 'Holding',
    'Educação', 'Cultura', 'Eventos',
    'Atividades físicas', 'Shoppings', 'Lazer',
    'Turismo', 'Transportes', 'Transportadora e Logística',
    'Distribuidoras', 'Drogarias', 'Farmacêuticas',
    'Serviços estéticos', 'Higiene e beleza', 'Saúde',
    'Limpeza', 'Indústria química', 'Tabaco',
    'Metalurgia', 'Ferramentas e Maquinários', 'Automotivo',
    'Engenharia e Construção', 'Imóveis', 'Materiais de construção',
    'Móveis e decorações', 'Entidades e federações', 'Política',
    'Órgãos Públicos', 'ONGs', 'Eletroeletrônicos',
    'Plataformas', 'Tecnologia', 'Telecom',
    'Serviços Básicos e Energia', 'Petróleo e Gás'
  ],
  modulos: [
    'Social Listening', 'SAC 2.0', 'Dashboards e Analytics',
    'Agendamento e Publicacao', 'Analytics Avancado', 'AI Insights',
    'Buzz GPT', 'Buzz Pills'
  ],
  horarios: ['09h', '10h', '11h', '14h', '15h', '16h', '17h'],
  // Espelho de speakers.json. Mudou la? Rode --form-spec e recole aqui.
  speakers: [
    { id: 'adriane-ferreira', nome: 'Adriane Ferreira' }, { id: 'athaide-martins', nome: 'Athaide Martins' },
    { id: 'bruno-braga', nome: 'Bruno Braga' }, { id: 'daniel-jesus', nome: 'Daniel Jesus' },
    { id: 'fatima-silana', nome: 'Fatima Silana' }, { id: 'guilherme-werzel', nome: 'Guilherme Werzel' },
    { id: 'hugo-nagawa', nome: 'Hugo Nagawa' }, { id: 'juliana-mendonca', nome: 'Juliana Mendonca' },
    { id: 'leandra-lira', nome: 'Leandra Lira' }, { id: 'leticia-mello', nome: 'Leticia Mello' },
    { id: 'michelle-carmo', nome: 'Michelle Carmo' }, { id: 'nathalia-crivellaro', nome: 'Nathalia Crivellaro' },
    { id: 'paloma-braga', nome: 'Paloma Braga' }, { id: 'pedro-de-morais', nome: 'Pedro de Morais' },
    { id: 'renato-couto', nome: 'Renato Couto' }, { id: 'tereza-rici', nome: 'Tereza Rici' },
    { id: 'tiago-cantu', nome: 'Tiago Cantu' }, { id: 'valkiria-guedes', nome: 'Valkiria Guedes' },
    { id: 'camila-ribeiro', nome: 'Camila Ribeiro' }, { id: 'anna-beatriz', nome: 'Anna Beatriz' },
    { id: 'jacqueline-castro', nome: 'Jacqueline Castro' }
  ],
  titulo_max: 60,
  dias_maximo: 180
};

// ===== Colunas ==============================================================
var COL = {
  carimbo: 'Carimbo de data/hora',
  email: 'Endereco de e-mail',
  titulo: 'Titulo do encontro',
  nicho: 'Nicho',
  modulo: 'Modulo Buzzmonitor',
  data: 'Data do encontro',
  horario: 'Horario',
  speaker: 'Quem apresenta',
  status: 'Status',
  url: 'URL da LP',
  detalhe: 'Detalhe'
};
var COLUNAS_CONTROLE = [COL.status, COL.url, COL.detalhe];

// ===========================================================================
// Criacao do formulario
// ===========================================================================
function criarFormulario(forcar) {
  var planilha = SpreadsheetApp.getActiveSpreadsheet();

  // Trava: rodar isto por engano com um formulario ja ligado cria um SEGUNDO
  // formulario, uma segunda aba de respostas e duas versoes das mesmas perguntas
  // circulando (aconteceu em 2026-09-14). Pra mudar as opcoes do formulario que
  // ja existe, o caminho e `atualizarOpcoes`, nao este.
  var jaTem = planilha.getFormUrl();
  if (jaTem && !forcar) {
    throw new Error('Esta planilha JA tem um formulario ligado (' + jaTem + '). ' +
                    'Para trocar as opcoes, rode atualizarOpcoes. Para criar um ' +
                    'segundo formulario mesmo assim, chame criarFormulario(true).');
  }

  var form = FormApp.create('Pocket Event - solicitar LP')
    .setDescription(
      'Preencha para gerar a landing page de um Pocket Event. A pagina entra no ar ' +
      'sozinha em poucos minutos. Tudo que nao esta aqui (bio do speaker, depoimentos, ' +
      'social proof) ja vem pronto do modelo.')
    .setCollectEmail(true)
    .setRequireLogin(true);

  form.addTextItem()
    .setTitle(COL.titulo)
    .setHelpText('Ate ' + OPCOES.titulo_max + ' caracteres. Sem ponto final, sem travessao ' +
                 '(-) e sem aspas. Ex: Como o varejo escuta o cliente em tempo real')
    .setRequired(true)
    .setValidation(FormApp.createTextValidation()
      .requireTextLengthLessThanOrEqualTo(OPCOES.titulo_max).build());

  form.addListItem().setTitle(COL.nicho).setChoiceValues(OPCOES.nichos).setRequired(true);
  // Caixa de selecao, nao lista: um encontro pode cobrir mais de um modulo.
  // A planilha recebe as marcadas como "A, B, C" numa celula so, e o validador
  // do repo separa por virgula.
  form.addCheckboxItem().setTitle(COL.modulo)
    .setHelpText('Marque um ou mais. Aparecem na LP na ordem desta lista.')
    .setChoiceValues(OPCOES.modulos).setRequired(true);
  form.addDateItem().setTitle(COL.data)
    .setHelpText('No maximo ' + OPCOES.dias_maximo + ' dias a frente. Data passada e recusada.')
    .setRequired(true);
  form.addListItem().setTitle(COL.horario)
    .setHelpText('Horario de Brasilia.')
    .setChoiceValues(OPCOES.horarios).setRequired(true);

  if (OPCOES.speakers.length) {
    form.addListItem().setTitle(COL.speaker)
      .setHelpText('Cargo, bio e foto ja estao cadastrados. Nao esta na lista? Pedir ' +
                   'o cadastro antes de solicitar a LP.')
      .setChoiceValues(OPCOES.speakers.map(function (s) { return s.nome; }))
      .setRequired(true);
  } else {
    form.addTextItem().setTitle(COL.speaker)
      .setHelpText('ATENCAO: nenhum speaker cadastrado ainda. Cadastre em ' +
                   'speakers.json e rode atualizarOpcoes.')
      .setRequired(true);
  }

  form.setDestination(FormApp.DestinationType.SPREADSHEET, planilha.getId());
  Logger.log('Formulario criado. Link para responder:\n' + form.getPublishedUrl());
  Logger.log('Link para editar:\n' + form.getEditUrl());
  return form.getPublishedUrl();
}

/**
 * Converte o campo de modulo de lista (1 escolha) para caixa de selecao (N
 * escolhas), preservando titulo, ajuda, obrigatoriedade e posicao.
 *
 * Existe porque `setChoiceValues` so troca as opcoes de um campo: nao muda o
 * TIPO dele. Um formulario criado antes da multisselecao continuaria aceitando
 * um modulo so, em silencio. Roda sozinha dentro de `atualizarOpcoes`.
 *
 * A coluna da planilha nao se mexe (mesmo titulo), entao as respostas antigas
 * continuam onde estavam.
 */
function migrarModuloParaCheckbox_(form) {
  var antigo = null;
  form.getItems(FormApp.ItemType.LIST).forEach(function (item) {
    if (item.getTitle() === COL.modulo) antigo = item;
  });
  if (!antigo) return false;  // ja e checkbox, ou o campo nao existe

  var posicao = antigo.getIndex();
  var ajuda = antigo.getHelpText();
  var obrigatorio = antigo.asListItem().isRequired();
  form.deleteItem(antigo);

  var novo = form.addCheckboxItem()
    .setTitle(COL.modulo)
    .setHelpText(ajuda || 'Marque um ou mais. Aparecem na LP na ordem desta lista.')
    .setChoiceValues(OPCOES.modulos)
    .setRequired(obrigatorio);
  form.moveItem(novo.getIndex(), posicao);
  return true;
}

/** Re-sincroniza as listas do formulario com o OPCOES deste arquivo. */
function atualizarOpcoes() {
  var form = FormApp.openByUrl(
    SpreadsheetApp.getActiveSpreadsheet().getFormUrl());
  var migrou = migrarModuloParaCheckbox_(form);
  var mapa = {};
  mapa[COL.nicho] = OPCOES.nichos;
  mapa[COL.modulo] = OPCOES.modulos;
  mapa[COL.horario] = OPCOES.horarios;
  mapa[COL.speaker] = OPCOES.speakers.map(function (s) { return s.nome; });

  var tocados = 0;
  form.getItems(FormApp.ItemType.LIST).forEach(function (item) {
    var novas = mapa[item.getTitle()];
    if (novas && novas.length) { item.asListItem().setChoiceValues(novas); tocados++; }
  });
  // O modulo e caixa de selecao (CHECKBOX), que nao aparece no getItems(LIST).
  form.getItems(FormApp.ItemType.CHECKBOX).forEach(function (item) {
    var novas = mapa[item.getTitle()];
    if (novas && novas.length) { item.asCheckboxItem().setChoiceValues(novas); tocados++; }
  });
  return tocados + ' campo(s) atualizado(s)' +
    (migrou ? ' + modulo convertido de lista para caixa de selecao' : '');
}

/** Instala o gatilho de envio e garante as colunas de controle. */
function configurar() {
  var planilha = SpreadsheetApp.getActiveSpreadsheet();

  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'aoEnviarFormulario') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('aoEnviarFormulario').forSpreadsheet(planilha).onFormSubmit().create();

  var aba = aba_();
  var cabecalhos = cabecalhos_(aba);
  COLUNAS_CONTROLE.forEach(function (nome) {
    if (cabecalhos.indexOf(nome) < 0) {
      aba.getRange(1, aba.getLastColumn() + 1).setValue(nome).setFontWeight('bold');
      cabecalhos.push(nome);
    }
  });
  aba.setFrozenRows(1);

  var faltando = ['GITHUB_TOKEN', 'GITHUB_REPO', 'POCKET_TOKEN'].filter(function (p) {
    return !PropertiesService.getScriptProperties().getProperty(p);
  });
  return faltando.length
    ? 'gatilho ok, MAS faltam propriedades do script: ' + faltando.join(', ')
    : 'gatilho instalado e colunas de controle prontas';
}

// ===========================================================================
// Envio -> GitHub
// ===========================================================================
function aoEnviarFormulario(e) {
  var linha = e && e.range ? e.range.getRow() : aba_().getLastRow();
  var pedido = lerLinha_(linha);
  if (!pedido) return;
  try {
    dispararGitHub_([pedido]);
    marcarLinha_(linha, 'enviada', '', 'aguardando o GitHub Actions');
  } catch (err) {
    // Nao marca erro: a varredura diaria pega de novo a linha sem status.
    Logger.log('falha ao disparar o GitHub: ' + err);
  }
}

function dispararGitHub_(solicitacoes) {
  var props = PropertiesService.getScriptProperties();
  var repo = props.getProperty('GITHUB_REPO');
  var token = props.getProperty('GITHUB_TOKEN');
  if (!repo || !token) throw new Error('GITHUB_REPO/GITHUB_TOKEN nao configurados');

  var resposta = UrlFetchApp.fetch('https://api.github.com/repos/' + repo + '/dispatches', {
    method: 'post',
    contentType: 'application/json',
    headers: { Authorization: 'Bearer ' + token, Accept: 'application/vnd.github+json' },
    payload: JSON.stringify({
      event_type: 'pocket-event',
      client_payload: { solicitacoes: solicitacoes }
    }),
    muteHttpExceptions: true
  });
  var codigo = resposta.getResponseCode();
  if (codigo !== 204) {
    throw new Error('GitHub respondeu ' + codigo + ': ' + resposta.getContentText());
  }
}

// ===========================================================================
// Web app: varredura diaria (doGet) e escrita de volta (doPost)
// ===========================================================================
function doGet(e) {
  if (!autorizado_(e && e.parameter)) return responder_({ ok: false, error: 'token invalido' });
  if (e.parameter.acao !== 'pendentes') {
    return responder_({ ok: true, servico: 'Pocket Event - solicitacoes' });
  }
  var aba = aba_();
  var pendentes = [];
  for (var linha = 2; linha <= aba.getLastRow(); linha++) {
    var status = String(valor_(aba, linha, COL.status) || '').trim();
    // 'enviada' entra de novo de proposito: o webhook pode ter disparado e o
    // workflow ter falhado antes de criar qualquer coisa. Criar duas vezes nao
    // e risco — o job ignora slug que ja existe.
    if (status === '' || status === 'enviada') {
      var pedido = lerLinha_(linha);
      if (pedido) pendentes.push(pedido);
    }
  }
  return responder_({ ok: true, solicitacoes: pendentes });
}

function doPost(e) {
  var corpo;
  try {
    corpo = JSON.parse(e.postData.contents);
  } catch (err) {
    return responder_({ ok: false, error: 'corpo invalido' });
  }
  if (!autorizado_(corpo)) return responder_({ ok: false, error: 'token invalido' });
  if (corpo.acao !== 'marcar') return responder_({ ok: false, error: 'acao desconhecida' });

  (corpo.linhas || []).forEach(function (m) {
    marcarLinha_(m.linha, m.status, m.url || '', m.motivo || '');
  });
  return responder_({ ok: true, marcadas: (corpo.linhas || []).length });
}

// ===========================================================================
// Helpers
// ===========================================================================
function autorizado_(obj) {
  var esperado = PropertiesService.getScriptProperties().getProperty('POCKET_TOKEN');
  return !!esperado && !!obj && obj.token === esperado;
}

/**
 * A aba das respostas, achada pelo CONTEUDO e nao pelo nome nem pela posicao.
 *
 * Procurar por nome nao funciona: o Google nomeia a aba "Respostas ao formulário 1",
 * com acento e no idioma da conta. E cair em getSheets()[0] e pior ainda, porque a
 * ordem das abas muda — um formulario novo ligado a mesma planilha entra na frente e
 * o script passa a ler uma aba vazia, sem erro nenhum (foi o que aconteceu em
 * 2026-09-14). Entao: vale a aba que tiver o cabecalho do titulo do encontro.
 */
function aba_() {
  var planilha = SpreadsheetApp.getActiveSpreadsheet();
  var abas = planilha.getSheets();
  var alvo = normalizar_(COL.titulo);
  for (var i = 0; i < abas.length; i++) {
    if (abas[i].getLastColumn() < 1) continue;
    var cabecalhos = abas[i].getRange(1, 1, 1, abas[i].getLastColumn()).getValues()[0];
    for (var c = 0; c < cabecalhos.length; c++) {
      if (normalizar_(cabecalhos[c]) === alvo) return abas[i];
    }
  }
  throw new Error('nenhuma aba tem a coluna "' + COL.titulo + '". O formulario ja foi ' +
                  'criado e ligado a esta planilha? (rodar criarFormulario)');
}

function cabecalhos_(aba) {
  return aba.getRange(1, 1, 1, Math.max(aba.getLastColumn(), 1)).getValues()[0]
    .map(function (v) { return String(v).trim(); });
}

/** Acha a coluna pelo cabecalho, ignorando acento e caixa. */
function coluna_(aba, nome) {
  var alvo = normalizar_(nome);
  var cabecalhos = cabecalhos_(aba);
  for (var i = 0; i < cabecalhos.length; i++) {
    if (normalizar_(cabecalhos[i]) === alvo) return i + 1;
  }
  return 0;
}

function normalizar_(s) {
  return String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();
}

function valor_(aba, linha, nome) {
  var c = coluna_(aba, nome);
  return c ? aba.getRange(linha, c).getValue() : '';
}

/** Data pode chegar como Date (Form) ou texto. A LP so aceita AAAA-MM-DD. */
function dataISO_(v) {
  if (v instanceof Date) {
    return Utilities.formatDate(v, 'America/Sao_Paulo', 'yyyy-MM-dd');
  }
  return String(v || '').trim();
}

function lerLinha_(linha) {
  var aba = aba_();
  var titulo = String(valor_(aba, linha, COL.titulo) || '').trim();
  if (!titulo) return null;
  return {
    linha: linha,
    solicitante: String(valor_(aba, linha, COL.email) || '').trim(),
    titulo: titulo,
    nicho: String(valor_(aba, linha, COL.nicho) || '').trim(),
    modulo: String(valor_(aba, linha, COL.modulo) || '').trim(),
    data: dataISO_(valor_(aba, linha, COL.data)),
    horario: String(valor_(aba, linha, COL.horario) || '').trim(),
    speaker: String(valor_(aba, linha, COL.speaker) || '').trim()
  };
}

function marcarLinha_(linha, status, url, detalhe) {
  if (!linha) return;
  var aba = aba_();
  var mapa = [[COL.status, status], [COL.url, url], [COL.detalhe, detalhe]];
  mapa.forEach(function (par) {
    var c = coluna_(aba, par[0]);
    if (c) aba.getRange(linha, c).setValue(par[1]);
  });
}

function responder_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
