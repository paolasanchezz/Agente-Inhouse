/**
 * Buzz Compass: leads do totem do evento -> planilha do Google Sheets.
 *
 * O backend do Buzz Compass (landing-pages/buzzmonitor/buzz-radar/api/totem-lead.js) manda um POST com os dados de cada
 * lead para a URL deste script. Ele grava uma linha por lead. E uma das tres saidas do lead (as outras sao o
 * ActiveCampaign, com a tag "Buzz Compass", e o e-mail com o QR code): se uma delas falhar, as outras continuam.
 *
 * ┌── PRIMEIRA VEZ ────────────────────────────────────────────────
 * 1. Criar a planilha "Buzz Compass - leads" e anotar o ID que esta na URL
 *    (docs.google.com/spreadsheets/d/ESTE_TRECHO/edit).
 * 2. Extensoes > Apps Script, colar este arquivo inteiro e preencher ID_PLANILHA abaixo.
 * 3. Escolher uma senha longa (o TOKEN). No Apps Script: Configuracoes do projeto (engrenagem) > Propriedades do script >
 *    Adicionar propriedade: nome TOKEN, valor = a senha. Anotar a senha: ela vai para a Vercel no passo 6.
 * 4. Rodar a funcao `prepararCabecalhos` (menu superior) e aceitar as permissoes.
 * 5. Implantar > Nova implantacao > tipo "Aplicativo da Web"
 *      Executar como: Eu | Quem tem acesso: Qualquer pessoa
 *    Copiar a URL que termina em /exec.
 * 6. No projeto buzzmonitor-lp-buzz-radar da Vercel (Settings > Environment Variables, ambiente Production):
 *      TOTEM_LEADS_WEBHOOK_URL   = a URL /exec do passo 5
 *      TOTEM_LEADS_WEBHOOK_TOKEN = a senha do passo 3
 *    e republicar o projeto (variavel nova so vale no proximo deploy).
 * 7. Testar: rodar `testarLinha` aqui (grava uma linha de teste; apague depois) e depois fazer um Compass de verdade.
 *
 * JA TINHA PUBLICADO A VERSAO ANTIGA (so ate a coluna "Origem")? Para ganhar as colunas de URL de conversao e UTMs: cole este arquivo
 * de novo, rode `prepararCabecalhos` (reescreve so a linha 1) e publique "Nova versao" (ver abaixo). As linhas antigas ficam como estao.
 * └──────────────────────────────────────────────────────────────────
 *
 * MUDOU O CODIGO DEPOIS DE PUBLICAR? Implantar > Gerenciar implantacoes > editar (lapis) > Versao: "Nova versao".
 * So salvar nao troca o que roda.
 *
 * SEGURANCA: a URL /exec e publica (o servidor da Vercel precisa chamar). Quem protege e o TOKEN: sem ele a linha nao e
 * gravada. O doGet devolve so uma mensagem de funcionamento, nunca o conteudo da planilha. Cada linha nova e formatada
 * como TEXTO PURO antes de gravar: o que o lead digitou no totem nunca vira formula (ex.: "=IMPORTXML(...)").
 */

var ID_PLANILHA = '';
var NOME_ABA = 'Leads';

var COLUNAS = [
  'Data e hora', 'Nome', 'E-mail', 'Marca', 'Segmento', 'Instagram da marca',
  'Concorrentes informados', 'Link do resultado', 'Origem',
  'URL de conversao', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'
];

function aba_() {
  if (!ID_PLANILHA) throw new Error('ID_PLANILHA nao preenchido no topo do script');
  var livro = SpreadsheetApp.openById(ID_PLANILHA);
  var h = livro.getSheetByName(NOME_ABA);
  if (!h) {
    h = livro.insertSheet(NOME_ABA);
    prepararCabecalhos();
    h = livro.getSheetByName(NOME_ABA);
  }
  return h;
}

function prepararCabecalhos() {
  if (!ID_PLANILHA) throw new Error('ID_PLANILHA nao preenchido no topo do script');
  var livro = SpreadsheetApp.openById(ID_PLANILHA);
  var h = livro.getSheetByName(NOME_ABA) || livro.insertSheet(NOME_ABA);
  h.getRange(1, 1, 1, COLUNAS.length).setValues([COLUNAS]).setFontWeight('bold');
  h.setFrozenRows(1);
  h.setColumnWidth(1, 150);
  h.setColumnWidth(8, 360);
}

function texto_(v) {
  return (v == null ? '' : String(v)).replace(/[\r\n\t]+/g, ' ').slice(0, 500);
}

// Grava a linha no fim da planilha, ja formatada como texto puro (formato "@") ANTES de colocar os valores. Assim "=1+1" ou
// "+55 11 9999" ficam exatamente como foram digitados, sem virar formula e sem apostrofo aparecendo.
function gravarLinha_(valores) {
  var h = aba_();
  var linha = h.getLastRow() + 1;
  var faixa = h.getRange(linha, 1, 1, valores.length);
  faixa.setNumberFormat('@');
  faixa.setValues([valores]);
}

function dataHora_(iso) {
  var d = iso ? new Date(iso) : new Date();
  if (isNaN(d.getTime())) d = new Date();
  return Utilities.formatDate(d, 'America/Sao_Paulo', 'dd/MM/yyyy HH:mm:ss');
}

function resposta_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  var trava = LockService.getScriptLock();
  try {
    trava.waitLock(20000); // varios leads ao mesmo tempo (evento cheio) entram um por vez, sem se atropelar
  } catch (err) {
    return resposta_({ ok: false, erro: 'ocupado' });
  }
  try {
    var senha = PropertiesService.getScriptProperties().getProperty('TOKEN');
    if (!senha) return resposta_({ ok: false, erro: 'TOKEN nao configurado nas Propriedades do script' });
    var d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    if (d.token !== senha) return resposta_({ ok: false, erro: 'token' });
    if (!d.email) return resposta_({ ok: false, erro: 'sem e-mail' });

    var concorrentes = Array.isArray(d.concorrentes) ? d.concorrentes.join(', ') : d.concorrentes;
    gravarLinha_([
      dataHora_(d.criado_em),
      texto_(d.nome),
      texto_(d.email),
      texto_(d.marca),
      texto_(d.segmento),
      texto_(d.instagram ? '@' + String(d.instagram).replace(/^@/, '') : ''),
      texto_(concorrentes),
      texto_(d.link),
      texto_(d.origem || 'buzz-compass-totem'),
      texto_(d.url_conversao),
      texto_(d.utm_source),
      texto_(d.utm_medium),
      texto_(d.utm_campaign),
      texto_(d.utm_content),
      texto_(d.utm_term)
    ]);
    return resposta_({ ok: true });
  } catch (err) {
    return resposta_({ ok: false, erro: String(err && err.message ? err.message : err) });
  } finally {
    trava.releaseLock();
  }
}

// Abrir a URL no navegador mostra so que o script esta no ar. Nada da planilha.
function doGet() {
  return resposta_({ ok: true, servico: 'buzz-compass-leads' });
}

// Para testar sem a Vercel: grava uma linha de exemplo (apague depois).
function testarLinha() {
  gravarLinha_([dataHora_(), 'Teste', 'teste@exemplo.com', 'Marca Teste', 'Segmento Teste', '@marcateste', 'Concorrente A, Concorrente B', 'https://buzzcompass.buzzmonitor.com/totem-resultado?m=Marca+Teste', 'teste-manual',
    'https://buzzcompass.buzzmonitor.com/totem', 'evento', '', '', 'captacao-buzz-compass', '']);
}
