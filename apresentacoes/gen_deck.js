// Apresentação: Automação de Conteúdo — Grupo Elife (2026-06-11)
// Gera automacao-conteudo-grupo-elife.pptx — 16:9, minimalista.
const pptxgen = require("pptxgenjs");

// ---------- paleta ----------
const PAPER = "FAF9F6";
const INK = "1E2723";
const DARK = "14201A";
const ACCENT = "0B7A65";
const AMBER = "975711";        // passa 4.5:1 sobre AMBER_TINT
const AMBER_TINT = "FBF3E4";
const MUTED = "616E68";        // 4.9:1 sobre PAPER
const BORDER = "D7E0DA";
const SAGE = "E9F1EC";
const ARROW = "9DB2A9";
const WHITE = "FFFFFF";
const DARK_TXT = "F4F4EF";
const DARK_MUT = "9AAFA5";

const F_TITLE = "Georgia";
const F_BODY = "Calibri";
const F_MONO = "Consolas";

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10 x 5.625
pres.author = "Time de Conteúdo — Grupo Elife";
pres.title = "Automação de Conteúdo — Grupo Elife";

pres.defineSlideMaster({
  title: "LIGHT",
  background: { color: PAPER },
  objects: [
    { text: { text: "Automação de conteúdo · Grupo Elife", options: { x: 0.55, y: 5.34, w: 3.5, h: 0.22, fontSize: 8, fontFace: F_BODY, color: MUTED } } },
  ],
  slideNumber: { x: 9.3, y: 5.34, w: 0.35, h: 0.22, fontSize: 8, fontFace: F_BODY, color: MUTED, align: "right" },
});
pres.defineSlideMaster({ title: "DARK", background: { color: DARK }, objects: [] });

// ---------- helpers ----------
function kickerTitle(slide, kicker, title, desc, dark = false) {
  slide.addText(kicker.toUpperCase(), {
    x: 0.55, y: 0.38, w: 6.3, h: 0.3, fontSize: 9.5, bold: true, charSpacing: 2.5,
    fontFace: F_BODY, color: dark ? "5FD3B8" : ACCENT, margin: 0,
  });
  slide.addText(title, {
    x: 0.52, y: 0.62, w: 6.35, h: 0.62, fontSize: 26, bold: true,
    fontFace: F_TITLE, color: dark ? DARK_TXT : INK, margin: 0, valign: "top",
  });
  if (desc) slide.addText(desc, {
    x: 0.55, y: 1.28, w: 6.1, h: 0.78, fontSize: 11, fontFace: F_BODY,
    color: dark ? DARK_MUT : MUTED, margin: 0, valign: "top",
  });
}

// coluna de meta-informações à direita (comando + pares rótulo/valor)
function metaColumn(slide, cmd, pairs) {
  const x = 7.0, w = 2.45;
  slide.addShape(pres.shapes.LINE, { x: 6.82, y: 0.45, w: 0, h: 1.62, line: { color: BORDER, width: 1 } });
  slide.addText(cmd, {
    shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.05,
    x, y: 0.42, w, h: 0.34, fill: { color: SAGE }, fontSize: 8.5, fontFace: F_MONO,
    color: ACCENT, align: "left", valign: "middle", margin: 0.06, bold: true,
  });
  const runs = [];
  pairs.forEach((p, i) => {
    runs.push({ text: p[0].toUpperCase() + "  ", options: { fontSize: 7.5, fontFace: F_MONO, color: MUTED, breakLine: false } });
    runs.push({ text: p[1], options: { fontSize: 9.5, fontFace: F_BODY, color: INK, breakLine: i < pairs.length - 1 } });
  });
  slide.addText(runs, { x, y: 0.86, w, h: 1.3, margin: 0, valign: "top", paraSpaceAfter: 5 });
}

// nó do fluxograma
const NODE_H = 0.95;
function nodeStyle(type) {
  if (type === "src") return { fill: { color: SAGE }, line: null, tc: INK, cc: MUTED };
  if (type === "gate") return { fill: { color: AMBER_TINT }, line: { color: AMBER, width: 1.25, dashType: "dash" }, tc: AMBER, cc: AMBER };
  if (type === "out") return { fill: { color: INK }, line: null, tc: WHITE, cc: "C7D6CF" };
  return { fill: { color: WHITE }, line: { color: BORDER, width: 1 }, tc: INK, cc: MUTED };
}

