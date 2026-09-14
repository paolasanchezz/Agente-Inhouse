/**
 * Pocket Event — inscricoes das LPs -> planilha unica.
 *
 * Um endpoint para TODAS as edicoes. Quem separa uma da outra e a coluna
 * `Edicao` (o slug da LP), mandada pelo campo oculto do formulario. Sem sala de
 * webinar no meio: a planilha e o registro da inscricao.
 *
 * Grava `URL de conversao` e as UTMs porque lead sem `utm_source` E sem
 * `url_conversao` some do filtro das dashboards de CM (landing-pages/CONTEXT.md 5.5).
 *
 * Pocket Event tem 10 vagas. Da 11a inscricao em diante a pessoa continua sendo
 * gravada, com `Vaga` = espera, e a LP avisa que entrou na lista de espera.
 * Ninguem e barrado em silencio.
 *
 * ┌── PRIMEIRA VEZ ─────────────────────────────────────────────────────────┐
 * 1. Criar a planilha "Pocket Events - inscricoes" e anotar o ID da URL.
 * 2. Extensoes > Apps Script, colar este arquivo, preencher ID_PLANILHA abaixo.
 * 3. Rodar `prepararCabecalhos` e aceitar as permissoes.
 * 4. Implantar > Nova implantacao > Aplicativo da Web
 *      Executar como: Eu | Quem tem acesso: Qualquer pessoa
 * 5. Colar a URL /exec em `form_endpoint` de
 *    landing-pages/build/templates/pocket-event/config.json, commitar e
 *    reprocessar as LPs (ou deixar valer a partir da proxima edicao).
 * └─────────────────────────────────────────────────────────────────────────┘
 *
 * MUDOU O CODIGO DEPOIS DE PUBLICAR? Implantar > Gerenciar implantacoes >
 * editar (lapis) > Versao: "Nova versao". So salvar nao troca o que roda.
 *
 * A URL /exec e publica (tem que ser: o navegador do visitante chama direto).
 * Por isso o doGet devolve so contagem, nunca o conteudo da planilha.
 */

var ID_PLANILHA = '';       // <- ID da planilha de inscricoes
var NOME_ABA = 'Inscricoes';
var VAGAS = 10;

var COLUNAS = [
  'Data e hora', 'Edicao', 'Evento', 'Data do evento', 'Horario', 'Speaker',
  'Nome', 'E-mail', 'Empresa', 'Cargo', 'Vaga',
  'URL de conversao', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content',
  'Chave'
];

function aba_() {
  if (!ID_PLANILHA) throw new Error('ID_PLANILHA nao preenchido no topo do script');
  var livro = SpreadsheetApp.openById(ID_PLANILHA);
  var h = livro.getSheetByName(NOME_ABA);
  if (!h) {
    h = livro.insertSheet(NOME_ABA);
    prepararCabecalhos();
  }
  return h;
}

function prepararCabecalhos() {
  var livro = SpreadsheetApp.openById(ID_PLANILHA);
  var h = livro.getSheetByName(NOME_ABA) || livro.insertSheet(NOME_ABA);
  h.getRange(1, 1, 1, COLUNAS.length).setValues([COLUNAS]).setFontWeight('bold');
  h.setFrozenRows(1);
  h.setFrozenColumns(2);
  return 'pronto: ' + COLUNAS.length + ' colunas';
}

function indice_(nome) { return COLUNAS.indexOf(nome) + 1; }

/** Inscricoes ja gravadas nesta edicao, e se este e-mail ja esta entre elas. */
function situacao_(h, edicao, email) {
  var total = h.getLastRow() - 1;
  if (total <= 0) return { nesta: 0, duplicado: false };
  var edicoes = h.getRange(2, indice_('Edicao'), total, 1).getValues();
  var emails = h.getRange(2, indice_('E-mail'), total, 1).getValues();
  var nesta = 0, duplicado = false;
  for (var i = 0; i < total; i++) {
    if (String(edicoes[i][0]) !== edicao) continue;
    nesta++;
    if (String(emails[i][0]).toLowerCase() === email) duplicado = true;
  }
  return { nesta: nesta, duplicado: duplicado };
}

function texto_(v, max) {
  return String(v == null ? '' : v).trim().slice(0, max || 300);
}

function emailValido_(v) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
}

function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) {
      return responder_({ ok: false, error: 'sem corpo na requisicao' });
    }
    var d = JSON.parse(e.postData.contents);

    var email = texto_(d.email, 200).toLowerCase();
    var edicao = texto_(d.edicao, 120);
    if (!emailValido_(email)) return responder_({ ok: false, error: 'e-mail invalido' });
    if (!edicao) return responder_({ ok: false, error: 'edicao ausente' });
    if (!texto_(d.nome, 200)) return responder_({ ok: false, error: 'nome ausente' });

    var h = aba_();
    if (h.getLastRow() === 0) prepararCabecalhos();

    var s = situacao_(h, edicao, email);
    if (s.duplicado) {
      return responder_({ ok: true, duplicado: true, esgotado: s.nesta >= VAGAS });
    }

    var esgotado = s.nesta >= VAGAS;
    h.appendRow([
      new Date(), edicao, texto_(d.evento, 200), texto_(d.data_evento, 20),
      texto_(d.horario, 20), texto_(d.speaker, 200),
      texto_(d.nome, 200), email, texto_(d.empresa, 200), texto_(d.cargo, 200),
      esgotado ? 'espera' : 'confirmada',
      texto_(d.url_conversao, 500), texto_(d.utm_source, 120),
      texto_(d.utm_medium, 120), texto_(d.utm_campaign, 120), texto_(d.utm_content, 120),
      email + '|' + edicao
    ]);

    return responder_({ ok: true, duplicado: false, esgotado: esgotado });
  } catch (err) {
    return responder_({ ok: false, error: String(err) });
  }
}

/** Sinal de vida. So contagem: a URL e publica e nao pode expor lead nenhum. */
function doGet() {
  var h = aba_();
  return responder_({
    ok: true,
    servico: 'Pocket Event - inscricoes',
    inscricoes: Math.max(0, h.getLastRow() - 1)
  });
}

function responder_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
