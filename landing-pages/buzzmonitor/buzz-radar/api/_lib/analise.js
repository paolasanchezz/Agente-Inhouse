// Pipeline do totem: marca + concorrentes -> buscas (skill /buscas, ver buscas.js) -> Trends -> scores deterministicos
// -> narrativa por IA. Os numeros nunca vem da IA: ela so escreve texto em cima do que foi calculado aqui.
// O Compass Score e da MARCA (api/_lib/score.js, documentado em SCORING.md); o segmento aparece nos graficos e nos cards.

const { normalize, fetchWithTimeout, bmDate, bmVolume, bmPosts, bmInfluencers, bmPerfilInstagram, emLote } = require('./trends');
const { chamarJSON } = require('./llm');
const { planejarBuscas, revisarBusca, soAncoras, queryExata, categoriaPeloSegmento } = require('./buscas');
const { scoreDaMarca, crescimentoPct } = require('./score');

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

// 30 dias corridos no fuso do Brasil (-3), na mesma ordem para todos os grupos (barra comparar linha com linha).
function chavesDosDias() {
  const chaves = [];
  for (let i = 29; i >= 0; i--) {
    const d = new Date(Date.now() - 3 * 3600e3 - i * 86400e3);
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
const RUIDO = new Set(['link', 'bio', 'whatsapp', 'zap', 'direct', 'clique', 'aqui', 'perfil', 'siga', 'comente', 'compartilhe',
  'garanta', 'aproveite', 'confira', 'deixar', 'gente', 'mundo', 'hoje', 'agora', 'todos', 'todas', 'ainda', 'ficar', 'fazer',
  'tudo', 'tudo', 'coisa', 'vida', 'dia', 'dias', 'novo', 'nova', 'mais', 'muito', 'pra', 'pro', 'tbm', 'vcs', 'voce', 'voces',
  'mercado', 'qualquer', 'especial', 'loja', 'site', 'instagram', 'facebook', 'twitter', 'video', 'foto', 'post', 'live']);

function limparTermos(termos, nome, query) {
  const tokens = tokensDaBusca(nome, query);
  return (termos || []).filter((t) => !tokens.has(semAcento(t.label)) && !RUIDO.has(semAcento(t.label)));
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

const NARRATIVE_SYSTEM = `Voce e a analista de inteligencia de mercado por tras do Buzz Compass, ferramenta da Buzzmonitor, lendo o resultado de uma pessoa que acabou de rodar o Buzz Compass da propria marca num totem de evento.
Tom de voz: profissional, acessivel, orientado a dados, com energia e clareza. Nunca use "revolucionario", "disruptivo" ou hype vazio. Nunca sugira que a inteligencia artificial substitui pessoas. A marca e sempre feminina: "a Buzzmonitor". Nunca use a palavra "momentum".
Voce recebe: "marca_em_foco", o "segmento", a leitura do "mercado" (a conversa inteira do segmento, com a marca e os concorrentes dentro), os "fatos" ja comparados e a "comparacao" de cada marca com exemplos reais de posts positivos e negativos. A base e limitada (projetos ja monitorados por clientes da Buzzmonitor), nao a internet inteira em tempo real.

COMO TRABALHAR, nesta ordem:
1) Preencha "temas" PRIMEIRO. Leia os "exemplos_positivos" e "exemplos_negativos" de cada marca e do mercado e liste de 4 a 8 temas CONCRETOS que aparecem de verdade nesses posts (ex.: "cupom de desconto na loja da consultora", "lancamento de uma linha de perfume", "reclamacao de atraso na entrega"). Para cada um: sentimento, onde aparece (marca, concorrente ou mercado), "evidencia" (trecho curto do exemplo) e "posts_na_amostra" (quantos exemplos tratam disso). Ignore post que nao fala do segmento nem da marca (noticia aleatoria, outro assunto). So liste tema que existe nos exemplos: nunca invente.
2) Escreva os 4 cards a partir dos temas e dos numeros.

REGRAS DE NUMERO (a IA ja errou conta e disse que 30 mil era menos que 17 mil):
- Use somente numeros do payload, copiados. NAO some, subtraia, arredonde nem compare numeros por conta propria.
- Ranking, lider, maior crescimento, maior percentual positivo e maior percentual de reclamacao: use SO o campo "fatos".
- Use "volume_30d_formatado" exatamente como esta (ex.: 30.083).
- "crescimento_ultimos_7_dias_vs_7_anteriores_pct" compara a ultima semana com a anterior: nunca diga "nos ultimos 30 dias". "variacao_do_percentual_positivo_entre_quinzenas_em_pontos" e do MERCADO inteiro, em pontos percentuais, nunca atribuida a uma marca nem escrita como %.
- "percentual_com_linguagem_de_reclamacao" e "..._de_elogio" medem quanto das mencoes da marca usa vocabulario de queixa ou de elogio; "composicao_da_amostra_aleatoria" mostra quantos posts da amostra sao positivos, neutros e negativos.

O QUE SE ESPERA DE CADA CARD. Cada card tem tres campos: "titulo" (ate 6 palavras), "segmento" e "marca".
- "segmento" fala do MERCADO do segmento: a conversa inteira (temas, termos, sentimento, formatos e os concorrentes). "marca" fala SO da marca em foco: a evidencia dela (percentuais, exemplos, posicao) e termina com uma acao concreta. Cada campo tem 2 a 3 frases e ao menos um numero real; numeros do segmento ficam em "segmento" e numeros da marca em "marca", nunca misturados.
- oportunidade: "segmento" = 2 ou 3 temas positivos CONCRETOS que geram conversa favoravel agora, com o numero que os sustenta. "marca" = como a marca aparece nesses temas (ou ainda nao aparece, e esse e o espaco a ocupar) e a acao ligada a eles (qual tema, formato ou canal).
- risco: "segmento" = os temas negativos CONCRETOS do mercado (o que irrita, o que da errado), com exemplo parafraseado; se a critica na amostra for pequena, DIGA isso com os numeros em vez de inventar risco. "marca" = as queixas da propria marca (exemplos_negativos dela e percentual com linguagem de reclamacao) e o que fazer; se forem poucas, diga o numero.
- tendencia_emergente: "segmento" = o que e novo na conversa ("termos_emergentes_2a_quinzena") e o formato que performa ("conteudos_que_performaram_bem"); sem termo emergente, diga que e o retrato do mes inteiro. "marca" = o ritmo dela e o que isso pede dela.
- concorrentes: "segmento" = como os concorrentes estao no segmento, usando "fatos" e os exemplos de cada um: quem lidera, quem tem a conversa mais positiva, quem cresce mais, quem recebe mais queixa e o que as pessoas elogiam ou criticam em cada concorrente (tema concreto). Cite pelo menos dois concorrentes pelo nome. "marca" = onde a marca esta frente a eles (posicao, participacao, reputacao, crescimento) e uma acao. Se "concorrentes_sugeridos" for true, diga em uma frase que parte foi escolhida pela Buzzmonitor pelo mercado da marca. Marca com "busca_incerta" true tem nome comum: avise e nao tire conclusao forte.
- Marca com pouca conversa: apresente o numero real como ESPACO A OCUPAR. NUNCA use as expressoes "dados insuficientes", "sem dados", "dados limitados" nem "aparece pouco na base". Marcas em "marcas_pequenas_demais_para_comparar" (menos de 50 mencoes) ainda tem pouca conversa no periodo: nao compare percentuais delas.

PROIBIDO: frases vazias como "e importante monitorar", "participar mais das conversas", "fortalecer a imagem" sem dizer COM QUE (qual tema, formato ou canal). Toda recomendacao aponta algo que apareceu nas evidencias. Nunca mande olhar grafico, nuvem ou tabela. NUNCA cite nome de pessoa, perfil ou pagina que aparece nos exemplos de posts; nomes de marcas da comparacao podem ser citados. Se "dados_parciais" for true, seja mais cauteloso.
Escreva em portugues do Brasil, direto, sem cliches, sem em-dash, com numeros no formato brasileiro (ponto separa milhar: 40.459 e 2.391; virgula separa decimal: 2,4%), sem formulas do tipo "nao e X, e Y". Titulo de ate 6 palavras.`;

// A IA escreve numero ao estilo americano ("40459", "2.4%"). A tela e em portugues do Brasil: milhar com ponto (40.459) e
// decimal com virgula (2,4%). A correcao e feita aqui, no texto pronto, porque so o prompt nao garante.
// - inteiro de 4+ digitos sem separador ganha o ponto de milhar, EXCETO ano (1900 a 2100) que nao e seguido de contagem
//   ("Natura 2000", "em 2026"); "2391 menções" continua sendo numero;
// - decimal com ponto (1 ou 2 casas) vira virgula; numero que ja tem ponto de milhar (11.179) nao muda.
const CONTAGEM = /^\s*(mencoes|menções|posts|perfis|seguidores|curtidas|comentarios|comentários|compartilhamentos|pessoas|vezes|resultados|%)/i;
function formatarNumerosPtBr(texto) {
  if (typeof texto !== 'string') return texto;
  return texto
    // milhar ja correto (11.179, 1.234.567): protege trocando por marcador, para a regra do decimal nao mexer
    .replace(/(?<![\d.,])(\d{1,3}(?:\.\d{3})+)(?![\d])/g, (m) => m.replace(/\./g, '\u0001'))
    // decimal com ponto: 2.4% / 0.7 / 14.35
    .replace(/(?<![\d.,])(\d+)\.(\d{1,2})(?![\d.])/g, '$1,$2')
    .replace(/\u0001/g, '.')
    // inteiro de 4+ digitos sem separador
    .replace(/(?<![\d.,])(\d{4,})(?![\d])(?!\.\d)(?!,\d)/g, (m, num, pos, todo) => {
      const n = Number(num);
      const resto = todo.slice(pos + m.length);
      if (n >= 1900 && n <= 2100 && !CONTAGEM.test(resto)) return m; // ano
      return num.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    });
}
function formatarTextosPtBr(obj) {
  if (typeof obj === 'string') return formatarNumerosPtBr(obj);
  if (Array.isArray(obj)) return obj.map(formatarTextosPtBr);
  if (obj && typeof obj === 'object') {
    const novo = {};
    Object.keys(obj).forEach((k) => { novo[k] = formatarTextosPtBr(obj[k]); });
    return novo;
  }
  return obj;
}

// --- Insights sem IA: texto montado so com o que a Trends devolveu (mesma regra: nada inventado, nada de "veja o grafico") ---

const VOLUME_MINIMO_COMPARAR = 50;
const fmtN = (n) => Number(n || 0).toLocaleString('pt-BR');
const lista = (itens) => (itens.length <= 1 ? itens.join('') : `${itens.slice(0, -1).join(', ')} e ${itens[itens.length - 1]}`);
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
    titulo: 'Temas que geram conversa positiva',
    segmento: `${pctP !== null ? `${pctP}% dos posts com polaridade no segmento de ${segmento} são positivos (${fmtN(pos)} de ${fmtN(comPolaridade)}). ` : `O segmento de ${segmento} somou ${fmtN(mercado.sent.total)} menções em 30 dias. `}` +
      `${top.length ? `Os termos mais citados são ${lista(top)}. ` : ''}` +
      `${mercado.positivos[0] ? `Um dos posts positivos da amostra diz: “${citar(mercado.positivos[0].resumo)}”.` : ''}`.trim(),
    marca: `${euComVolume && eu.pct_positivo !== null ? `${eu.pct_positivo}% dos posts de ${marca} com polaridade são positivos. ` : `${marca} ainda tem pouca conversa no período, o que deixa espaço para ocupar. `}` +
      `Conteúdo de ${marca} que entre nesses temas pega uma conversa que já está favorável.`,
  };

  const queda = mercado.tendenciaSentimento;
  const risco = {
    titulo: 'Assuntos que geram conversa negativa',
    segmento: `${comPolaridade ? `${100 - pctP}% dos posts com polaridade no segmento são negativos (${fmtN(neg)}). ` : ''}` +
      `${queda !== null ? `O percentual de posts positivos ${queda < 0 ? 'caiu' : 'subiu'} ${Math.abs(queda)} pontos da primeira para a segunda quinzena. ` : ''}` +
      `${mercado.negativos[0] ? `Um dos posts negativos da amostra diz: “${citar(mercado.negativos[0].resumo)}”.` : ''}`.trim(),
    marca: `${eu && eu.reclamacao_pct != null ? `${eu.reclamacao_pct}% das menções de ${marca} usam linguagem de queixa. ` : ''}` +
      `${eu ? `${marca} responde por ${eu.share_pct}% da conversa entre as marcas comparadas, então esses assuntos chegam à marca em proporção parecida. ` : ''}` +
      `Vale acompanhar esses temas antes que ganhem escala.`,
  };

  const emerg = mercado.emergentes.slice(0, 5);
  const tendencia = {
    titulo: emerg.length ? 'O que cresce na conversa' : 'O que mais aparece na conversa',
    segmento: `${emerg.length ? `Os termos que mais cresceram da primeira para a segunda quinzena são ${lista(emerg)}. ` : `Nenhum termo novo se destacou entre as quinzenas. O retrato do mês traz ${lista(top)}. `}` +
      `${ritmo !== null ? `O volume diário do segmento ${ritmo >= 0 ? 'subiu' : 'caiu'} ${Math.abs(ritmo)}% na última semana frente à anterior. ` : ''}` +
      `${mercado.destaques[0] && mercado.destaques[0].tipo ? `Entre os posts de maior alcance, o formato predominante é ${String(mercado.destaques[0].tipo).toLowerCase()}.` : ''}`.trim(),
    marca: `${euComVolume && eu.crescimento_pct !== null ? `${marca} ${eu.crescimento_pct >= 0 ? 'cresceu' : 'recuou'} ${Math.abs(eu.crescimento_pct)}% na última semana frente à anterior. ` : ''}` +
      `Quem chegar primeiro a esses assuntos fala com uma audiência em movimento.`,
  };

  // Marca com menos de VOLUME_MINIMO_COMPARAR mencoes: percentual e crescimento dela enganam, entao nao entram no ranking.
  const comparaveis = comparacao.filter((g) => g.volume >= VOLUME_MINIMO_COMPARAR);
  const pequenos = concs.filter((g) => g.volume < VOLUME_MINIMO_COMPARAR);
  const lider = comparacao.slice().sort((a, b) => b.volume - a.volume)[0];
  const maisPositivo = comparaveis.filter((g) => g.pct_positivo !== null).sort((a, b) => b.pct_positivo - a.pct_positivo)[0];
  const maisCresce = comparaveis.filter((g) => g.crescimento_pct !== null).sort((a, b) => b.crescimento_pct - a.crescimento_pct)[0];
  const concorrentes = {
    titulo: 'Como a marca se posiciona',
    segmento: `${lider ? `${lider.rotulo} lidera a conversa com ${lider.share_pct}% (${fmtN(lider.volume)} menções). ` : ''}` +
      `${maisPositivo ? `A conversa mais positiva é a de ${maisPositivo.rotulo}, com ${maisPositivo.pct_positivo}% de posts positivos. ` : ''}` +
      `${maisCresce ? `Quem mais cresce na última semana é ${maisCresce.rotulo}, com ${maisCresce.crescimento_pct >= 0 ? '+' : ''}${maisCresce.crescimento_pct}%. ` : ''}` +
      `${pequenos.length ? `${lista(pequenos.map((g) => g.rotulo))} ${pequenos.length > 1 ? 'têm' : 'tem'} pouca conversa no período (menos de ${VOLUME_MINIMO_COMPARAR} menções), por isso ritmo e sentimento ${pequenos.length > 1 ? 'deles' : 'dele'} ficam fora da comparação. ` : ''}` +
      `${concs.length && sugeridos ? 'Parte dos concorrentes foi escolhida pela Buzzmonitor pelo mercado da marca.' : ''}`.trim(),
    marca: `${eu && lider && lider !== eu ? `${marca} tem ${eu.share_pct}% da conversa (${fmtN(eu.volume)} menções) contra ${lider.share_pct}% de ${lider.rotulo}: essa distância é o espaço que ${marca} ainda pode ocupar.` : `${marca} lidera a conversa, e o desafio é manter a vantagem.`}`,
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
  return String(segmento || '').split(/[^\p{L}\p{N}]+/u).filter((p) => p.length >= 4 && !/^(para|como|mais|sobre|entre)$/i.test(p)).slice(0, 2);
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
const RELEVANCIA_SYSTEM = `Voce confere posts de redes sociais e sites. Recebe o nome de uma MARCA (empresa ou produto), o segmento dela e uma lista numerada de posts com rede, autor e texto.
Devolva em "relevantes" os numeros dos posts que falam DA MARCA do segmento informado: citam, comentam, anunciam, vendem, criticam ou usam a marca, mesmo de passagem.
NAO inclua posts em que a palavra aparece em outro sentido ou fala de outra coisa com o mesmo nome (ex.: "Natura 2000" rede europeia de areas protegidas, "in natura" para alimento, "vivo" no sentido de estar vivo, nome de pessoa, lugar ou banda).
Na duvida sobre um post que so cita a palavra sem contexto de marca, deixe de fora.`;

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
    const r = await fetchWithTimeout(u.href, { headers: { 'User-Agent': 'Mozilla/5.0 (compatible; BuzzCompass/1.0; +https://buzzmonitor.com.br)', Accept: 'text/html' }, redirect: 'follow' }, 4500);
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
    if (!r || !r.ok) continue;
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
const LEXICO_RECLAMACAO = '(reclamação OR reclamar OR péssimo OR péssima OR horrível OR "não recomendo" OR golpe OR demora OR atraso OR enganação OR defeito OR "não chegou" OR decepção OR decepcionada OR cancelar OR problema OR absurdo OR "nunca mais" OR "não funciona" OR "mal atendida" OR "mal atendido")';
const LEXICO_ELOGIO = '(amo OR amei OR adoro OR recomendo OR perfeito OR perfeita OR melhor OR queridinho OR queridinha OR apaixonada OR apaixonado OR maravilhoso OR maravilhosa OR cheiroso OR "vale a pena")';
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

async function analisar({ marca, segmento, informados, instagram, debug }) {
  const until = new Date();
  const since = new Date(until.getTime() - 30 * 24 * 60 * 60 * 1000);
  const meio = new Date(since.getTime() + 15 * 24 * 60 * 60 * 1000);
  const [sinceStr, untilStr, meioStr] = [bmDate(since), bmDate(until), bmDate(meio)];

  // A conferencia do perfil roda junto com o plano de buscas: nao soma tempo.
  const [plano, perfilInstagram] = await Promise.all([planejarBuscas({ marca, segmento, informados, instagram }), conferirPerfil(instagram, marca)]);

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
    () => bmInfluencers(grupoMarca.nome, '["pt"]'), // so perfis em portugues: sem isso aparece gente de outro pais com o mesmo nome
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
  const [provaIg, provaFb, provaX, provaSites, provaInfl] = pega('prova');
  const influenciadores = escolherInfluenciadores([provaInfl], marcasDaComparacao.map((g) => g.nome));
  // candidatos limitados a 4 por rede antes da conferencia de IA (a lista fica curta e a chamada barata)
  const candidatosDePosts = candidatosDaMarca([provaIg, provaFb, provaX, provaSites], fichaDe(grupoMarca.nome))
    .filter((p, i, todos) => todos.slice(0, i).filter((q) => q.rede === p.rede).length < 4);
  const postsDaMarca = await comPreviaDosSites(selecionarPostsDaMarca(await conferirRelevancia(candidatosDePosts, grupoMarca.nome, segmento)));

  // Fatos ja comparados: a IA erra conta e comparacao (escreveu que 30 mil era menos que 17 mil), entao ela nao compara
  // numeros: copia estes rankings.
  const fmtMil = (n) => Number(n || 0).toLocaleString('pt-BR');
  const comparaveis = comparacao.filter((g) => g.volume >= VOLUME_MINIMO_COMPARAR);
  const porVolume = comparacao.slice().sort((x, y) => y.volume - x.volume);
  const melhor = (lista, campo) => lista.filter((g) => g[campo] !== null).sort((x, y) => y[campo] - x[campo])[0];
  const euComp = comparacao[0];
  const fatos = {
    ranking_por_volume: porVolume.map((g, i) => `${i + 1}o ${g.rotulo}: ${fmtMil(g.volume)} menções (${g.share_pct}% da conversa entre as marcas comparadas)`),
    marca_na_posicao_de_volume: porVolume.findIndex((g) => g.tipo === 'marca') + 1,
    lider_em_volume: porVolume[0].rotulo,
    maior_crescimento_ultimos_7_dias: (() => { const m = melhor(comparaveis, 'crescimento_pct'); return m ? `${m.rotulo} (${m.crescimento_pct >= 0 ? '+' : ''}${m.crescimento_pct}%)` : null; })(),
    maior_percentual_positivo: (() => { const m = melhor(comparaveis, 'pct_positivo'); return m ? `${m.rotulo} (${m.pct_positivo}%)` : null; })(),
    maior_percentual_de_reclamacao: (() => { const m = melhor(comparaveis, 'reclamacao_pct'); return m ? `${m.rotulo} (${m.reclamacao_pct}% das menções com linguagem de queixa)` : null; })(),
    marcas_pequenas_demais_para_comparar: comparacao.filter((g) => g.volume < VOLUME_MINIMO_COMPARAR).map((g) => g.rotulo),
  };
  const payload = {
    dados_parciais: dadosParciais,
    marca_em_foco: grupoMarca.nome,
    segmento: nomeMercado,
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
  const narrativa = daIA ? formatarTextosPtBr(daIA) : narrativaPorDados({ marca: grupoMarca.nome, segmento: nomeMercado, mercado, comparacao, sugeridos: sugeridosNaComparacao });

  return {
    ok: true,
    // ?debug=1: mostra o que a IA recebeu (so dado publico da Trends + nomes digitados) para auditar o texto dos cards
    ...(debug ? { debug: { payload_ia: payload } } : {}),
    marca: { nome: grupoMarca.nome, segmento: segmento || null, query: grupoMarca.query, instagram: perfilInstagram, scores: scoresMarca },
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

module.exports = { analisar, narrativaPorDados, formatarNumerosPtBr, formatarTextosPtBr, escolherPostsDaMarca, candidatosDaMarca, selecionarPostsDaMarca, conferirRelevancia, lerMeta, previaDoSite };