function drawNode(slide, n, x, y, w) {
  const st = nodeStyle(n.type || "step");
  const runs = [{ text: n.t, options: { bold: true, fontSize: 10.5, fontFace: F_BODY, color: st.tc, breakLine: !!n.c } }];
  if (n.c) {
    const lines = Array.isArray(n.c) ? n.c : [n.c];
    lines.forEach((ln, i) => runs.push({ text: ln, options: { fontSize: 7.5, fontFace: F_BODY, color: st.cc, breakLine: i < lines.length - 1 } }));
  }
  const opts = {
    shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06,
    x, y, w, h: NODE_H, fill: st.fill, align: "center", valign: "middle", margin: 0.06,
  };
  if (st.line) opts.line = st.line;
  slide.addText(runs, opts);
}

function hArrow(slide, x, y, len) {
  slide.addShape(pres.shapes.LINE, {
    x: x + 0.03, y, w: len - 0.06, h: 0,
    line: { color: ARROW, width: 1.5, endArrowType: "triangle" },
  });
}

// fluxo em 1 ou 2 linhas (serpentina simples entre linhas)
function flow(slide, rows, topY) {
  const MX = 0.5, GAP = 0.3, AVAIL = 10 - 2 * MX;
  const ROW_GAP = 0.46;
  rows.forEach((nodes, r) => {
    const y = topY + r * (NODE_H + ROW_GAP);
    let unit = (AVAIL - GAP * (nodes.length - 1)) / nodes.length;
    if (unit > 1.9) unit = 1.9;
    const totalW = unit * nodes.length + GAP * (nodes.length - 1);
    let x = MX + (AVAIL - totalW) / 2;
    nodes.forEach((n, i) => {
      drawNode(slide, n, x, y, unit);
      n._x = x; n._w = unit; n._y = y;
      if (i < nodes.length - 1) hArrow(slide, x + unit, y + NODE_H / 2, GAP);
      x += unit + GAP;
    });
    // conector serpentina: última caixa da linha r-1 → primeira da linha r
    if (r > 0) {
      const prev = rows[r - 1][rows[r - 1].length - 1];
      const cur = nodes[0];
      const x1 = prev._x + prev._w / 2, y1 = prev._y + NODE_H;
      const x2 = cur._x + cur._w / 2, y2 = y;
      const midY = y1 + (y2 - y1) / 2;
      slide.addShape(pres.shapes.LINE, { x: x1, y: y1, w: 0, h: midY - y1, line: { color: ARROW, width: 1.5 } });
      slide.addShape(pres.shapes.LINE, { x: x2, y: midY, w: x1 - x2, h: 0, line: { color: ARROW, width: 1.5 } });
      slide.addShape(pres.shapes.LINE, { x: x2, y: midY, w: 0, h: y2 - midY - 0.03, line: { color: ARROW, width: 1.5, endArrowType: "triangle" } });
    }
  });
}

function legend(slide, hasGate) {
  const y = 5.08, h = 0.12;
  const items = [
    { fill: SAGE, line: null, label: "entrada", adv: 1.05 },
    { fill: WHITE, line: { color: BORDER, width: 1 }, label: "etapa automática", adv: 1.55 },
  ];
  if (hasGate) items.push({ fill: AMBER_TINT, line: { color: AMBER, width: 1, dashType: "dash" }, label: "aprovação humana", adv: 1.6 });
  items.push({ fill: INK, line: null, label: "saída / destino", adv: 1.3 });
  let x = 0.55;
  items.forEach((it) => {
    const o = { x, y, w: 0.18, h, fill: { color: it.fill } };
    if (it.line) o.line = it.line;
    slide.addShape(pres.shapes.RECTANGLE, o);
    slide.addText(it.label, { x: x + 0.23, y: y - 0.05, w: it.adv - 0.2, h: 0.22, fontSize: 7.5, fontFace: F_BODY, color: MUTED, margin: 0, valign: "middle" });
    x += it.adv + 0.23;
  });
}

function note(slide, symbol, text, y) {
  slide.addText([
    { text: symbol + "  ", options: { fontSize: 9.5, color: ACCENT, bold: true } },
    { text, options: { fontSize: 9, color: MUTED } },
  ], { x: 0.55, y, w: 8.9, h: 0.22, fontFace: F_BODY, margin: 0, valign: "middle" });
}

function processSlide(p) {
  const s = pres.addSlide({ masterName: "LIGHT" });
  kickerTitle(s, p.kicker, p.title, p.desc);
  metaColumn(s, p.cmd, p.meta);
  const twoRows = p.rows.length > 1;
  flow(s, p.rows, twoRows ? 2.18 : 2.85);
  if (p.note) note(s, p.noteSym || "↺", p.note, twoRows ? 4.8 : 4.45);
  const hasGate = p.rows.some((r) => r.some((n) => n.type === "gate"));
  legend(s, hasGate);
  return s;
}

