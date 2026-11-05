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

const SINTAXE = `Sintaxis aceptada por la búsqueda, y solo esta:
- OR entre términos alternativos. Paréntesis solo para agrupar términos unidos por OR.
- Comillas para frase exacta: "palacio de hierro". Palabras separadas por espacio SIN comillas exigen que todas aparezcan en el post, en cualquier posición.
- Guion antes del término lo excluye: -futbol. Excluye solo sentidos equivocados claros y pocos.
- #hashtag y @perfil funcionan como términos comunes.
- PROHIBIDO usar AND, NOT, && o &: se vuelven palabra literal y dejan el resultado en cero.
- ATENCIÓN, el error más común: términos separados solo por espacio significan Y (todos tienen que aparecer en el mismo post). Para ALTERNATIVAS usa SIEMPRE OR entre cada una, también entre frases, #hashtags y @perfiles.
  CORRECTO: "bimbo" OR "grupo bimbo" OR #bimbo OR @grupobimbo
  INCORRECTO (deja el resultado en cero): "bimbo" "grupo bimbo" #bimbo @grupobimbo`;

const PLAN_SYSTEM = `Armas búsquedas para Buzzmonitor Trends (social listening: posts públicos en español de México y del resto de América Latina, últimos 30 días).
${SINTAXE}
Reglas de la marca y de los competidores: cubre el nombre con y sin acento, junto y separado, apodo común, @perfil oficial probable y #hashtag cuando el nombre sea distintivo. Si el nombre es una palabra común (corona, modelo, victoria, liverpool, claro, sol, estrella, vivo, total)), NUNCA incluyas el nombre suelto: ánclalo SOLO en frases compuestas con el segmento ("cerveza corona", "tienda liverpool", "claro internet"), @perfil y #hashtag, y excluye el sentido equivocado con guion. No inventes perfiles si no tienes seguridad: omítelos. Si "perfil_instagram_oficial_da_marca" viene lleno, usa exactamente ese @ en la búsqueda de la marca (y no inventes otro).
El visitante indica el segmento de la marca: úsalo para desambiguar el nombre (la marca pertenece a ese segmento), para armar la categoría y para sugerir competidores de ese mismo segmento.
Regla de la categoría: términos genéricos de uso y compra de lo que vende la marca, como lo dice la gente en México y América Latina (con y sin acento), SIN nombres de marcas.
Cada query con un máximo de ${MAX_QUERY} caracteres.
Competidores: devuelve primero todos los que indicó el visitante (origem "informado", respetando el nombre que escribió). Después, si se pide, sugiere candidatos (origem "sugerido"): competidores directos en México (o en América Latina, si la marca no opera en México), mismo mercado y tamaño comparable, con conversación espontánea en redes, sin repetir los indicados.
Si no reconoces la marca, arma la búsqueda solo con el nombre exacto entre comillas y sus variantes de escritura, y devuelve competidores sugeridos solo si tienes seguridad del mercado.`;

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

const REVIEW_SYSTEM = `Revisas una búsqueda de social listening hecha para encontrar posts de una MARCA. Recibes el nombre de la marca, su segmento, la búsqueda usada y una muestra aleatoria de posts que trajo esa búsqueda (texto y nombre del perfil que publicó). Los posts están en español.
Cuenta en "posts_fora_do_assunto" cuántos posts de la muestra NO hablan de la marca del segmento indicado: hablan de otra persona, grupo musical, personaje, lugar o de la palabra con otro sentido. Los posts que mencionan la marca de pasada, aunque no sea el foco, cuentan como DE la marca.
En "assunto_errado" di en pocas palabras de qué hablan los posts que sobran (ej.: "equipo de futbol Liverpool"). Si no hay, déjalo vacío.
En "query_corrigida" devuelve la MISMA búsqueda corregida, solo cuando más del 30% de la muestra esté fuera de tema: agrega exclusiones (-término o -"frase") de los temas equivocados y, si hace falta, cambia el nombre suelto por frases compuestas, @perfil o #hashtag que la anclen a la marca. Conserva lo que ya funcionaba, pero si el nombre de la marca es una palabra común y la búsqueda lo trae suelto, QUITA el nombre suelto y deja solo las anclas (frases compuestas con el segmento, @perfil, #hashtag). NUNCA excluyas (-) un término que la propia búsqueda incluye: eso borra la marca. Si la búsqueda está bien, déjalo vacío.
${SINTAXE}
Nunca inventes perfiles ni hashtags: si no tienes seguridad, mejor excluye el tema equivocado.`;

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
