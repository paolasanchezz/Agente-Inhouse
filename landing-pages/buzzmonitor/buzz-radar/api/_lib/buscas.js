// Monta as buscas do totem seguindo o metodo da skill /anthropic-skills:buscas-buzz-radar, reescrito para rodar
// no backend (a skill em si so executa dentro de uma sessao do Claude, nao dentro de uma pagina no ar):
//   - uma query por grupo (marca, ate 3 concorrentes, categoria), nunca uma query so
//   - grafias reais (acento, junto/separado, apelido, @perfil, #hashtag), aspas em frase, exclusao de sentido errado
//   - concorrente informado pelo visitante tem prioridade; o que faltar a IA sugere (mesmo mercado e porte parecido)
//   - concorrente sem conversa nenhuma e trocado por outro candidato
// A diferenca para a skill: a sintaxe aceita pela API guest e outra (sem AND/NOT, ver _lib/trends.js).

const { chamarJSON } = require('./llm');

const MAX_QUERY = 380;

const PLAN_SCHEMA = {
  type: 'object',
  properties: {
    marca: {
      type: 'object',
      properties: { nome_exibicao: { type: 'string' }, query: { type: 'string' } },
      required: ['nome_exibicao', 'query'],
      additionalProperties: false,
    },
    categoria: {
      type: 'object',
      properties: { nome: { type: 'string' }, query: { type: 'string' } },
      required: ['nome', 'query'],
      additionalProperties: false,
    },
    concorrentes: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          nome: { type: 'string' },
          query: { type: 'string' },
          origem: { type: 'string', enum: ['informado', 'sugerido'] },
        },
        required: ['nome', 'query', 'origem'],
        additionalProperties: false,
      },
    },
  },
  required: ['marca', 'categoria', 'concorrentes'],
  additionalProperties: false,
};

const SINTAXE = `Sintaxe aceita pela busca, e somente esta:
- OR entre termos alternativos. Parenteses so para agrupar termos ligados por OR.
- Aspas para frase exata: "o boticario". Palavras separadas por espaco SEM aspas exigem que todas aparecam no post, em qualquer posicao.
- Hifen antes do termo exclui: -jogo. Exclua so sentidos errados claros e poucos.
- #hashtag e @perfil funcionam como termos comuns.
- PROIBIDO usar AND, NOT, && ou &: viram palavra literal e zeram o resultado.
- ATENCAO, o erro mais comum: termos separados so por espaco significam E (todos precisam aparecer no mesmo post). Para ALTERNATIVAS use SEMPRE OR entre cada uma, inclusive entre frases, #hashtags e @perfis.
  CERTO: "havaianas" OR havaiana OR #havaianas OR @havaianas
  ERRADO (zera o resultado): "havaianas" "havaiana" #havaianas @havaianas`;

const PLAN_SYSTEM = `Voce monta buscas para a Buzzmonitor Trends (social listening: posts publicos em portugues do Brasil, ultimos 30 dias).
${SINTAXE}
Regras da marca e dos concorrentes: cubra o nome com e sem acento, junto e separado, apelido comum, @perfil oficial provavel e #hashtag quando o nome for distintivo. Se o nome for palavra comum (vivo, claro, sprite, ype, tim, oi, marisa, renner, natura), NUNCA inclua o nome solto: ancore SO em frases compostas com o segmento ("vivo fibra", "operadora vivo", "lojas renner"), @perfil e #hashtag, e exclua o sentido errado com hifen. Nao invente perfil se nao tiver seguranca: omita. Se "perfil_instagram_oficial_da_marca" vier preenchido, use exatamente esse @ na busca da marca (e nao invente outro).
O visitante informa o segmento da marca: use-o para desambiguar o nome (a marca pertence a esse segmento), para montar a categoria e para sugerir concorrentes desse mesmo segmento.
Regra da categoria: termos genericos de uso e compra do que a marca vende, como a pessoa fala (com e sem acento), SEM nomes de marcas.
Cada query com no maximo ${MAX_QUERY} caracteres.
Concorrentes: devolva primeiro todos os informados pelo visitante (origem "informado", respeitando o nome que ele digitou). Depois, se pedido, sugira candidatos (origem "sugerido"): concorrentes diretos no Brasil, mesmo mercado e porte comparavel, com conversa espontanea nas redes, sem repetir os informados.
Se nao reconhecer a marca, monte a busca so com o nome exato entre aspas e as variacoes de grafia, e devolva concorrentes sugeridos apenas se tiver seguranca do mercado.`;