// ============================================================
// 1 — CAPA (dark)
// ============================================================
{
  const s = pres.addSlide({ masterName: "DARK" });
  s.addText("GRUPO ELIFE — TIME DE CONTEÚDO", { x: 0.7, y: 1.05, w: 8.5, h: 0.3, fontSize: 10, bold: true, charSpacing: 3, fontFace: F_BODY, color: "5FD3B8", margin: 0 });
  s.addText("Automação de conteúdo", { x: 0.65, y: 1.4, w: 8.8, h: 0.85, fontSize: 40, bold: true, fontFace: F_TITLE, color: DARK_TXT, margin: 0 });
  s.addText("O que já roda sozinho, como cada processo funciona e o que vem a seguir.", { x: 0.7, y: 2.32, w: 7.5, h: 0.35, fontSize: 13, fontFace: F_BODY, color: DARK_MUT, margin: 0 });
  s.addText("11 de junho de 2026", { x: 0.7, y: 2.78, w: 4, h: 0.3, fontSize: 10, fontFace: F_BODY, color: DARK_MUT, margin: 0 });

  // fluxo-fantasma decorativo (motivo do deck)
  const gy = 4.15, gw = 1.7, gh = 0.62, ggap = 0.42;
  let gx = 0.7;
  const ghost = [
    { line: { color: "33493F", width: 1 } },
    { line: { color: "33493F", width: 1 } },
    { line: { color: "7A5A28", width: 1, dashType: "dash" } },
    { fill: { color: "1E3A31" }, line: { color: "2E5A4C", width: 1 } },
  ];
  ghost.forEach((g, i) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: gx, y: gy, w: gw, h: gh, rectRadius: 0.06, fill: g.fill ? g.fill : { color: DARK }, line: g.line });
    if (i < ghost.length - 1) s.addShape(pres.shapes.LINE, { x: gx + gw + 0.05, y: gy + gh / 2, w: ggap - 0.1, h: 0, line: { color: "33493F", width: 1.25, endArrowType: "triangle" } });
    gx += gw + ggap;
  });
  s.addText("pesquisa → criação → aprovação humana → entrega", { x: 0.7, y: gy + gh + 0.12, w: 7.9, h: 0.25, fontSize: 8.5, fontFace: F_MONO, color: "7E948A", margin: 0 });
}

// ============================================================
// 2 — VISÃO GERAL
// ============================================================
{
  const s = pres.addSlide({ masterName: "LIGHT" });
  kickerTitle(s, "Onde estamos", "O que já roda hoje", null);

  const stats = [
    ["11", "processos automatizados", ["10 no agente inhouse", "1 no Make (blog)"]],
    ["4", "marcas atendidas", ["Buzzmonitor · Buzzcreators", "Cxpress · Elife"]],
    ["3", "idiomas nativos", ["PT-BR · ES-LATAM · PT-PT"]],
    ["40+", "comandos prontos", ["pipelines completos", "e etapas avulsas"]],
  ];
  let sy = 1.42;
  stats.forEach((st) => {
    s.addText(st[0], { x: 0.55, y: sy, w: 1.05, h: 0.55, fontSize: 28, bold: true, fontFace: F_TITLE, color: ACCENT, margin: 0, align: "left" });
    const runs = [{ text: st[1], options: { fontSize: 10.5, bold: true, color: INK, breakLine: true } }];
    st[2].forEach((ln, i) => runs.push({ text: ln, options: { fontSize: 8, color: MUTED, breakLine: i < st[2].length - 1 } }));
    s.addText(runs, { x: 1.62, y: sy + 0.03, w: 1.9, h: 0.9, fontFace: F_BODY, margin: 0, valign: "top" });
    sy += 0.95;
  });

  const procs = [
    ["Newsletters", "pipeline semanal completo"],
    ["Posts de blog", "via Make (externo)"],
    ["Pauta Quente", "notícia → N peças"],
    ["Redes sociais", "calendário mensal"],
    ["Copywriting", "3 variações revisadas"],
    ["Tradução", "PT-PT · ES-LATAM"],
    ["Criativos", "estático e carrossel"],
    ["Landing pages", "da copy ao ar"],
    ["Webinar perpétuo", "evento diário automático"],
    ["Meta Ads", "análise read-only"],
    ["Dashboards CM", "funil semanal por marca"],
  ];
  const gx0 = 3.6, cw = 2.85, ch = 0.55, gpx = 0.16, gpy = 0.12;
  procs.forEach((p, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = gx0 + col * (cw + gpx), y = 1.28 + row * (ch + gpy);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: cw, h: ch, rectRadius: 0.05, fill: { color: WHITE }, line: { color: BORDER, width: 1 } });
    s.addText(String(i + 1).padStart(2, "0"), { x: x + 0.12, y, w: 0.32, h: ch, fontSize: 8, fontFace: F_MONO, color: ACCENT, margin: 0, valign: "middle" });
    s.addText([
      { text: p[0], options: { fontSize: 10.5, bold: true, color: INK, breakLine: true } },
      { text: p[1], options: { fontSize: 8, color: MUTED } },
    ], { x: x + 0.5, y, w: cw - 0.62, h: ch, fontFace: F_BODY, margin: 0, valign: "middle" });
  });
}

