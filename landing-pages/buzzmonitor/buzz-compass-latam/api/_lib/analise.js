// Pipeline do totem: marca + concorrentes -> buscas (skill /buscas, ver buscas.js) -> Trends -> scores deterministicos
// -> narrativa por IA. Os numeros nunca vem da IA: ela so escreve texto em cima do que foi calculado aqui.
// O Compass Score e da MARCA (api/_lib/score.js, documentado em SCORING.md); o segmento aparece nos graficos e nos cards.

const { fusoAtual, comFuso, normalize, fetchWithTimeout, bmDate, bmVolume, bmPosts, bmInfluencers, bmPerfilInstagram, emLote } = require('./trends');
const { chamarJSON } = require('./llm');
const { planejarBuscas, revisarBusca, soAncoras, queryExata, categoriaPeloSegmento } = require('./buscas');
const { scoreDaMarca, crescimentoPct } = require('./score');
const { dadosDoPais, fusoHoras } = require('./paises');

// --- Utilidades de dado ---

const semAcento = (s) => String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

function contarSentimento(data) {
  const arr = Array.isArray(data) ? data : [];
  const pega = (l) => arr.find((d) => d.label === l)?.value || 0;
  const positivos = pega('positive');
  const neutros = pega('neutral');
  const negativos = pega('negative');
  return { positivos, neutros, negativos, total: positivos + neutros + negativos };
}

// 30 dias corridos no fuso do pais da analise (padrao -6, Cidade do Mexico; ver trends.js comFuso), na mesma ordem para todos os grupos (barra comparar linha com linha).
function chavesDosDias() {
  const chaves = [];
  for (let i = 29; i >= 0; i--) {
    const d = new Date(Date.now() + fusoAtual() * 3600e3 - i * 86400e3);
    chaves.push(`${d.getUTCFullYear()}${String(d.getUTCMonth() + 1).padStart(2, '0')}${String(d.getUTCDate()).padStart(2, '0')}`);
  }
  return chaves;
}

function serieAlinhada(dailyData) {
  const porDia = new Map((Array.isArray(dailyData) ? dailyData : []).map((d) => [String(d.label).slice(0, 8), d.value || 0]));
  return chavesDosDias().map((k) => porDia.get(k) || 0);
}