// Erro classico de modelo: alternativas coladas so por espaco ("a" "b" #c @d). Na Trends espaco e E, entao o resultado
// zera. Frase entre aspas, #hashtag e @perfil seguidos um do outro viram alternativas (OR). Exclusoes (-"x") ficam como
// estao, e palavras soltas seguidas continuam sendo E (e assim que se pede co-ocorrencia de proposito).
const ATOMO = /(?:"[^"]*"|[#@][^\s()"]+)/.source;
function ligarAtomosComOr(q) {
  const re = new RegExp(`(?<![-\\w])(${ATOMO})\\s+(?=${ATOMO})`, 'g');
  let atual = q;
  for (let i = 0; i < 5; i++) { // repete: a regex nao sobrepoe casamentos vizinhos
    const proximo = atual.replace(re, '$1 OR ');
    if (proximo === atual) break;
    atual = proximo;
  }
  return atual;
}

// Converte o que a IA devolver em algo que a API aceita. Defesa em profundidade: o prompt ja proibe, mas modelo erra.
// Os operadores so sao tratados FORA de aspas: dentro de uma frase exata "melissa and doug" o AND e palavra de verdade.
// NOT vira hifen (a API aceita -termo, -"frase" e -(a OR b)); AND e & viram espaco (E implicito entre palavras).
function sanitizarQuery(q) {
  let s = String(q || '').replace(/\s+/g, ' ').trim();
  if ((s.match(/"/g) || []).length % 2 === 1) s = s.replace(/"/g, '');
  const partes = s.split(/("[^"]*")/);
  s = partes.map((parte, i) => {
    if (i % 2 === 1) return parte; // dentro de aspas: intocado
    let fora = parte;
    if (i + 1 < partes.length) fora = fora.replace(/\bNOT\s*$/i, '-'); // NOT "frase" -> -"frase"
    return fora.replace(/\bNOT\s+/gi, '-').replace(/\s+AND\s+/gi, ' ').replace(/&&|&/g, ' ');
  }).join('');
  let abre = 0;
  for (const ch of s.replace(/"[^"]*"/g, '')) { if (ch === '(') abre++; else if (ch === ')') abre--; if (abre < 0) break; }
  if (abre !== 0) s = s.split(/("[^"]*")/).map((p, i) => (i % 2 === 1 ? p : p.replace(/[()]/g, ''))).join('');
  s = s.replace(/-\s+/g, '-').replace(/\s+/g, ' ').trim();
  s = ligarAtomosComOr(s);
  return s.slice(0, MAX_QUERY);
}

// Exclusao que contradiz a propria busca (ex.: "Vivo" OR vivo ... -"vivo") apaga a marca inteira. A IA erra assim com
// nome comum, entao qualquer -termo igual a um termo positivo da mesma busca (ou contido nele) e descartado.
function removerAutoExclusoes(q) {
  const norm = (t) => String(t).replace(/^-/, '').replace(/["#@]/g, '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  const positivos = new Set();
  String(q).replace(/-"[^"]*"|-[^\s()]+/g, ' ').replace(/"[^"]*"|[^\s()]+/g, (m) => {
    if (!/^or$/i.test(m)) positivos.add(norm(m));
    return m;
  });
  // contradiz: algum termo positivo e igual ao excluido ou o CONTEM como palavras (-vivo contra "vivo fibra")
  const contradiz = (e) => [...positivos].some((p) => ` ${p} `.includes(` ${e} `));
  return (' ' + q).replace(/\s-"[^"]*"|\s-[^\s()]+/g, (m) => (contradiz(norm(m.trim())) ? '' : m)).replace(/\s+/g, ' ').trim();
}

// Modo ancora, para nome de marca que e palavra comum (vivo, claro, oi): descarta o nome solto e fica so com o que
// prende a busca na marca: @perfil, #hashtag e frases compostas entre aspas ("lojas renner"). Exclusoes sao mantidas.
// Devolve null se nao sobrar nenhuma ancora.
function soAncoras(q) {
  const exclusoes = [];
  const sem = (' ' + String(q)).replace(/\s-"[^"]*"|\s-[^\s()]+/g, (m) => { exclusoes.push(m.trim()); return ' '; });
  const ancoras = [];
  sem.replace(/"[^"]*"|[^\s()]+/g, (m) => {
    if (/^or$/i.test(m)) return m;
    if (/^[#@]/.test(m) || /^"[^"]*\s[^"]*"$/.test(m)) ancoras.push(m);
    return m;
  });
  const unicas = [...new Set(ancoras)];
  if (!unicas.length) return null;
  return [unicas.join(' OR '), ...exclusoes].join(' ').trim();
}

// Garante o @ informado pelo visitante na busca da marca, como alternativa (OR) aos termos positivos. As exclusoes (-x)
// ficam no fim, onde estavam. Se a busca ja tem o @, nao muda nada.
function comPerfil(query, handle) {
  if (!handle) return query;
  const alvo = `@${handle}`;
  if (new RegExp(`(^|[\\s(])${alvo.replace(/[.]/g, '\\.')}(?![\\w.])`, 'i').test(query)) return query;
  const exclusoes = [];
  const positivos = (' ' + String(query)).replace(/\s-"[^"]*"|\s-[^\s()]+/g, (m) => { exclusoes.push(m.trim()); return ' '; }).replace(/\s+/g, ' ').trim();
  const base = positivos ? `${positivos} OR ${alvo}` : alvo;
  return [base, ...exclusoes].join(' ').slice(0, MAX_QUERY);
}

// Busca de reserva quando a IA nao esta disponivel ou devolveu algo que a API recusou: frase exata do nome.
function queryExata(nome) {
  const limpo = String(nome || '').replace(/["()\\]/g, ' ').replace(/\s+/g, ' ').trim();
  return limpo ? `"${limpo}"` : '';
}

// --- Checagem de homonimo ---
// Nome de marca que e tambem outra coisa (Renner x a dupla Rick & Renner; Vivo, Claro, Oi...) enche a busca de posts
// de outro assunto e infla o numero. Depois da busca, a IA le uma amostra aleatoria de posts DA PROPRIA BUSCA e diz
// quantos nao falam da marca; se forem muitos, devolve a mesma busca com exclusoes e ancoras.

const REVIEW_SCHEMA = {
  type: 'object',
  properties: {
    posts_fora_do_assunto: { type: 'integer' },
    assunto_errado: { type: 'string' },
    query_corrigida: { type: 'string' },
  },
  required: ['posts_fora_do_assunto', 'assunto_errado', 'query_corrigida'],
  additionalProperties: false,
};

const REVIEW_SYSTEM = `Voce revisa uma busca de social listening feita para encontrar posts de uma MARCA. Recebe o nome da marca, o segmento dela, a busca usada e uma amostra aleatoria de posts que essa busca trouxe (texto e nome do perfil que postou).
Conte em "posts_fora_do_assunto" quantos posts da amostra NAO falam da marca do segmento informado: falam de outra pessoa, dupla, banda, personagem, lugar ou da palavra em outro sentido. Posts que citam a marca de passagem, mesmo sem ser o foco, contam como DA marca.
Em "assunto_errado" diga em poucas palavras do que falam os posts que sobraram (ex.: "dupla sertaneja Rick & Renner"). Se nao houver, deixe vazio.
Em "query_corrigida" devolva a MESMA busca com a correcao, so quando mais de 30% da amostra estiver fora do assunto: acrescente exclusoes (-termo ou -"frase") dos assuntos errados e, se preciso, troque o nome solto por frases compostas, @perfil ou #hashtag que ancorem na marca. Mantenha o que ja funcionava, mas se o nome da marca for palavra comum e a busca o traz solto, REMOVA o nome solto e deixe so as ancoras (frases compostas com o segmento, @perfil, #hashtag). NUNCA exclua (-) um termo que a propria busca inclui: isso apaga a marca. Se a busca estiver boa, deixe vazio.
${SINTAXE}
Nunca invente perfil nem hashtag: se nao tiver seguranca, prefira excluir o assunto errado.`;

// posts: [{ texto, autor }]. Devolve null (sem IA, ou amostra pequena) ou { fora, total, assunto, corrigida }.
async function revisarBusca({ nome, segmento, query, posts }) {
  if (!Array.isArray(posts) || posts.length < 8) return null;
  const resposta = await chamarJSON({
    system: REVIEW_SYSTEM,
    user: { marca: nome, segmento: segmento || null, busca_usada: query, amostra: posts },
    schema: REVIEW_SCHEMA,
    schemaName: 'revisao_da_busca',
    maxTokens: 500,
    timeoutMs: 15000,
    temperature: 0,
  });
  if (!resposta) return null;
  const total = posts.length;
  const fora = Math.max(0, Math.min(total, Number(resposta.posts_fora_do_assunto) || 0));
  const nova = removerAutoExclusoes(sanitizarQuery(resposta.query_corrigida));
  const corrigir = fora / total >= 0.3 && nova && nova !== query;
  return { fora, total, problema: fora / total >= 0.3, assunto: String(resposta.assunto_errado || '').slice(0, 120), corrigida: corrigir ? nova : null };
}

// Sem IA, a categoria vira as palavras do segmento ligadas por OR ("Cosmeticos e Beleza" -> Cosmeticos OR Beleza).
function categoriaPeloSegmento(segmento) {
  const palavras = String(segmento || '').split(/[^\p{L}\p{N}]+/u).filter((p) => p.length >= 4);
  if (!palavras.length) return null;
  return { nome: segmento, query: sanitizarQuery(palavras.join(' OR ')) };
}

async function planejarBuscas({ marca, segmento, informados, instagram }) {
  const faltam = Math.max(0, 3 - informados.length);
  const pedido = {
    marca_digitada: marca,
    segmento_da_marca: segmento || null,
    perfil_instagram_oficial_da_marca: instagram ? `@${instagram}` : null,
    concorrentes_informados: informados,
    sugerir_quantos_candidatos: faltam > 0 ? faltam + 2 : 0,
  };
  const plano = await chamarJSON({
    system: PLAN_SYSTEM,
    user: pedido,
    schema: PLAN_SCHEMA,
    schemaName: 'plano_de_buscas',
    maxTokens: 1100,
    timeoutMs: 20000,
    temperature: 0.2,
  });

  const informadosNorm = informados.map((n) => n.toLowerCase());
  const doPlano = plano && Array.isArray(plano.concorrentes) ? plano.concorrentes : [];

  // Informados sempre entram, com a query da IA quando existir e a busca exata como reserva.
  const concorrentes = informados.map((nome) => {
    const achado = doPlano.find((c) => c.origem === 'informado' && String(c.nome || '').toLowerCase() === nome.toLowerCase())
      || doPlano.find((c) => String(c.nome || '').toLowerCase().includes(nome.toLowerCase()));
    return { nome, query: sanitizarQuery(achado && achado.query) || queryExata(nome), origem: 'informado' };
  });
  const sugeridos = doPlano
    .filter((c) => c.origem === 'sugerido' && c.nome && !informadosNorm.includes(String(c.nome).toLowerCase()))
    .map((c) => ({ nome: String(c.nome).slice(0, 60), query: sanitizarQuery(c.query) || queryExata(c.nome), origem: 'sugerido' }))
    .filter((c) => c.query);

  return {
    iaDisponivel: Boolean(plano),
    marca: {
      nome: (plano && plano.marca && plano.marca.nome_exibicao) || marca,
      query: comPerfil(sanitizarQuery(plano && plano.marca && plano.marca.query) || queryExata(marca), instagram),
    },
    categoria: plano && plano.categoria && sanitizarQuery(plano.categoria.query)
      ? { nome: plano.categoria.nome, query: sanitizarQuery(plano.categoria.query) }
      : categoriaPeloSegmento(segmento),
    informados: concorrentes,
    sugeridos,
  };
}

module.exports = { planejarBuscas, revisarBusca, sanitizarQuery, removerAutoExclusoes, soAncoras, queryExata, categoriaPeloSegmento, comPerfil };