// ============================================================
// 3..12 — PROCESSOS
// ============================================================
processSlide({
  kicker: "Processo 01 · Editorial",
  title: "Newsletters semanais",
  desc: "Newsletter noticiosa por marca e região, com eixo no blog próprio. Quando a pesquisa aponta lacuna de pauta, o agente propõe o tema e espera aprovação antes de criar o post.",
  cmd: "/news-pipeline",
  meta: [["marcas", "as 4 do grupo"], ["idiomas", "PT-BR · ES-LATAM · PT-PT"], ["saída", "Notion (Entregas)"]],
  rows: [
    [
      { t: "Pesquisa", c: "dores + blog próprio + clipping PR", type: "src" },
      { t: "Dor da semana", c: "posts-âncora do blog" },
      { t: "Pauta aprovada?", c: "só quando há lacuna", type: "gate" },
      { t: "Post de blog", c: "draft no Notion" },
    ],
    [
      { t: "Newsletter", c: "90% blog · 10–20% imprensa" },
      { t: "Revisão", c: "fact-check · anti-IA · dedupe" },
      { t: "Notion", c: "pronta para disparo", type: "out" },
    ],
  ],
  note: "Cadência semanal agendável por marca e região — uma newsletter por execução.",
});

// --- 4: Blog via Make (fluxo real) ---
processSlide({
  kicker: "Processo 02 · Editorial",
  title: "Posts de blog",
  desc: "Pipeline autônomo no Make.com: sinais de busca e notícias viram pauta inédita, o GPT-4o redige com orientação estratégica e o post chega ao WordPress como rascunho — nada vai ao ar sem revisão humana.",
  cmd: "Make.com (orquestrador)",
  meta: [["geração", "OpenAI GPT-4o"], ["memória", "Supabase"], ["publicação", "WordPress (REST API)"]],
  rows: [
    [
      { t: "Sinais", c: "Google Trends + Google News RSS", type: "src" },
      { t: "Checagem de temas", c: "Supabase: já publicado?" },
      { t: "Redação GPT-4o", c: "com orientação estratégica" },
      { t: "Memória", c: "grava o tema no Supabase" },
    ],
    [
      { t: "WordPress", c: "rascunho via REST API" },
      { t: "Revisão humana", c: "antes de ir ao ar", type: "gate" },
      { t: "Blog no ar", c: "post publicado", type: "out" },
    ],
  ],
  note: "Complementar, no agente: /news-criar-post cria posts de apoio à newsletter (draft no Notion).",
  noteSym: "↳",
});

processSlide({
  kicker: "Processo 03 · Editorial",
  title: "Pauta Quente",
  desc: "Transforma uma notícia recente em várias peças de uma vez — todos os formatos × todos os idiomas pedidos — com fonte primária rastreada e conector com o produto.",
  cmd: "/pauta-quente",
  meta: [["entrada", "1 notícia (URL)"], ["saída", "N peças (tipos × idiomas)"], ["destino", "Notion"]],
  rows: [[
    { t: "Notícia", c: "URL recente", type: "src" },
    { t: "Fonte primária", c: "rastreio + verificação" },
    { t: "Ângulo da marca", c: "edutainment + produto" },
    { t: "Multiformato", c: ["carrossel · vídeo · blog", "LinkedIn · email"] },
    { t: "Multi-idioma", c: "BR · PT · ES" },
    { t: "Notion", c: "Entregas, por marca", type: "out" },
  ]],
  note: "Exemplo: 1 notícia vira carrossel + blog + email em 3 idiomas — 9 peças numa execução.",
  noteSym: "→",
});