// O proprio nome da marca domina a nuvem de palavras e nao diz nada: tira o que veio da busca.
function tokensDaBusca(nome, query) {
  const base = `${nome} ${String(query || '').replace(/-"[^"]*"|-\S+/g, ' ').replace(/\bOR\b/g, ' ')}`;
  return new Set(
    semAcento(base).replace(/[#@"()]/g, ' ').split(/\s+/).filter((t) => t.length >= 3)
  );
}

// Palavras de rede social e de venda que aparecem em todo post e nao dizem nada sobre o assunto ("link na bio").
// Versao LATAM: o mesmo filtro com o vocabulario de rede social e de venda em espanhol.
const RUIDO = new Set(['link', 'bio', 'whatsapp', 'dm', 'direct', 'clic', 'click', 'aqui', 'perfil', 'sigue', 'siguenos', 'comenta', 'comparte',
  'aprovecha', 'descubre', 'conoce', 'dejar', 'gente', 'mundo', 'hoy', 'ahora', 'todos', 'todas', 'todo', 'aun', 'hacer', 'tener',
  'cosa', 'vida', 'dia', 'dias', 'nuevo', 'nueva', 'mas', 'muy', 'mucho', 'para', 'pero', 'porque', 'esta', 'este', 'esto', 'como',
  'cuando', 'donde', 'tambien', 'solo', 'asi', 'bien', 'vez', 'ser', 'hay', 'sus', 'les', 'del', 'los', 'las', 'una', 'uno', 'que',
  'tus', 'mis', 'personas', 'gente', 'ano', 'anos', 'semana', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto',
  'septiembre', 'octubre', 'noviembre', 'diciembre', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo',
  'mercado', 'cualquier', 'especial', 'tienda', 'sitio', 'web', 'instagram', 'facebook', 'twitter', 'video', 'foto', 'post', 'live']);

function limparTermos(termos, nome, query) {
  const tokens = tokensDaBusca(nome, query);
  // numero solto (ano, data) tambem nao diz nada sobre o assunto
  return (termos || []).filter((t) => !tokens.has(semAcento(t.label)) && !RUIDO.has(semAcento(t.label)) && !/^\d+$/.test(String(t.label).trim()));
}

function termosEmergentes(primeira, segunda, nome, query) {
  const antes = new Map((primeira || []).map((t) => [t.label, t.value]));
  const lista = limparTermos(segunda, nome, query)
    .filter((t) => t.value >= 15)
    .map((t) => {
      const a = antes.get(t.label) || 0;
      return { label: t.label, crescimento: a === 0 ? Infinity : (t.value - a) / a };
    })
    .filter((t) => t.crescimento > 0.3 || t.crescimento === Infinity)
    .sort((a, b) => b.crescimento - a.crescimento)
    .slice(0, 8)
    .map((t) => t.label);
  return lista;
}

// --- Narrativa ---
// Uma leitura so, do MERCADO (a marca e os concorrentes estao dentro dele). Quatro cards de texto com insight pronto:
// oportunidade, risco, tendencia emergente e concorrentes. Os graficos ficam na secao de numeros, nunca dentro dos cards.

// Cada card tem dois paragrafos com escopo explicito: "segmento" (o mercado) e "marca" (a marca em foco).
const CARD = {
  type: 'object',
  properties: { titulo: { type: 'string' }, segmento: { type: 'string' }, marca: { type: 'string' } },
  required: ['titulo', 'segmento', 'marca'],
  additionalProperties: false,
};

const TEMA = {
  type: 'object',
  properties: {
    tema: { type: 'string' },
    sentimento: { type: 'string', enum: ['positivo', 'negativo', 'neutro'] },
    onde: { type: 'string', enum: ['marca', 'concorrente', 'mercado'] },
    evidencia: { type: 'string' },
    posts_na_amostra: { type: 'integer' },
  },
  required: ['tema', 'sentimento', 'onde', 'evidencia', 'posts_na_amostra'],
  additionalProperties: false,
};

// "temas" vem primeiro de proposito: a IA lista o que aparece de verdade nos posts antes de escrever os cards, o que
// ancora o texto na evidencia. Nao vai para a tela.
const NARRATIVE_SCHEMA = {
  type: 'object',
  properties: {
    temas: { type: 'array', items: TEMA },
    oportunidade: CARD,
    risco: CARD,
    tendencia_emergente: CARD,
    concorrentes: CARD,
  },
  required: ['temas', 'oportunidade', 'risco', 'tendencia_emergente', 'concorrentes'],
  additionalProperties: false,
};

const NARRATIVE_SYSTEM = `Eres la analista de inteligencia de mercado detrás de Buzz Compass, una herramienta de Buzzmonitor. Estás leyendo el resultado de una persona que acaba de correr el Buzz Compass de su propia marca en un tótem, durante un evento en América Latina.
Tono de voz: profesional, accesible, basado en datos, con energía y claridad. Tutea siempre ("tu marca"), nunca "usted" ni "vosotros". Nunca uses "revolucionario", "disruptivo" ni hype vacío. Nunca sugieras que la inteligencia artificial reemplaza a las personas. Nunca uses la palabra "momentum".
Recibes: "marca_em_foco", el "segmento", la lectura del "mercado" (toda la conversación del segmento, con la marca y los competidores adentro), los "fatos" ya comparados y la "comparacao" de cada marca con ejemplos reales de posts positivos y negativos. Los posts están en español (México, el resto de América Latina y también España). La base es limitada (proyectos que ya monitorean clientes de Buzzmonitor), no es todo internet en tiempo real.
Si viene "pais", la persona eligió ese país: las búsquedas y los competidores se armaron para ese mercado y puedes nombrar el país, pero Trends no filtra los posts por ubicación (entra conversación en español de toda la región), así que NUNCA digas que los números son solo de ese país ni "en México"/"en Colombia" como si fuera un conteo por país.

CÓMO TRABAJAR, en este orden:
1) Llena "temas" PRIMERO. Lee los "exemplos_positivos" y "exemplos_negativos" de cada marca y del mercado y lista de 4 a 8 temas CONCRETOS que de verdad aparecen en esos posts (ej.: "cupón de descuento en la tienda en línea", "lanzamiento de una nueva línea de producto", "queja por retraso en la entrega"). Para cada uno: sentimiento, dónde aparece (marca, competidor o mercado), "evidencia" (fragmento corto del ejemplo) y "posts_na_amostra" (cuántos ejemplos tratan de eso). Ignora el post que no habla del segmento ni de la marca (noticia aleatoria, otro asunto). Solo lista temas que existen en los ejemplos: nunca inventes.
2) Escribe las 4 tarjetas a partir de los temas y de los números.

REGLAS DE NÚMEROS (la IA ya se equivocó y dijo que 30 mil era menos que 17 mil):
- Usa solo números del payload, copiados. NO sumes, restes, redondees ni compares números por tu cuenta.
- Ranking, líder, mayor crecimiento, mayor porcentaje positivo y mayor porcentaje de quejas: usa SOLO el campo "fatos".
- Usa "volume_30d_formatado" tal cual viene (ej.: 30,083).
- "crescimento_ultimos_7_dias_vs_7_anteriores_pct" compara la última semana con la anterior: nunca digas "en los últimos 30 días". "variacao_do_percentual_positivo_entre_quinzenas_em_pontos" es del MERCADO completo, en puntos porcentuales; nunca se lo atribuyas a una marca ni lo escribas como %.
- "percentual_com_linguagem_de_reclamacao" y "..._de_elogio" miden qué parte de las menciones de la marca usa vocabulario de queja o de elogio; "composicao_da_amostra_aleatoria" muestra cuántos posts de la muestra son positivos, neutros y negativos.

LO QUE SE ESPERA DE CADA TARJETA. Cada tarjeta tiene tres campos: "titulo" (hasta 6 palabras), "segmento" y "marca".
- "segmento" habla del MERCADO del segmento: toda la conversación (temas, términos, sentimiento, formatos y competidores). "marca" habla SOLO de la marca en foco: su evidencia (porcentajes, ejemplos, posición) y cierra con una acción concreta. Cada campo tiene de 2 a 3 frases y al menos un número real; los números del segmento van en "segmento" y los de la marca en "marca", sin mezclarlos.
- oportunidade: "segmento" = 2 o 3 temas positivos CONCRETOS que hoy generan conversación favorable, con el número que los respalda. "marca" = cómo aparece la marca en esos temas (o si todavía no aparece, y ese es el espacio por ocupar) y la acción ligada a ellos (qué tema, formato o canal).
- risco: "segmento" = los temas negativos CONCRETOS del mercado (lo que molesta, lo que sale mal), con un ejemplo parafraseado; si la crítica en la muestra es poca, DILO con los números en lugar de inventar un riesgo. "marca" = las quejas de la propia marca (sus exemplos_negativos y el porcentaje con lenguaje de queja) y qué hacer; si son pocas, di el número.
- tendencia_emergente: "segmento" = lo que es nuevo en la conversación ("termos_emergentes_2a_quinzena") y el formato que mejor funciona ("conteudos_que_performaram_bem"); si no hay término emergente, di que es el retrato del mes completo. "marca" = su ritmo y lo que eso le pide.
- concorrentes: "segmento" = cómo están los competidores en el segmento, usando "fatos" y los ejemplos de cada uno: quién lidera, quién tiene la conversación más positiva, quién crece más, quién recibe más quejas y qué elogia o critica la gente de cada competidor (tema concreto). Menciona al menos dos competidores por nombre. "marca" = dónde está la marca frente a ellos (posición, participación, reputación, crecimiento) y una acción. Si "concorrentes_sugeridos" es true, di en una frase que parte de los competidores la eligió Buzzmonitor según el mercado de la marca. Si una marca tiene "busca_incerta" en true, su nombre es común: avísalo y no saques conclusiones fuertes.
- Marca con poca conversación: presenta el número real como ESPACIO POR OCUPAR. NUNCA uses las expresiones "datos insuficientes", "sin datos", "datos limitados" ni "aparece poco en la base". Las marcas en "marcas_pequenas_demais_para_comparar" (menos de 50 menciones) todavía tienen poca conversación en el periodo: no compares sus porcentajes.

PROHIBIDO: frases vacías como "es importante monitorear", "participar más en las conversaciones" o "fortalecer la imagen" sin decir CON QUÉ (qué tema, formato o canal). Toda recomendación apunta a algo que apareció en la evidencia. Nunca mandes a ver una gráfica, nube o tabla. NUNCA cites el nombre de una persona, perfil o página que aparezca en los ejemplos de posts; los nombres de las marcas de la comparación sí se pueden citar. Si "dados_parciais" es true, sé más cauteloso.
Escribe en español de México, natural y directo, como lo diría una analista mexicana: "celular" (nunca "móvil"), "reporte" (nunca "informe"), "monitoreo" (nunca "monitorización"), "clientes potenciales" en vez de "leads". Sin clichés, sin em-dash (—), sin fórmulas del tipo "no es X, es Y", sin "Cabe mencionar", "Vale la pena destacar" ni "En resumen". Números en formato mexicano: la coma separa miles (40,459 y 2,391) y el punto separa decimales (2.4%). Título de hasta 6 palabras.`;

// Versao LATAM: a tela e em espanhol do Mexico, onde a virgula separa milhar (40,459) e o ponto separa decimal (2.4%).
// A IA as vezes escreve sem separador ("40459") ou no estilo europeu ("40.459", "2,4%"). A correcao e feita aqui, no texto
// pronto, porque so o prompt nao garante.
// - milhar com ponto (40.459, 1.234.567) vira virgula;
// - decimal com virgula seguido de % (2,4%) vira ponto;
// - inteiro de 4+ digitos sem separador ganha a virgula de milhar, EXCETO ano (1900 a 2100) que nao e seguido de contagem
//   ("en 2026"); "2391 menciones" continua sendo numero.
const CONTAGEM = /^\s*(menciones|posts|publicaciones|perfiles|seguidores|likes|me gusta|comentarios|compartidos|veces|personas|resultados|%)/i;
function formatarNumerosEsMx(texto) {
  if (typeof texto !== 'string') return texto;
  return texto
    .replace(/(?<![\d.,])(\d{1,3}(?:\.\d{3})+)(?![\d.,]\d)/g, (m) => m.replace(/\./g, ','))
    .replace(/(?<![\d.,])(\d+),(\d{1,2})(?=\s?%)/g, '$1.$2')
    .replace(/(?<![\d.,])(\d{4,})(?![\d])(?!\.\d)(?!,\d)/g, (m, num, pos, todo) => {
      const n = Number(num);
      const resto = todo.slice(pos + m.length);
      if (n >= 1900 && n <= 2100 && !CONTAGEM.test(resto)) return m; // ano
      return num.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    });
}
function formatarTextosEsMx(obj) {
  if (typeof obj === 'string') return formatarNumerosEsMx(obj);
  if (Array.isArray(obj)) return obj.map(formatarTextosEsMx);
  if (obj && typeof obj === 'object') {
    const novo = {};
    Object.keys(obj).forEach((k) => { novo[k] = formatarTextosEsMx(obj[k]); });
    return novo;
  }
  return obj;
}

// --- Insights sem IA: texto montado so com o que a Trends devolveu (mesma regra: nada inventado, nada de "veja o grafico") ---

const VOLUME_MINIMO_COMPARAR = 50;
// A Trends devolve o tipo do post em ingles (photo, video, link...): na tela vai em espanhol.
const FORMATOS = { photo: 'foto', image: 'imagen', video: 'video', reel: 'reel', link: 'enlace', text: 'texto', status: 'texto', carousel: 'carrusel', album: 'carrusel', story: 'historia' };
const nomeDoFormato = (t) => FORMATOS[String(t || '').toLowerCase()] || String(t || '').toLowerCase();
const fmtN = (n) => Number(n || 0).toLocaleString('es-MX');
const lista = (itens) => (itens.length <= 1 ? itens.join('') : `${itens.slice(0, -1).join(', ')} y ${itens[itens.length - 1]}`);
const citar = (t, max = 120) => {
  const s = String(t || '').replace(/\s+/g, ' ').trim();
  return s.length > max ? `${s.slice(0, max - 1).trim()}…` : s;
};

function narrativaPorDados({ marca, segmento, mercado, comparacao, sugeridos }) {
  const pos = mercado.sent.positivos;
  const neg = mercado.sent.negativos;
  const comPolaridade = pos + neg;
  const pctP = comPolaridade ? Math.round((pos / comPolaridade) * 100) : null;
  const top = mercado.termos.slice(0, 3).map((t) => t.label);
  const ritmo = crescimentoPct(mercado.serie);
  const eu = comparacao.find((g) => g.tipo === 'marca');
  const concs = comparacao.filter((g) => g.tipo === 'concorrente');
  const euComVolume = eu && eu.volume >= VOLUME_MINIMO_COMPARAR;

  const oportunidade = {
    titulo: 'Temas que generan conversación positiva',
    segmento: `${pctP !== null ? `El ${pctP}% de los posts con polaridad en el sector de ${segmento} son positivos (${fmtN(pos)} de ${fmtN(comPolaridade)}). ` : `El sector de ${segmento} sumó ${fmtN(mercado.sent.total)} menciones en 30 días. `}` +
      `${top.length ? `Los términos más mencionados son ${lista(top)}. ` : ''}` +
      `${mercado.positivos[0] ? `Uno de los posts positivos de la muestra dice: “${citar(mercado.positivos[0].resumo)}”.` : ''}`.trim(),
    marca: `${euComVolume && eu.pct_positivo !== null ? `El ${eu.pct_positivo}% de los posts de ${marca} con polaridad son positivos. ` : `${marca} todavía tiene poca conversación en el periodo, y eso deja un espacio por ocupar. `}` +
      `El contenido de ${marca} que entre en estos temas llega a una conversación que ya es favorable.`,
  };

  const queda = mercado.tendenciaSentimento;
  const risco = {
    titulo: 'Temas que generan conversación negativa',
    segmento: `${comPolaridade ? `El ${100 - pctP}% de los posts con polaridad en el sector son negativos (${fmtN(neg)}). ` : ''}` +
      `${queda !== null ? (queda === 0 ? 'El porcentaje de posts positivos se mantuvo igual de la primera a la segunda quincena. ' : `El porcentaje de posts positivos ${queda < 0 ? 'bajó' : 'subió'} ${Math.abs(queda)} puntos de la primera a la segunda quincena. `) : ''}` +
      `${mercado.negativos[0] ? `Uno de los posts negativos de la muestra dice: “${citar(mercado.negativos[0].resumo)}”.` : ''}`.trim(),
    marca: `${eu && eu.reclamacao_pct != null ? `El ${eu.reclamacao_pct}% de las menciones de ${marca} usa lenguaje de queja. ` : ''}` +
      `${eu ? `${marca} tiene el ${eu.share_pct}% de la conversación entre las marcas comparadas, así que estos temas le llegan en una proporción parecida. ` : ''}` +
      `Conviene seguir estos temas de cerca antes de que crezcan.`,
  };

  const emerg = mercado.emergentes.slice(0, 5);
  const tendencia = {
    titulo: emerg.length ? 'Lo que crece en la conversación' : 'Lo que más aparece en la conversación',
    segmento: `${emerg.length ? `Los términos que más crecieron de la primera a la segunda quincena son ${lista(emerg)}. ` : `Ningún término nuevo destacó entre una quincena y otra. El retrato del mes trae ${lista(top)}. `}` +
      `${ritmo !== null ? `El volumen diario del sector ${ritmo >= 0 ? 'subió' : 'bajó'} ${Math.abs(ritmo)}% en la última semana frente a la anterior. ` : ''}` +
      `${mercado.destaques[0] && mercado.destaques[0].tipo ? `Entre los posts de mayor alcance, el formato que predomina es ${nomeDoFormato(mercado.destaques[0].tipo)}.` : ''}`.trim(),
    marca: `${euComVolume && eu.crescimento_pct !== null ? `${marca} ${eu.crescimento_pct >= 0 ? 'creció' : 'bajó'} ${Math.abs(eu.crescimento_pct)}% en la última semana frente a la anterior. ` : ''}` +
      `Quien llegue primero a estos temas le habla a una audiencia que se está moviendo.`,
  };

  // Marca com menos de VOLUME_MINIMO_COMPARAR mencoes: percentual e crescimento dela enganam, entao nao entram no ranking.
  const comparaveis = comparacao.filter((g) => g.volume >= VOLUME_MINIMO_COMPARAR);
  const pequenos = concs.filter((g) => g.volume < VOLUME_MINIMO_COMPARAR);
  const lider = comparacao.slice().sort((a, b) => b.volume - a.volume)[0];
  const maisPositivo = comparaveis.filter((g) => g.pct_positivo !== null).sort((a, b) => b.pct_positivo - a.pct_positivo)[0];
  const maisCresce = comparaveis.filter((g) => g.crescimento_pct !== null).sort((a, b) => b.crescimento_pct - a.crescimento_pct)[0];
  const concorrentes = {
    titulo: 'Cómo se posiciona tu marca',
    segmento: `${lider ? `${lider.rotulo} lidera la conversación con el ${lider.share_pct}% (${fmtN(lider.volume)} menciones). ` : ''}` +
      `${maisPositivo ? `La conversación más positiva es la de ${maisPositivo.rotulo}, con ${maisPositivo.pct_positivo}% de posts positivos. ` : ''}` +
      `${maisCresce ? `La que más crece en la última semana es ${maisCresce.rotulo}, con ${maisCresce.crescimento_pct >= 0 ? '+' : ''}${maisCresce.crescimento_pct}%. ` : ''}` +
      `${pequenos.length ? `${lista(pequenos.map((g) => g.rotulo))} ${pequenos.length > 1 ? 'tienen' : 'tiene'} poca conversación en el periodo (menos de ${VOLUME_MINIMO_COMPARAR} menciones), por eso su ritmo y su sentimiento quedan fuera de la comparación. ` : ''}` +
      `${concs.length && sugeridos ? 'Parte de los competidores la eligió Buzzmonitor según el mercado de la marca.' : ''}`.trim(),
    marca: `${eu && lider && lider !== eu ? `${marca} tiene el ${eu.share_pct}% de la conversación (${fmtN(eu.volume)} menciones) contra el ${lider.share_pct}% de ${lider.rotulo}: esa distancia es el espacio que ${marca} todavía puede ocupar.` : `${marca} lidera la conversación, y el reto es mantener la ventaja.`}`,
  };
  return { oportunidade, risco, tendencia_emergente: tendencia, concorrentes };
}

// --- Coleta e leitura de um grupo (o mercado e lido com as mesmas chamadas e as mesmas contas da LP original) ---

const N_TAREFAS_MERCADO = 10;

function tarefasDoMercado(query, sinceStr, untilStr, meioStr) {
  return [
    () => bmVolume(query, 'service', sinceStr, untilStr),
    () => bmVolume(query, 'period_daily', sinceStr, untilStr),
    () => bmVolume(query, 'term', sinceStr, untilStr),
    // top posts: o que exibir e de onde sai o formato que performa. A API devolve ~30 e nao filtra por sentimento.
    () => bmPosts(query, sinceStr, untilStr, 50, 'top_posts_field'),
    () => bmVolume(query, 'sentiment', sinceStr, meioStr),
    () => bmVolume(query, 'sentiment', meioStr, untilStr),
    () => bmVolume(query, 'term', sinceStr, meioStr),
    () => bmVolume(query, 'term', meioStr, untilStr),
    () => bmVolume(query, 'gender', sinceStr, untilStr),
    // amostra aleatoria (como a skill de buscas): de onde saem os temas de oportunidade e de risco
    () => bmPosts(query, sinceStr, untilStr, 50, 'random'),
  ];
}

const pctPos = (s) => (s.positivos + s.negativos === 0 ? null : Math.round((s.positivos / (s.positivos + s.negativos)) * 100));

const composicao = (posts) => {
  const c = { positivos: 0, neutros: 0, negativos: 0, total: posts.length };
  posts.forEach((p) => {
    const s = String(p.sentiment || '').toUpperCase();
    if (s === 'POSITIVE') c.positivos++; else if (s === 'NEGATIVE') c.negativos++; else c.neutros++;
  });
  return c;
};

const resumoPost = (p) => ({ tipo: p.content_type || p.type || null, resumo: normalize(p.text || p.content || '', 240) });
const postsDe = (res) => (res ? (res.posts || res.data || []) : []);
const porSentimento = (posts, alvo, n) => posts
  .filter((p) => String(p.sentiment || '').toUpperCase() === alvo)
  .map(resumoPost).filter((p) => p.resumo).slice(0, n);

function interpretarMercado(resultados, sent, nome, query) {
  const v = (i) => (resultados[i] && resultados[i].ok ? resultados[i].value : null);
  const [serviceRes, dailyRes, termsRes, topRes, sent1Res, sent2Res, termos1Res, termos2Res, genderRes, amostraRes] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map(v);

  const serie = serieAlinhada(dailyRes && dailyRes.data);
  const termos = limparTermos((termsRes && termsRes.data) || [], nome, query).slice().sort((a, b) => b.value - a.value).slice(0, 20);
  const s1 = sent1Res ? pctPos(contarSentimento(sent1Res.data)) : null;
  const s2 = sent2Res ? pctPos(contarSentimento(sent2Res.data)) : null;

  const top = postsDe(topRes);
  const amostra = postsDe(amostraRes);
  // Sem nome de autor nos dados da IA de proposito: ela fala de tema e formato, nunca de quem postou.
  const destaques = top.slice(0, 5)
    .map((p) => ({ tipo: p.content_type || p.type || null, curtidas: p.likes || 0, compartilhamentos: p.shares || 0, resumo: normalize(p.text || p.content || '', 140) }))
    .filter((p) => p.resumo);
  const posts = top.slice(0, 3).map((p) => {
    const curtidas = p.likes || 0;
    const compartilhamentos = p.shares || 0;
    const comentarios = p.comments_amounts || 0;
    return {
      texto: normalize(p.text || p.content || '', 260),
      rede: p.service || null,
      autor: normalize(p.author && p.author.name, 80) || null,
      link: p.link || p.url || null,
      data: p.date || null,
      curtidas, compartilhamentos, comentarios,
      interacoes: curtidas + compartilhamentos + comentarios,
    };
  }).filter((p) => p.texto);

  // Temas: da amostra aleatoria (representativa); se ela falhar, dos top posts.
  const base = amostra.length ? amostra : top;
  return {
    sent, serie, termos,
    emergentes: termosEmergentes(termos1Res && termos1Res.data, termos2Res && termos2Res.data, nome, query),
    tendenciaSentimento: s1 !== null && s2 !== null ? s2 - s1 : null,
    canais: serviceRes ? serviceRes.data || [] : [],
    genero: genderRes ? genderRes.data || [] : [],
    negativos: porSentimento(base, 'NEGATIVE', 5),
    positivos: porSentimento(base, 'POSITIVE', 5),
    composicaoAmostra: composicao(base),
    destaques, posts,
    parcial: [serviceRes, dailyRes, termsRes, topRes].some((r) => !r),
  };
}

function paraIAMercado(info, nome) {
  return {
    segmento: nome,
    volume_30d: info.sent.total,
    sentimento: { positivos: info.sent.positivos, neutros: info.sent.neutros, negativos: info.sent.negativos },
    crescimento_ultimos_7_dias_vs_7_anteriores_pct: crescimentoPct(info.serie),
    variacao_do_percentual_positivo_entre_quinzenas_em_pontos: info.tendenciaSentimento,
    composicao_da_amostra_aleatoria: info.composicaoAmostra,
    termos_mais_citados: info.termos.slice(0, 12).map((t) => t.label),
    termos_emergentes_2a_quinzena: info.emergentes,
    conteudos_que_performaram_bem: info.destaques,
    exemplos_conteudo_negativo: info.negativos,
    exemplos_conteudo_positivo: info.positivos,
  };
}

// Influenciadores: a busca so entende uma palavra; tenta as palavras do segmento ate achar perfis, sem repetir marcas da comparacao.
function palavrasDoSegmento(segmento) {
  return String(segmento || '').split(/[^\p{L}\p{N}]+/u).filter((p) => p.length >= 4 && !/^(para|como|mas|más|sobre|entre|otros|otras)$/i.test(p)).slice(0, 2);
}

// Posts da marca para mostrar na tela: Instagram, Facebook, X e sites, que falem da marca (palavra inteira no texto ou no
// nome de quem postou), os mais engajados primeiro. Quem fala DE fora vem antes; o perfil da propria marca completa a lista.
// Instagram e Facebook viram quadro oficial da rede; X e sites viram cartao de texto (com a imagem, se houver).
// Ate 6 posts, com pelo menos um de cada rede quando houver.
const MAX_POSTS_DA_MARCA = 6;
const MAX_POR_REDE = 2;

// A rede vem do ENDERECO do post (o campo "service" varia: sites chegam como blogs, news...). Perfil e pagina que nao sao
// um post (instagram.com/marca) nao contam.
function redeDoLink(link) {
  let u;
  try { u = new URL(String(link || '')); } catch (e) { return null; }
  if (!/^https?:$/.test(u.protocol)) return null;
  const host = u.hostname.replace(/^(www|m|mobile)\./, '').toLowerCase();
  if (host === 'instagram.com') return /^\/(p|reel|tv)\/[\w-]+/i.test(u.pathname) ? 'instagram' : null;
  if (host === 'facebook.com') return u.protocol === 'https:' && u.pathname.length > 1 ? 'facebook' : null;
  if (host === 'twitter.com' || host === 'x.com') return /\/status(es)?\/\d+/.test(u.pathname) ? 'x' : null;
  return /\./.test(host) ? 'site' : null;
}

function candidatosDaMarca(resultados, ficha) {
  const re = ficha ? new RegExp(`(^|[^a-z0-9])${ficha}([^a-z0-9]|$)`) : null;
  const doAutor = (p) => (re ? re.test(semAcento((p.author && p.author.name) || '')) : false);
  const mencionaMarca = (p) => !re || re.test(semAcento(`${p.text || p.content || ''} ${(p.author && p.author.name) || ''}`));
  const semUrl = (t) => String(t || '').replace(/https?:\/\/\S+/g, '').replace(/\s+/g, ' ').trim();
  const porRede = resultados.map((r) => (r && r.ok && r.value ? postsDe(r.value) : [])
    .map((p) => ({ p, link: String(p.link || p.url || '') }))
    .map(({ p, link }) => ({ p, link, rede: redeDoLink(link) }))
    .filter(({ p, rede }) => rede && mencionaMarca(p))
    .map(({ p, link, rede }) => {
      const curtidas = p.likes || 0;
      const compartilhamentos = p.shares || 0;
      const comentarios = p.comments_amounts || 0;
      const comQuadro = rede === 'instagram' || rede === 'facebook';
      const foto = String(p.picture_full_size || '');
      return {
        texto: normalize(comQuadro ? (p.text || p.content || '') : semUrl(p.text || p.content || ''), 260),
        rede,
        autor: normalize(p.author && p.author.name, 80) || null,
        propria: doAutor(p),
        link,
        // X e sites nao tem quadro oficial: a foto do post (nunca video) ajuda o cartao a parecer um post
        imagem: !comQuadro && /^https:\/\//i.test(foto) && !/\.(mp4|m3u8|mov)(\?|$)/i.test(foto) ? foto : null,
        data: p.date || null,
        curtidas, compartilhamentos, comentarios,
        interacoes: curtidas + compartilhamentos + comentarios,
      };
    })
    .filter((p) => p.texto)
    // de fora primeiro; dentro de cada grupo, o mais engajado
    .sort((a, b) => (a.propria - b.propria) || (b.interacoes - a.interacoes)));
  return porRede.flat().sort((a, b) => (a.propria - b.propria) || (b.interacoes - a.interacoes));
}

// Fecha a lista: um de cada rede primeiro, no maximo 2 por rede, ate 6 no total, do mais para o menos engajado.
function selecionarPostsDaMarca(candidatos) {
  const escolhidos = [];
  const vistos = new Set();
  const poe = (p) => {
    if (!p || vistos.has(p.link) || escolhidos.length >= MAX_POSTS_DA_MARCA) return;
    if (escolhidos.filter((e) => e.rede === p.rede).length >= MAX_POR_REDE) return;
    vistos.add(p.link); escolhidos.push(p);
  };
  const todos = candidatos.slice().sort((a, b) => (a.propria - b.propria) || (b.interacoes - a.interacoes));
  ['instagram', 'facebook', 'x', 'site'].forEach((rede) => poe(todos.find((p) => p.rede === rede)));
  todos.forEach(poe);
  return escolhidos.sort((a, b) => b.interacoes - a.interacoes);
}

// Sem conferencia de IA (usado nos testes e como base).
function escolherPostsDaMarca(resultados, nomeMarca, ficha) {
  return selecionarPostsDaMarca(candidatosDaMarca(resultados, ficha));
}

// Conferencia de relevancia: o nome da marca tambem e palavra comum ("Natura 2000" e uma rede europeia de areas protegidas,
// "in natura" e fruta, "vivo" e estar vivo). A IA le o texto de cada candidato e diz quais falam da MARCA do segmento.
// Sem IA ou com erro, mantem todos (so o filtro de palavra inteira).
const RELEVANCIA_SCHEMA = { type: 'object', properties: { relevantes: { type: 'array', items: { type: 'integer' } } }, required: ['relevantes'], additionalProperties: false };
const RELEVANCIA_SYSTEM = `Revisas posts de redes sociales y sitios web. Recibes el nombre de una MARCA (empresa o producto), su segmento y una lista numerada de posts con red, autor y texto. Los posts están en español.
Devuelve en "relevantes" los números de los posts que hablan DE LA MARCA del segmento indicado: la mencionan, la comentan, la anuncian, la venden, la critican o la usan, aunque sea de pasada.
NO incluyas posts donde la palabra aparece con otro sentido o habla de otra cosa con el mismo nombre (ej.: "Corona" como enfermedad o como corona de rey, "Bimbo" como apodo, "Liverpool" como ciudad o equipo de futbol en vez de la tienda, nombre de persona, lugar o banda).
Si tienes duda sobre un post que solo menciona la palabra sin contexto de marca, déjalo fuera.`;

async function conferirRelevancia(candidatos, nomeMarca, segmento) {
  if (!candidatos.length) return candidatos;
  const lista = candidatos.map((p, i) => ({ n: i, rede: p.rede, autor: p.autor, texto: normalize(p.texto, 200) }));
  const resposta = await chamarJSON({
    system: RELEVANCIA_SYSTEM,
    user: { marca: nomeMarca, segmento: segmento || null, posts: lista },
    schema: RELEVANCIA_SCHEMA,
    schemaName: 'relevancia_dos_posts',
    maxTokens: 300,
    timeoutMs: 12000,
    temperature: 0,
  }).catch(() => null);
  if (!resposta || !Array.isArray(resposta.relevantes)) return candidatos;
  const ok = new Set(resposta.relevantes.filter((n) => Number.isInteger(n)));
  // o perfil da propria marca sempre conta
  return candidatos.filter((p, i) => ok.has(i) || p.propria);
}

// --- Previa de link dos sites ---
// Quase nenhum site deixa ser embutido (X-Frame-Options), entao o "embed" de um site e a previa do link, como o Facebook e o X
// mostram: foto, titulo e resumo que a propria pagina declara (og:title, og:description, og:image). Falha ou demora: o post
// segue como cartao de texto. So http(s) e nunca endereco interno.
const decodificar = (t) => String(t || '').replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#0?39;|&apos;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>')
  .replace(/&#(\d+);/g, (m, n) => String.fromCodePoint(Math.min(Number(n), 0x10ffff))).replace(/\s+/g, ' ').trim();
const hostInterno = (h) => /^(localhost|.*\.(local|internal|localdomain))$/i.test(h) || /^\d{1,3}(\.\d{1,3}){3}$/.test(h) || h.includes(':') || !h.includes('.');

function lerMeta(html) {
  const metas = {};
  (html.match(/<meta\b[^>]*>/gi) || []).forEach((tag) => {
    const chave = (tag.match(/\b(?:property|name)\s*=\s*["']([^"']+)["']/i) || [])[1];
    const valor = (tag.match(/\bcontent\s*=\s*"([^"]*)"/i) || tag.match(/\bcontent\s*=\s*'([^']*)'/i) || [])[1];
    if (chave && valor && !metas[chave.toLowerCase()]) metas[chave.toLowerCase()] = decodificar(valor);
  });
  const titulo = (html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1];
  return {
    site: metas['og:site_name'] || null,
    titulo: metas['og:title'] || metas['twitter:title'] || decodificar(titulo) || null,
    descricao: metas['og:description'] || metas['twitter:description'] || metas.description || null,
    imagem: metas['og:image'] || metas['og:image:url'] || metas['twitter:image'] || null,
  };
}

async function previaDoSite(url) {
  try {
    const u = new URL(url);
    if (!/^https?:$/.test(u.protocol) || hostInterno(u.hostname)) return null;
    const r = await fetchWithTimeout(u.href, { headers: { 'User-Agent': 'Mozilla/5.0 (compatible; BuzzCompass/1.0; +https://buzzmonitor.com/es/)', Accept: 'text/html' }, redirect: 'follow' }, 4500);
    if (!r.ok || !/html/i.test(r.headers.get('content-type') || '')) return null;
    const head = (await r.text()).slice(0, 300000).split(/<\/head>/i)[0];
    const m = lerMeta(head);
    let imagem = m.imagem;
    try { imagem = imagem ? new URL(imagem, r.url || u.href).href : null; } catch (e) { imagem = null; }
    if (imagem && !/^https:\/\//i.test(imagem)) imagem = null;
    if (!m.titulo && !m.descricao && !imagem) return null;
    return { site: normalize(m.site, 60) || u.hostname.replace(/^www\./, ''), titulo: normalize(m.titulo, 140) || null, descricao: normalize(m.descricao, 220) || null, imagem };
  } catch (e) {
    return null;
  }
}

async function comPreviaDosSites(posts) {
  await Promise.all(posts.filter((p) => p.rede === 'site').map(async (p) => { p.previa = await previaDoSite(p.link); }));
  return posts;
}

function escolherInfluenciadores(resultados, nomesDaComparacao) {
  const evitar = nomesDaComparacao.map(semAcento);
  const vistos = new Set();
  for (const r of resultados) {
    if (!r || !r.ok || !r.value) continue;
    const lista = (r.value.data || []).map((inf) => {
      const social = (inf.social || [])[0] || {};
      return { nome: normalize(inf.name, 60) || null, rede: social.social_network || null, seguidores: social.followers || 0 };
    }).filter((inf) => {
      if (!inf.nome || vistos.has(inf.nome)) return false;
      const n = semAcento(inf.nome);
      if (evitar.some((e) => e && (n.includes(e) || e.includes(n)))) return false;
      vistos.add(inf.nome);
      return true;
    }).slice(0, 4);
    if (lista.length) return lista;
  }
  return [];
}

// Amostra aleatoria de uma marca grande e quase toda anuncio, cupom e revenda: critica real e rara (1 em 30). Para achar
// o que irrita e o que encanta, a busca da marca e cruzada com vocabulario de reclamacao e de elogio (E entre os grupos).
// O volume desses cruzamentos tambem e um numero: quanto da conversa tem linguagem de queixa ou de elogio.
// Versao LATAM: vocabulario de queixa e de elogio como se escreve em espanhol no Mexico e na America Latina.
const LEXICO_RECLAMACAO = '(queja OR quejarme OR pésimo OR pésima OR horrible OR "no lo recomiendo" OR "no recomiendo" OR fraude OR estafa OR tardanza OR retraso OR engaño OR defecto OR "no llegó" OR decepción OR decepcionada OR decepcionado OR cancelar OR problema OR "una vergüenza" OR "nunca más" OR "no funciona" OR "mal servicio" OR "mala atención" OR profeco)';
const LEXICO_ELOGIO = '(amo OR encanta OR encantó OR recomiendo OR "lo recomiendo" OR perfecto OR perfecta OR "el mejor" OR "la mejor" OR favorito OR favorita OR enamorada OR enamorado OR maravilloso OR maravillosa OR increíble OR "vale la pena" OR excelente)';
const comLexico = (query, lexico) => {
  const q = `(${query}) ${lexico}`;
  return q.length <= 1900 ? q : null;
};

// --- Perfil do Instagram da marca ---
// A Trends so confirma perfis que estao na base dela (com 1.000+ seguidores). Achou e o nome bate com o @ ou com a marca:
// perfil confirmado, com nome e seguidores. Nao achou: o @ continua valendo como ancora da busca, so nao ganha selo.
async function conferirPerfil(handle, nomeMarca) {
  if (!handle) return null;
  const limpo = (s) => semAcento(s).replace(/[^a-z0-9]/g, '');
  const h = limpo(handle);
  const b = limpo(nomeMarca);
  try {
    const resposta = await bmPerfilInstagram(handle);
    const candidatos = (Array.isArray(resposta && resposta.data) ? resposta.data : [])
      .map((p) => {
        const ig = (Array.isArray(p.social) ? p.social : []).find((s) => s && s.social_network === 'instagram');
        return { nome: normalize(p.name, 60), n: limpo(p.name), seguidores: ig ? Number(ig.followers) || 0 : 0, ig: Boolean(ig) };
      })
      .filter((c) => c.ig && c.n.length >= 3 && (h.includes(c.n) || c.n.includes(h) || c.n.includes(b) || b.includes(c.n)))
      .sort((x, y) => y.seguidores - x.seguidores);
    if (candidatos.length) return { handle, confirmado: true, nome: candidatos[0].nome, seguidores: candidatos[0].seguidores };
  } catch (err) { /* sem confirmacao: o @ segue valendo na busca */ }
  return { handle, confirmado: false };
}

// --- Pipeline ---

async function volumeComReserva(grupo, since, until) {
  try {
    return await bmVolume(grupo.query, 'sentiment', since, until);
  } catch (err) {
    // So troca a busca se a API a RECUSOU (4xx). Falha passageira (rede, 5xx) ja foi repetida em bmVolume: trocar uma
    // busca boa por uma pior so porque a rede oscilou esconderia o erro e encolheria o resultado.
    if (!/_4\d\d$/.test(String((err && err.message) || ''))) throw err;
    const reserva = grupo.reserva || queryExata(grupo.nome);
    if (!reserva || reserva === grupo.query) throw err;
    grupo.query = reserva; // a busca montada pela IA foi recusada pela API: cai para a de reserva
    return bmVolume(grupo.query, 'sentiment', since, until);
  }
}

function sugeridoMaisParecido(candidatos, volumeMarca) {
  const alvo = Math.log10(Math.max(volumeMarca, 1) + 1);
  return candidatos
    .slice()
    .sort((a, b) => Math.abs(Math.log10(a.sent.total + 1) - alvo) - Math.abs(Math.log10(b.sent.total + 1) - alvo));
}

// O mercado e a conversa do segmento MAIS as marcas da comparacao: uma busca so, cada parte entre parenteses ligada por OR.
function montarMercado(categoriaQuery, marcaQuery, finais) {
  const partes = [categoriaQuery, marcaQuery, ...finais.map((c) => c.query)].filter(Boolean).map((q) => `(${q})`);
  const uniao = partes.join(' OR ');
  if (uniao.length <= 1800) return uniao;
  return [categoriaQuery, marcaQuery].filter(Boolean).map((q) => `(${q})`).join(' OR ');
}

// Checagem de homonimo: para cada marca da comparacao, a IA le uma amostra aleatoria da propria busca e, se muitos posts
// forem de outro assunto, a busca e corrigida e o volume recalculado. Protecoes:
//  - correcao que apaga quase tudo (menos de 3% do volume) e descartada (exclusao errada e pior que o homonimo);
//  - se a IA acusa que metade ou mais dos posts e de outro assunto e a correcao nao resolveu (volume quase igual, ou
//    sem correcao), entra o modo ancora: so @perfil, #hashtag e frases compostas;
//  - se nada disso deixa a busca confiavel, a marca e sinalizada (busca_incerta) em vez de mostrar numero sem aviso.
// Qualquer falha de rede ou de IA mantem a busca original.
async function corrigirHomonimos(grupos, segmento, sinceStr, untilStr) {
  const volume = async (q) => contarSentimento((await bmVolume(q, 'sentiment', sinceStr, untilStr)).data);
  const revisoes = await Promise.all(grupos.map(async (g) => {
    try {
      const amostra = postsDe(await bmPosts(g.query, sinceStr, untilStr, 30, 'random'));
      const itens = amostra.slice(0, 20)
        .map((p) => ({ texto: normalize(p.text || p.content || '', 180), autor: normalize(p.author && p.author.name, 40) }))
        .filter((i) => i.texto);
      const rev = await revisarBusca({ nome: g.nome, segmento, query: g.query, posts: itens });
      if (!rev || !rev.problema) return { g, rev, aplicada: false };

      const antes = g.sent.total;
      const aceitavel = (sent) => sent.total > 0 && sent.total >= antes * 0.03;
      let query = null; let sent = null; let modo = null;
      if (rev.corrigida) {
        const s1 = await volume(rev.corrigida);
        if (aceitavel(s1)) { query = rev.corrigida; sent = s1; modo = 'corrigida'; }
      }
      const metadeFora = rev.fora / rev.total >= 0.5;
      if (metadeFora && (!query || sent.total > antes * 0.85)) {
        const anc = soAncoras(query || g.query);
        if (anc && anc !== (query || g.query)) {
          const s2 = await volume(anc);
          if (aceitavel(s2)) { query = anc; sent = s2; modo = 'ancora'; }
        }
      }
      const incerta = !query || (metadeFora && sent.total > antes * 0.85);
      return { g, rev, aplicada: Boolean(query), query, sent, modo, incerta };
    } catch (err) {
      return { g, aplicada: false };
    }
  }));
  const log = [];
  for (const r of revisoes) {
    if (r.incerta) r.g.incerta = true;
    if (!r.aplicada) continue;
    log.push({ marca: r.g.nome, modo: r.modo, fora_do_assunto: `${r.rev.fora} de ${r.rev.total}`, assunto: r.rev.assunto, volume_antes: r.g.sent.total, volume_depois: r.sent.total, incerta: Boolean(r.incerta) });
    r.g.query = r.query;
    r.g.sent = r.sent;
  }
  return log;
}

// Cada analise roda no fuso do pais escolhido (series diarias e chamadas da Trends). Sem pais, -6 (Cidade do Mexico).
function analisar(entrada) {
  return comFuso(fusoHoras(entrada && entrada.pais), () => analisarNoFuso(entrada));
}

async function analisarNoFuso({ marca, segmento, pais: codigoPais, informados, instagram, debug }) {
  const pais = dadosDoPais(codigoPais);
  const until = new Date();
  const since = new Date(until.getTime() - 30 * 24 * 60 * 60 * 1000);
  const meio = new Date(since.getTime() + 15 * 24 * 60 * 60 * 1000);
  const [sinceStr, untilStr, meioStr] = [bmDate(since), bmDate(until), bmDate(meio)];

  // A conferencia do perfil roda junto com o plano de buscas: nao soma tempo.
  const [plano, perfilInstagram] = await Promise.all([planejarBuscas({ marca, segmento, pais, informados, instagram }), conferirPerfil(instagram, marca)]);

  // Onda 1: volume por sentimento de cada marca candidata e da categoria (valida a query e mede o tamanho da conversa).
  const grupoMarca = { nome: plano.marca.nome, query: plano.marca.query };
  const candidatos = [...plano.informados, ...plano.sugeridos].map((c) => ({ ...c }));
  const reservaSegmento = categoriaPeloSegmento(segmento);
  const grupoCategoria = plano.categoria
    ? { nome: segmento || plano.categoria.nome, query: plano.categoria.query, reserva: reservaSegmento && reservaSegmento.query }
    : null;
  const todos = [grupoMarca, ...candidatos, ...(grupoCategoria ? [grupoCategoria] : [])];

  const onda1 = await emLote(todos.map((g) => () => volumeComReserva(g, sinceStr, untilStr)), 10);
  if (!onda1[0].ok) throw new Error(`marca_indisponivel: ${onda1[0].error && onda1[0].error.message}`);

  grupoMarca.sent = contarSentimento(onda1[0].value.data);
  candidatos.forEach((c, i) => { c.sent = onda1[1 + i].ok ? contarSentimento(onda1[1 + i].value.data) : null; });
  const categoriaOk = Boolean(grupoCategoria && onda1[onda1.length - 1].ok);

  // Concorrentes finais: os informados sempre entram (mesmo sem conversa); o resto e preenchido pelos sugeridos
  // com conversa, do tamanho mais parecido com o da marca.
  const finais = candidatos.filter((c) => c.origem === 'informado' && c.sent).slice(0, 3);
  const sugeridosComConversa = candidatos.filter((c) => c.origem === 'sugerido' && c.sent && c.sent.total > 0);
  for (const c of sugeridoMaisParecido(sugeridosComConversa, grupoMarca.sent.total)) {
    if (finais.length >= 3) break;
    finais.push(c);
  }

  // Checagem de homonimo (marca e concorrentes, em paralelo): corrige buscas que trouxeram outro assunto.
  const correcoes = await corrigirHomonimos([grupoMarca, ...finais], segmento, sinceStr, untilStr);
  const sentMarca = grupoMarca.sent;

  // O mercado: categoria + marca + concorrentes numa busca so. Se a API recusar a uniao, cai para a categoria sozinha (ou a marca).
  let queryMercado = montarMercado(categoriaOk ? grupoCategoria.query : null, grupoMarca.query, finais);
  let sentMercado = null;
  try {
    sentMercado = contarSentimento((await bmVolume(queryMercado, 'sentiment', sinceStr, untilStr)).data);
  } catch (err) {
    queryMercado = categoriaOk ? grupoCategoria.query : grupoMarca.query;
    sentMercado = contarSentimento((await bmVolume(queryMercado, 'sentiment', sinceStr, untilStr)).data);
  }
  const nomeMercado = segmento || (grupoCategoria && grupoCategoria.nome) || grupoMarca.nome;

  // Onda 2: leitura completa do mercado, serie diaria + amostra de posts de cada marca da comparacao, influenciadores.
  const tarefas = [];
  const pos = {};
  const reg = (chave, itens) => { pos[chave] = [tarefas.length, itens.length]; tarefas.push(...itens); };
  reg('mercado', tarefasDoMercado(queryMercado, sinceStr, untilStr, meioStr));
  const marcasDaComparacao = [{ nome: grupoMarca.nome, query: grupoMarca.query, incerta: Boolean(grupoMarca.incerta) }, ...finais.map((c) => ({ nome: c.nome, query: c.query, incerta: Boolean(c.incerta) }))];
  marcasDaComparacao.forEach((g, i) => {
    const qNeg = comLexico(g.query, LEXICO_RECLAMACAO);
    const qPos = comLexico(g.query, LEXICO_ELOGIO);
    const nada = () => Promise.resolve(null);
    reg(`g${i}`, [
      () => bmVolume(g.query, 'period_daily', sinceStr, untilStr),
      () => bmPosts(g.query, sinceStr, untilStr, 30, 'random'),
      qNeg ? () => bmVolume(qNeg, 'sentiment', sinceStr, untilStr) : nada,
      qPos ? () => bmVolume(qPos, 'sentiment', sinceStr, untilStr) : nada,
      qNeg ? () => bmPosts(qNeg, sinceStr, untilStr, 30, 'random') : nada,
      // elogios: so a marca em foco (os concorrentes entram pelo volume e pelas queixas)
      i === 0 && qPos ? () => bmPosts(qPos, sinceStr, untilStr, 30, 'random') : nada,
    ]);
  });
  // Quem fala da MARCA: posts mais engajados dela no Instagram, Facebook, X e sites, e perfis ligados ao nome. Uma chamada por
  // rede: o ranking "top" com a lista inteira de redes devolve so posts de uma delas.
  const queryMarca = marcasDaComparacao[0].query;
  reg('prova', [
    () => bmPosts(queryMarca, sinceStr, untilStr, 40, 'top_posts_field', ['instagram']),
    () => bmPosts(queryMarca, sinceStr, untilStr, 40, 'top_posts_field', ['facebook']),
    () => bmPosts(queryMarca, sinceStr, untilStr, 40, 'top_posts_field', ['twitter']),
    () => bmPosts(queryMarca, sinceStr, untilStr, 40, 'top_posts_field', ['misc']),
    () => bmInfluencers(grupoMarca.nome, '["es"]'), // so perfis em espanhol: sem isso aparece gente de outro pais com o mesmo nome
    // com pais escolhido, primeiro os perfis daquele pais; se nao houver nenhum, vale a lista em espanhol acima
    pais ? () => bmInfluencers(grupoMarca.nome, '["es"]', JSON.stringify([pais.codigo])) : () => Promise.resolve(null),
  ]);
  const onda2 = await emLote(tarefas, 10);
  const pega = (chave) => (pos[chave] ? onda2.slice(pos[chave][0], pos[chave][0] + pos[chave][1]) : []);

  const mercado = interpretarMercado(pega('mercado'), sentMercado, nomeMercado, queryMercado);
  const dadosParciais = mercado.parcial;

  // Comparacao: marca + concorrentes finais (partes do mercado)
  const unicos = (lista, n) => {
    const vistos = new Set();
    return lista.filter((e) => { const k = e.resumo.slice(0, 60); if (vistos.has(k)) return false; vistos.add(k); return true; }).slice(0, n);
  };
  const total = (r) => (r && r.ok && r.value ? contarSentimento(r.value.data).total : null);
  // Exemplo de uma marca so vale se o texto (ou o autor) citar a marca: a busca cruzada com vocabulario de queixa traz
  // muita noticia e politica que so casou por acaso.
  const fichaDe = (nome) => semAcento(nome).split(/[^a-z0-9]+/).filter((t) => t.length >= 4).sort((x, y) => y.length - x.length)[0] || null;
  // palavra inteira ("natura" nao casa "natureza" nem "naturalmente")
  const falaDe = (ficha) => {
    const re = ficha ? new RegExp(`(^|[^a-z0-9])${ficha}([^a-z0-9]|$)`) : null;
    return (p) => !re || re.test(semAcento(`${p.text || p.content || ''} ${(p.author && p.author.name) || ''}`));
  };
  const grupos = marcasDaComparacao.map((g, i) => {
    const [dailyRes, postsRes, volNegRes, volPosRes, postsNegRes, postsPosRes] = pega(`g${i}`);
    const sent = i === 0 ? sentMarca : finais[i - 1].sent;
    const amostra = postsRes && postsRes.ok ? postsDe(postsRes.value) : [];
    const ficha = fichaDe(g.nome);
    const doRes = (r) => (r && r.ok && r.value ? postsDe(r.value) : []).filter(falaDe(ficha));
    const amostraDaMarca = amostra.filter(falaDe(ficha));
    return {
      rotulo: g.nome,
      tipo: i === 0 ? 'marca' : 'concorrente',
      origem: i === 0 ? 'informado' : finais[i - 1].origem,
      query: g.query,
      incerta: g.incerta,
      sent,
      serie: serieAlinhada(dailyRes && dailyRes.ok ? dailyRes.value.data : null),
      composicaoAmostra: composicao(amostra),
      reclamacaoVolume: total(volNegRes),
      elogioVolume: total(volPosRes),
      // criticas e elogios: primeiro da busca cruzada com o vocabulario, depois da amostra aleatoria
      positivos: unicos([...porSentimento(doRes(postsPosRes), 'POSITIVE', 6), ...porSentimento(amostraDaMarca, 'POSITIVE', 6)], 5),
      negativos: unicos([...porSentimento(doRes(postsNegRes), 'NEGATIVE', 8), ...porSentimento(amostraDaMarca, 'NEGATIVE', 6)], 6),
    };
  });
  const somaVolume = grupos.reduce((s, g) => s + g.sent.total, 0);
  const comparacao = grupos.map((g) => ({
    rotulo: g.rotulo,
    tipo: g.tipo,
    origem: g.origem,
    query: g.query,
    volume: g.sent.total,
    share_pct: somaVolume ? Math.round((g.sent.total / somaVolume) * 100) : 0,
    positivos: g.sent.positivos,
    neutros: g.sent.neutros,
    negativos: g.sent.negativos,
    pct_positivo: pctPos(g.sent),
    crescimento_pct: crescimentoPct(g.serie),
    busca_incerta: Boolean(g.incerta),
    reclamacao_volume: g.reclamacaoVolume,
    reclamacao_pct: g.reclamacaoVolume !== null && g.sent.total ? Math.round((g.reclamacaoVolume / g.sent.total) * 1000) / 10 : null,
    elogio_volume: g.elogioVolume,
    elogio_pct: g.elogioVolume !== null && g.sent.total ? Math.round((g.elogioVolume / g.sent.total) * 1000) / 10 : null,
    serie: g.serie,
  }));

  const entradaScore = (g, c) => ({ positivos: g.sent.positivos, negativos: g.sent.negativos, total: g.sent.total, reclamacao_pct: c.reclamacao_pct, serie: g.serie });
  const scoresMarca = scoreDaMarca({
    marca: entradaScore(grupos[0], comparacao[0]),
    concorrentes: grupos.slice(1).map((g, i) => entradaScore(g, comparacao[i + 1])),
    mercado: { positivos: sentMercado.positivos, negativos: sentMercado.negativos, serie: mercado.serie },
  });

  const sugeridosNaComparacao = finais.some((c) => c.origem === 'sugerido');
  const [provaIg, provaFb, provaX, provaSites, provaInfl, provaInflPais] = pega('prova');
  const influenciadores = escolherInfluenciadores([provaInflPais, provaInfl], marcasDaComparacao.map((g) => g.nome));
  // candidatos limitados a 4 por rede antes da conferencia de IA (a lista fica curta e a chamada barata)
  const candidatosDePosts = candidatosDaMarca([provaIg, provaFb, provaX, provaSites], fichaDe(grupoMarca.nome))
    .filter((p, i, todos) => todos.slice(0, i).filter((q) => q.rede === p.rede).length < 4);
  const postsDaMarca = await comPreviaDosSites(selecionarPostsDaMarca(await conferirRelevancia(candidatosDePosts, grupoMarca.nome, segmento)));

  // Fatos ja comparados: a IA erra conta e comparacao (escreveu que 30 mil era menos que 17 mil), entao ela nao compara
  // numeros: copia estes rankings.
  const fmtMil = (n) => Number(n || 0).toLocaleString('es-MX');
  const comparaveis = comparacao.filter((g) => g.volume >= VOLUME_MINIMO_COMPARAR);
  const porVolume = comparacao.slice().sort((x, y) => y.volume - x.volume);
  const melhor = (lista, campo) => lista.filter((g) => g[campo] !== null).sort((x, y) => y[campo] - x[campo])[0];
  const euComp = comparacao[0];
  const fatos = {
    ranking_por_volume: porVolume.map((g, i) => `${i + 1}.º ${g.rotulo}: ${fmtMil(g.volume)} menciones (${g.share_pct}% de la conversación entre las marcas comparadas)`),
    marca_na_posicao_de_volume: porVolume.findIndex((g) => g.tipo === 'marca') + 1,
    lider_em_volume: porVolume[0].rotulo,
    maior_crescimento_ultimos_7_dias: (() => { const m = melhor(comparaveis, 'crescimento_pct'); return m ? `${m.rotulo} (${m.crescimento_pct >= 0 ? '+' : ''}${m.crescimento_pct}%)` : null; })(),
    maior_percentual_positivo: (() => { const m = melhor(comparaveis, 'pct_positivo'); return m ? `${m.rotulo} (${m.pct_positivo}%)` : null; })(),
    maior_percentual_de_reclamacao: (() => { const m = melhor(comparaveis, 'reclamacao_pct'); return m ? `${m.rotulo} (${m.reclamacao_pct}% de las menciones con lenguaje de queja)` : null; })(),
    marcas_pequenas_demais_para_comparar: comparacao.filter((g) => g.volume < VOLUME_MINIMO_COMPARAR).map((g) => g.rotulo),
  };
  const payload = {
    dados_parciais: dadosParciais,
    marca_em_foco: grupoMarca.nome,
    segmento: nomeMercado,
    pais: pais ? pais.nome : null,
    mercado: paraIAMercado(mercado, nomeMercado),
    concorrentes_sugeridos: sugeridosNaComparacao,
    fatos,
    comparacao: grupos.map((g, i) => ({
      nome: g.rotulo,
      tipo: g.tipo,
      volume_30d: comparacao[i].volume,
      volume_30d_formatado: fmtMil(comparacao[i].volume),
      share_de_voz_pct: comparacao[i].share_pct,
      percentual_positivo_entre_posts_com_polaridade: comparacao[i].pct_positivo,
      crescimento_ultimos_7_dias_vs_7_anteriores_pct: comparacao[i].crescimento_pct,
      mencoes_com_linguagem_de_reclamacao: comparacao[i].reclamacao_volume,
      percentual_com_linguagem_de_reclamacao: comparacao[i].reclamacao_pct,
      mencoes_com_linguagem_de_elogio: comparacao[i].elogio_volume,
      percentual_com_linguagem_de_elogio: comparacao[i].elogio_pct,
      composicao_da_amostra_aleatoria: g.composicaoAmostra,
      busca_incerta: comparacao[i].busca_incerta,
      exemplos_positivos: g.positivos,
      exemplos_negativos: g.negativos,
    })),
  };
  const daIA = await chamarJSON({
    system: NARRATIVE_SYSTEM,
    user: payload,
    schema: NARRATIVE_SCHEMA,
    schemaName: 'buzz_compass_totem',
    maxTokens: 2200,
    timeoutMs: 32000,
    temperature: 0.4,
    // modelo mais forte para a leitura (se nao existir na conta, cai no padrao). Troca por variavel de ambiente.
    modeloOpenAI: process.env.OPENAI_MODEL_NARRATIVA || 'gpt-4o',
  });
  // O rascunho de temas serve so para a IA se ancorar na evidencia antes de escrever: nao vai para a tela.
  if (daIA) delete daIA.temas;
  const narrativa = daIA ? formatarTextosEsMx(daIA) : narrativaPorDados({ marca: grupoMarca.nome, segmento: nomeMercado, mercado, comparacao, sugeridos: sugeridosNaComparacao });

  return {
    ok: true,
    // ?debug=1: mostra o que a IA recebeu (so dado publico da Trends + nomes digitados) para auditar o texto dos cards
    ...(debug ? { debug: { payload_ia: payload } } : {}),
    marca: { nome: grupoMarca.nome, segmento: segmento || null, pais: pais ? { codigo: pais.codigo, nome: pais.nome } : null, query: grupoMarca.query, instagram: perfilInstagram, scores: scoresMarca },
    mercado: {
      nome: nomeMercado,
      query: queryMercado,
      volume: sentMercado.total,
      emergentes: mercado.emergentes,
      charts: {
        sentimento: { positivos: sentMercado.positivos, neutros: sentMercado.neutros, negativos: sentMercado.negativos },
        genero: mercado.genero,
        canais: mercado.canais,
        serie_diaria: mercado.serie,
        datas: chavesDosDias(), // AAAAMMDD de cada ponto das series (eixo X dos graficos)
        termos: mercado.termos,
      },
    },
    narrativa,
    comparacao,
    prova: { posts: postsDaMarca, influenciadores },
    meta: {
      dados_parciais: dadosParciais,
      volume_total_30d: sentMercado.total,
      concorrentes_sugeridos: sugeridosNaComparacao,
      ia_buscas: plano.iaDisponivel,
      ia_narrativa: Boolean(daIA),
      modelo_narrativa: daIA ? daIA._modelo : null,
      correcoes_de_busca: correcoes,
      gerado_em: new Date().toISOString(),
    },
  };
}

module.exports = { analisar, narrativaPorDados, formatarNumerosEsMx, formatarTextosEsMx, escolherPostsDaMarca, candidatosDaMarca, selecionarPostsDaMarca, conferirRelevancia, lerMeta, previaDoSite };