processSlide({
  kicker: "Processo 04 · Editorial",
  title: "Redes sociais",
  desc: "Planejamento editorial mensal da Buzzmonitor para LinkedIn, Instagram e Facebook — pesquisa de referências, tendências do nicho e calendário detalhado por rede.",
  cmd: "/social-plan",
  meta: [["escopo", "Buzzmonitor BR"], ["redes", "LinkedIn · IG · FB"], ["saída", "Notion (Redes Sociais)"]],
  rows: [[
    { t: "Pesquisa", c: "perfis de referência + tendências virais", type: "src" },
    { t: "Calendário mensal", c: "3 posts/semana por rede" },
    { t: "Copy dos posts", c: "via /copy-criar, por tema" },
    { t: "Notion", c: "calendário publicado", type: "out" },
  ]],
  note: "Expansão para as demais marcas está no radar (ver próximos passos).",
  noteSym: "→",
});

processSlide({
  kicker: "Processo 05 · Criação",
  title: "Copywriting",
  desc: "Criação de copy nativa por marca, região, formato e estágio de funil — sempre 3 variações com hooks e premissas diferentes, revisadas contra a base de produto.",
  cmd: "/copy-criar · /copy-revisar",
  meta: [["formatos", "vídeo curto · estático · email"], ["funil", "ToFu · MoFu · BoFu"], ["base", "conhecimento/copywriting"]],
  rows: [[
    { t: "Briefing", c: "marca · região · formato · funil", type: "src" },
    { t: "Referências", c: "pesquisa fresca + swipe file" },
    { t: "3 variações", c: "hooks e ângulos distintos" },
    { t: "Revisão", c: "técnica · produto · anti-IA" },
    { t: "Copy final", c: "pronta para usar", type: "out" },
  ]],
  note: "Boas referências ficam guardadas e pesquisáveis num swipe file próprio (/copy-swipefile).",
});

processSlide({
  kicker: "Processo 06 · Criação",
  title: "Tradução de copy",
  desc: "Tradução que soa escrita por nativo, não traduzida — com padrões linguísticos por região (ex.: tratamento por “você” em PT-PT, vocabulário local em ES-LATAM).",
  cmd: "/trad-pipeline",
  meta: [["origem", "PT-BR"], ["destinos", "PT-PT · ES-LATAM"], ["saída", "Notion (Entregas)"]],
  rows: [[
    { t: "Copy PT-BR", c: "arquivo ou texto", type: "src" },
    { t: "Tradução nativa", c: "PT-PT ou ES-LATAM" },
    { t: "Revisão de nativo", c: "naturalidade · precisão · comprimento" },
    { t: "Notion", c: "versão final", type: "out" },
  ]],
  note: "/trad-calibrar renova os padrões periodicamente pesquisando sites e veículos nativos.",
});

processSlide({
  kicker: "Processo 07 · Ativos",
  title: "Criativos (imagens)",
  desc: "Imagens de criativo ponta a ponta — estático ou carrossel, orgânico ou anúncio — nos 3 formatos, com brandbook aplicado e safe-zones do Meta quando é anúncio.",
  cmd: "/criativo",
  meta: [["engines", "HTML pixel-perfect · Bloom (IA)"], ["formatos", "1:1 · 4:5 · 9:16"], ["uso", "orgânico · anúncio"]],
  rows: [[
    { t: "Copy aprovada", c: "de /copy-criar, Pauta Quente ou colada", type: "src" },
    { t: "Adaptação", c: "diagramação" },
    { t: "Brandbook", c: "tokens + guidelines" },
    { t: "Geração", c: "HTML ou Bloom (IA)" },
    { t: "Revisão visual", c: "corrige e re-renderiza" },
    { t: "Pasta local", c: "PNGs por formato", type: "out" },
  ]],
  note: "Texto pixel-perfect na engine HTML; contraste WCAG corrigido automaticamente.",
});

{
  const s = processSlide({
    kicker: "Processo 08 · Ativos",
    title: "Landing pages",
    desc: "Da copy crua à página no ar: estruturação anti-IA, geração com identidade da marca, auditoria dupla de design e publicação com validação automática.",
    cmd: "/lp-pipeline",
    meta: [["marcas", "as 4 do grupo"], ["domínios", "guarda-chuva por marca"], ["saída", "Vercel + relatório no Notion"]],
    rows: [
      [
        { t: "Copy crua", c: "Notion · arquivo · texto", type: "src" },
        { t: "Preparar", c: "blocos rotulados + anti-IA" },
        { t: "Gerar HTML", c: "brand tokens + guidelines" },
        { t: "Revisar", c: "design + acessibilidade" },
      ],
      [
        { t: "Aprovação", c: "design validado", type: "gate" },
        { t: "Form real", c: "Jotform · RD · HubSpot" },
        { t: "Vercel", c: "deploy + PageSpeed + smoke test", type: "out" },
      ],
    ],
    note: "*estimativa: ~16 h manuais (copy, design, dev, QA) vs ~1 h com o agente, por LP — /lp-health-check vigia tudo diariamente.",
    noteSym: "⊙",
  });
  // stats: LPs no ar + horas economizadas (na coluna direita, abaixo dos pares)
  s.addText([
    { text: "23", options: { fontSize: 15, bold: true, fontFace: F_TITLE, color: ACCENT, breakLine: false } },
    { text: "  LPs no ar no Vercel", options: { fontSize: 9.5, fontFace: F_BODY, color: INK } },
  ], { x: 7.0, y: 1.6, w: 2.45, h: 0.26, margin: 0, valign: "middle" });
  s.addText([
    { text: "~370 h", options: { fontSize: 15, bold: true, fontFace: F_TITLE, color: ACCENT, breakLine: false } },
    { text: "  economizadas*", options: { fontSize: 9.5, fontFace: F_BODY, color: INK } },
  ], { x: 7.0, y: 1.9, w: 2.45, h: 0.26, margin: 0, valign: "middle" });
}

processSlide({
  kicker: "Processo 09 · Ativos",
  title: "Webinar perpétuo",
  desc: "Um webinar gravado uma única vez vira evento diário: a LP criada pelo agente inscreve direto na API do ClickMeeting, que transmite a sessão todos os dias e dispara os lembretes sozinha.",
  cmd: "/lp-pipeline + ClickMeeting",
  meta: [["inscrição", "LP → API ClickMeeting"], ["cadência", "diária (gravado 1x)"], ["e-mails", "pré e pós evento, automáticos"]],
  rows: [[
    { t: "LP de inscrição", c: "criada pelo agente", type: "src" },
    { t: "API ClickMeeting", c: "form inscreve direto" },
    { t: "Transmissão diária", c: "mesma sessão gravada" },
    { t: "E-mails automáticos", c: "lembrete pré + pós evento" },
    { t: "Lead aquecido", c: "pronto p/ Ads + outbound", type: "out" },
  ]],
  note: "Próximos: concluir a configuração para todas as marcas e regiões + gravar webinars curtos por dor + solução, conectando Ads e outbound.",
  noteSym: "→",
});

{
  const s = processSlide({
    kicker: "Processo 10 · Análise",
    title: "Meta Ads",
    desc: "Leitura de performance das contas Buzzmonitor e Cxpress — tendências, comparação de janelas e diagnóstico por criativo. Somente leitura: nunca altera campanhas.",
    cmd: "/meta-ads · /meta-ads-trends",
    meta: [["contas", "6 (Buzz + Cxpress)"], ["janelas", "7 · 15 · 30 dias"], ["cross-check", "/bunzzai (via CRM)"]],
    rows: [[
      { t: "Meta API", c: "6 contas · BRL USD EUR", type: "src" },
      { t: "Coleta local", c: "campanhas + insights" },
      { t: "Análise", c: "CpL · CTR · frequência" },
      { t: "Relatório", c: "conta · funil · adset · ad" },
      { t: "Notion", c: "consolidado das contas", type: "out" },
    ]],
    note: "537 = ads únicos com veiculação real (impressões > 0), 01/01 a 11/06, via Meta API — cross-check independente via /bunzzai.",
    noteSym: "⇄",
  });
  // faixa de stats: ads veiculados em 2026 (contas Buzzmonitor)
  s.addText("ADS VEICULADOS EM 2026 — CONTAS BUZZMONITOR", {
    x: 0.55, y: 1.96, w: 6.5, h: 0.2, fontSize: 7.5, bold: true, charSpacing: 2,
    fontFace: F_BODY, color: MUTED, margin: 0,
  });
  const ads = [
    ["537", ["total no ano", "60 campanhas"]],
    ["175", ["Brasil", "R$ 117,4 mil"]],
    ["267", ["LATAM", "US$ 29,2 mil"]],
    ["95", ["Portugal", "€ 6,5 mil"]],
  ];
  ads.forEach((a, i) => {
    const bx = 0.55 + i * 2.225;
    if (i > 0) s.addShape(pres.shapes.LINE, { x: bx - 0.18, y: 2.22, w: 0, h: 0.42, line: { color: BORDER, width: 1 } });
    s.addText(a[0], { x: bx, y: 2.2, w: 0.88, h: 0.46, fontSize: 20, bold: true, fontFace: F_TITLE, color: ACCENT, margin: 0, valign: "middle" });
    s.addText([
      { text: a[1][0], options: { fontSize: 8, bold: true, color: INK, breakLine: true } },
      { text: a[1][1], options: { fontSize: 8, color: MUTED } },
    ], { x: bx + 0.92, y: 2.2, w: 1.15, h: 0.46, fontFace: F_BODY, margin: 0, valign: "middle" });
  });
}

{
  const s = pres.addSlide({ masterName: "LIGHT" });
  kickerTitle(s, "Processo 11 · Análise", "Dashboards CM",
    "KPIs semanais do funil de leads e fechamentos por marca, direto do CRM. Buzzmonitor BR e LATAM no ar; Cxpress calibrada e pronta em ambiente local.");
  metaColumn(s, "/dashboard-atualizar", [["no ar", "Buzz BR · LATAM"], ["em local", "Cxpress"], ["auditoria", "/auditar-deals-cm"]]);
  flow(s, [[
    { t: "Supabase", c: "funil de leads + fechamentos", type: "src" },
    { t: "Gerador Python", c: "KPIs por período" },
    { t: "Confirmação", c: "fechamentos novos", type: "gate" },
    { t: "Deploy Vercel", c: "fora do repo · Basic Auth" },
    { t: "Validação", c: "HTTP + login" },
    { t: "Dashboard live", c: "atualização semanal", type: "out" },
  ]], 2.22);

  // print real da dashboard + legenda ao lado
  s.addImage({ path: "C:/Users/titof/Downloads/Claude/Agente Inhouse/apresentacoes/assets/dash-bm-brasil.png", x: 0.55, y: 3.42, w: 2.32, h: 1.45 });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y: 3.42, w: 2.32, h: 1.45, fill: { color: WHITE, transparency: 100 }, line: { color: BORDER, width: 1 } });
  s.addText("DASHBOARD AO VIVO — BUZZMONITOR BRASIL", { x: 3.12, y: 3.46, w: 6.3, h: 0.2, fontSize: 7.5, bold: true, charSpacing: 2, fontFace: F_BODY, color: MUTED, margin: 0 });
  s.addText("dashboard-buzzmonitor-brasil.vercel.app", { x: 3.12, y: 3.68, w: 6.3, h: 0.24, fontSize: 10, fontFace: F_MONO, color: ACCENT, margin: 0, bold: true });
  s.addText("Visão da semana, do mês e do acumulado do ano — leads, reuniões, propostas, fechamentos e perdidos, atualizada semanalmente.", { x: 3.12, y: 3.98, w: 6.3, h: 0.42, fontSize: 9, fontFace: F_BODY, color: MUTED, margin: 0, valign: "top" });
  s.addText([
    { text: "⊙  ", options: { fontSize: 9.5, color: ACCENT, bold: true } },
    { text: "/auditar-deals-cm recupera deals que somem por UTM vazia — read-only, nunca grava no CRM.", options: { fontSize: 9, color: MUTED } },
  ], { x: 3.12, y: 4.55, w: 6.3, h: 0.22, fontFace: F_BODY, margin: 0, valign: "middle" });
  legend(s, true);
}

// ============================================================
// 13 — GOVERNANÇA
// ============================================================
{
  const s = pres.addSlide({ masterName: "LIGHT" });
  kickerTitle(s, "Como roda sem quebrar", "Governança embutida",
    "Automação com freios: tudo o que o agente produz passa por revisão, versionamento e monitoramento.");
  const cards = [
    ["Nada vai direto pra main", "/commit abre branch + pull request; revisão humana antes de entrar"],
    ["PRs revisados com método", "/pull-request-review gera relatório em 3 níveis de severidade"],
    ["Skills versionadas", "semver + changelog a cada mudança de comportamento"],
    ["Humano no circuito", "aprovações de pauta, design de LP e fechamentos de dashboard"],
    ["Monitoramento contínuo", "health check diário de LPs + validação pós-deploy"],
    ["Onboarding guiado", "/setup-agencia leva do zero à primeira skill rodando"],
  ];
  const cw = 2.86, ch = 1.18, gpx = 0.16, gpy = 0.22, x0 = 0.55, y0 = 2.12;
  cards.forEach((c, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = x0 + col * (cw + gpx), y = y0 + row * (ch + gpy);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: cw, h: ch, rectRadius: 0.05, fill: { color: WHITE }, line: { color: BORDER, width: 1 } });
    s.addShape(pres.shapes.RECTANGLE, { x: x + 0.16, y: y + 0.17, w: 0.12, h: 0.12, fill: { color: ACCENT } });
    s.addText([
      { text: c[0], options: { fontSize: 10.5, bold: true, color: INK, breakLine: true } },
      { text: c[1], options: { fontSize: 8.5, color: MUTED } },
    ], { x: x + 0.16, y: y + 0.36, w: cw - 0.32, h: ch - 0.46, fontFace: F_BODY, margin: 0, valign: "top", paraSpaceAfter: 4 });
  });
}

// ============================================================
// 14 — PRÓXIMOS PASSOS (dark)
// ============================================================
{
  const s = pres.addSlide({ masterName: "DARK" });
  s.addText("O QUE VEM AGORA", { x: 0.7, y: 0.45, w: 6, h: 0.3, fontSize: 9.5, bold: true, charSpacing: 2.5, fontFace: F_BODY, color: "5FD3B8", margin: 0 });
  s.addText("Próximas automações", { x: 0.67, y: 0.7, w: 8, h: 0.6, fontSize: 26, bold: true, fontFace: F_TITLE, color: DARK_TXT, margin: 0 });
  s.addText("Lista-rascunho para validarmos nesta reunião — prioridades em aberto.", { x: 0.7, y: 1.32, w: 7.5, h: 0.3, fontSize: 10.5, fontFace: F_BODY, color: DARK_MUT, margin: 0 });

  const cols = [
    [
      ["PESSOAS", "amber", "Treinar o time para escala", "capacitar mais gente pra rodar os pipelines"],
      ["BUNZZAI", "teal", "Análise de Meta Ads via BunzzAI", "desempenho analisado automaticamente"],
      ["BUNZZAI", "teal", "Subir novos ads via BunzzAI", "criar e publicar campanhas pelo agente"],
      ["MELHORIA", "teal", "Aprimorar blogpost e newsletter", "evoluir os dois pipelines que já rodam"],
      ["ORQUESTR.", "teal", "Pauta Quente auto-sugerida", "orquestrador propõe, agente gera as peças"],
      ["EXPANSÃO", "teal", "Webinars em todas as marcas", "roteiros por dor + solução · Ads e outbound"],
    ],
    [
      ["PRONTO", "teal", "Dashboard Cxpress no ar", "pronta em local; falta deploy + skill"],
      ["DECISÃO", "amber", "Cadência autônoma", "newsletter semanal + health check diário"],
      ["EXPANSÃO", "teal", "Redes sociais multi-marca", "hoje cobre só a Buzzmonitor"],
      ["DESENHADO", "teal", "Auditoria de deals — fase 2", "ActiveCampaign; espec. pronta no repo"],
      ["INSUMO", "amber", "Cases reais da Cxpress", "destrava prova social em copy e LP BoFu"],
    ],
  ];
  cols.forEach((items, ci) => {
    const cx = ci === 0 ? 0.7 : 5.15;
    let y = 1.72;
    items.forEach((it) => {
      const teal = it[1] === "teal";
      s.addText(it[0], {
        shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.03,
        x: cx, y: y + 0.01, w: 1.05, h: 0.24, fill: { color: teal ? "16352D" : "3A2C16" },
        fontSize: 6.5, bold: true, fontFace: F_MONO, color: teal ? "5FD3B8" : "E8B25C",
        align: "center", valign: "middle", margin: 0.02,
      });
      s.addText(it[2], { x: cx + 1.2, y, w: 2.95, h: 0.26, fontSize: 10, bold: true, fontFace: F_BODY, color: DARK_TXT, margin: 0, valign: "middle" });
      s.addText(it[3], { x: cx + 1.2, y: y + 0.27, w: 2.95, h: 0.2, fontSize: 8, fontFace: F_BODY, color: DARK_MUT, margin: 0, valign: "top" });
      y += 0.58;
    });
  });

  s.addText([
    { text: "teal", options: { fontSize: 8, bold: true, color: "5FD3B8", breakLine: false } },
    { text: " = frente encaminhada ou no roadmap técnico", options: { fontSize: 8, color: DARK_MUT, breakLine: false } },
    { text: "        ", options: { fontSize: 8, color: DARK_MUT, breakLine: false } },
    { text: "âmbar", options: { fontSize: 8, bold: true, color: "E8B25C", breakLine: false } },
    { text: " = depende de decisão ou insumo do time", options: { fontSize: 8, color: DARK_MUT } },
  ], { x: 0.7, y: 5.26, w: 8.5, h: 0.25, fontFace: F_BODY, margin: 0 });
}

pres.writeFile({ fileName: "C:/Users/titof/Downloads/Claude/Agente Inhouse/apresentacoes/automacao-conteudo-grupo-elife.pptx" })
  .then(() => console.log("OK: pptx gerado"))
  .catch((e) => { console.error(e); process.exit(1); });
