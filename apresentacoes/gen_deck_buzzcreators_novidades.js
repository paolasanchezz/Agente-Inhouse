// Apresentação: Novidades Buzzcreators (2026-08)
// Gera buzzcreators-novidades-2026-08.pptx — 16:9 wide, brand Buzzcreators.
// Prints em assets/bc-*.png
const pptxgen = require("pptxgenjs");
const path = require("path");

// ---------- paleta (brand/buzzcreators/tokens.json) ----------
const ROXO = "3A1652";        // colors.primary
const ROXO_CARD = "4A2168";   // card sobre fundo roxo
const ROXO_LT = "6A3895";     // colors.primaryLight
const LARANJA = "FF8119";     // colors.secondary
const WHITE = "FFFFFF";
const MUTED = "4A4A4A";       // neutral.700
const BORDER = "E3E7EB";
const LILAS = "C9B6DE";       // texto suave sobre roxo
const LILAS_DIM = "A492BC";

// A fonte da marca (DM Sans) e variavel: o PowerPoint renderiza condensado e com
// glifos colados, e a maioria das maquinas nao tem a fonte instalada. Usamos o par
// seguro Arial (titulos) + Calibri (corpo), que renderiza igual em Windows e Mac.
const F_HEAD = "Arial";
const F_BODY = "Calibri";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.author = "Buzzcreators";
pres.title = "Novidades Buzzcreators";

// Por padrao usa os prints em qualidade cheia. Com DECK_ASSETS apontando pra outra
// pasta (e DECK_SHOT3 pro nome do 3o print), gera a versao leve pra upload via API.
const ASSETS = process.env.DECK_ASSETS || path.join(__dirname, "assets");
const SHOT1 = process.env.DECK_SHOT1 || "bc-search-creators.png";
const SHOT2 = process.env.DECK_SHOT2 || "bc-links-parametrizados.png";
const SHOT3 = process.env.DECK_SHOT3 || "bc-aprovacao-post.png";
const OUTFILE = process.env.DECK_OUT || path.join(__dirname, "buzzcreators-novidades-2026-08.pptx");

// ---------- helpers ----------

// círculo numerado — motivo visual repetido em todos os slides
function numCircle(slide, n, x, y, d, filled) {
  slide.addShape(pres.shapes.OVAL, {
    x, y, w: d, h: d,
    fill: filled ? { color: LARANJA } : { color: ROXO },
    line: filled ? { color: LARANJA, width: 0 } : { color: LILAS_DIM, width: 1 },
  });
  slide.addText(n, {
    x, y, w: d, h: d,
    fontSize: 10, bold: true, fontFace: F_HEAD,
    color: filled ? WHITE : LILAS,
    align: "center", valign: "middle", margin: 0,
  });
}

// cabeçalho dos slides de feature
function featureHeader(slide, n, title, desc, x, w, y, titleSize, descW) {
  const d = 0.32;
  numCircle(slide, n, x, y, d, true);
  slide.addText("JÁ NO AR", {
    x: x + 0.48, y, w: 3.0, h: d,
    fontSize: 10, bold: true, charSpacing: 2.6, fontFace: F_HEAD,
    color: LARANJA, valign: "middle", margin: 0,
  });
  slide.addText(title, {
    x, y: y + 0.48, w, h: 0.66,
    fontSize: titleSize || 32, bold: true, fontFace: F_HEAD, color: ROXO, margin: 0, valign: "top",
  });
  slide.addText(desc, {
    x, y: y + 1.24, w: descW || w, h: 1.5,
    fontSize: 13, fontFace: F_BODY, color: MUTED, lineSpacing: 20, margin: 0, valign: "top",
  });
}

// print dentro de um card branco com sombra suave
function shot(slide, file, x, y, w, h) {
  const pad = 0.14;
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: x - pad, y: y - pad, w: w + pad * 2, h: h + pad * 2,
    rectRadius: 0.08,
    fill: { color: WHITE },
    line: { color: BORDER, width: 1 },
    shadow: { type: "outer", color: ROXO, opacity: 0.16, blur: 14, offset: 3, angle: 90 },
  });
  slide.addImage({ path: path.join(ASSETS, file), x, y, w, h });
}

// ============================================================
// SLIDE 1 — resumo
// ============================================================
const s1 = pres.addSlide();
s1.background = { color: ROXO };

s1.addText("BUZZCREATORS", {
  x: 0.7, y: 0.62, w: 6, h: 0.3,
  fontSize: 10.5, bold: true, charSpacing: 2.8, fontFace: F_HEAD, color: LARANJA, margin: 0,
});
s1.addText("O que mudou na plataforma", {
  x: 0.7, y: 0.98, w: 11.9, h: 0.76,
  fontSize: 38, bold: true, fontFace: F_HEAD, color: WHITE, margin: 0, valign: "top",
});
s1.addText("Quatro entregas já disponíveis e três em construção para este trimestre.", {
  x: 0.7, y: 1.82, w: 9.5, h: 0.4,
  fontSize: 13.5, fontFace: F_BODY, color: LILAS, margin: 0, valign: "top",
});

const CARD_Y = 2.44, CARD_H = 4.42;

// --- card esquerdo: já no ar ---
s1.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.7, y: CARD_Y, w: 6.15, h: CARD_H, rectRadius: 0.1,
  fill: { color: ROXO_CARD }, line: { color: ROXO_CARD, width: 0 },
});
s1.addText("JÁ NO AR", {
  x: 1.08, y: CARD_Y + 0.3, w: 4.5, h: 0.32,
  fontSize: 11, bold: true, charSpacing: 2.6, fontFace: F_HEAD, color: LARANJA, margin: 0, valign: "middle",
});

const jaNoAr = [
  ["Search de Creators", "Busca por perfis semelhantes e faixa de seguidores."],
  ["Links parametrizados", "UTMs na campanha, um link por creator."],
  ["Aprovação de post", "Revisão do conteúdo antes de ir ao ar."],
  ["Link público de campanha", "Convite aberto para creators de fora da base."],
];
jaNoAr.forEach(([label, desc], i) => {
  const y = CARD_Y + 0.94 + i * 0.82;
  numCircle(s1, String(i + 1).padStart(2, "0"), 1.08, y, 0.34, true);
  s1.addText(label, {
    x: 1.62, y: y - 0.05, w: 4.9, h: 0.32,
    fontSize: 14, bold: true, fontFace: F_HEAD, color: WHITE, margin: 0, valign: "middle",
  });
  s1.addText(desc, {
    x: 1.62, y: y + 0.27, w: 4.9, h: 0.3,
    fontSize: 11, fontFace: F_BODY, color: LILAS, margin: 0, valign: "middle",
  });
});

// --- card direito: chega neste trimestre ---
s1.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 7.18, y: CARD_Y, w: 5.45, h: CARD_H, rectRadius: 0.1,
  fill: { color: ROXO }, line: { color: ROXO_LT, width: 1 },
});
s1.addText("CHEGA NESTE TRIMESTRE", {
  x: 7.56, y: CARD_Y + 0.3, w: 4.6, h: 0.32,
  fontSize: 11, bold: true, charSpacing: 2.6, fontFace: F_HEAD, color: LILAS, margin: 0, valign: "middle",
});

const vemAi = [
  ["Pagamento variável", "Remuneração por resultado, além do valor fixo."],
  ["Monitoramento de cupom", "Vendas geradas pelo cupom de cada creator."],
  ["Campanhas “Always On”", "Relação contínua com embaixadores da marca."],
];
vemAi.forEach(([label, desc], i) => {
  const y = CARD_Y + 1.0 + i * 1.18;
  numCircle(s1, String(i + 1).padStart(2, "0"), 7.56, y, 0.34, false);
  s1.addText(label, {
    x: 8.1, y: y - 0.05, w: 4.2, h: 0.32,
    fontSize: 14, bold: true, fontFace: F_HEAD, color: WHITE, margin: 0, valign: "middle",
  });
  s1.addText(desc, {
    x: 8.1, y: y + 0.27, w: 4.25, h: 0.3,
    fontSize: 11, fontFace: F_BODY, color: LILAS_DIM, margin: 0, valign: "middle",
  });
});

// ============================================================
// SLIDE 2 — Search de Creators (print 1006x494)
// ============================================================
const s2 = pres.addSlide();
s2.background = { color: WHITE };
featureHeader(
  s2, "01", "Search de Creators",
  "Monte uma lista de busca a partir de perfis de referência e de uma faixa de seguidores. Você diz quantos creators quer, a plataforma devolve a lista.",
  0.7, 10.6, 0.62, 32, 8.8
);
{
  const w = 8.2, h = w / (1006 / 494);
  shot(s2, SHOT1, (13.333 - w) / 2, 2.75, w, h);
}

// ============================================================
// SLIDE 3 — Links parametrizados (print 914x802)
// duas colunas: texto à esquerda, print à direita
// ============================================================
const s3 = pres.addSlide();
s3.background = { color: WHITE };
featureHeader(
  s3, "02", "Links parametrizados",
  "As UTMs são definidas uma vez, na campanha. Cada creator recebe o link já parametrizado com o próprio nome, e a conversão chega identificada no seu analytics.",
  0.75, 5.1, 2.42, 28
);
{
  const w = 6.0, h = w / (914 / 802);
  shot(s3, SHOT2, 6.45, (7.5 - h) / 2, w, h);
}

// ============================================================
// SLIDE 4 — Aprovação de post (print 1756x879)
// ============================================================
const s4 = pres.addSlide();
s4.background = { color: WHITE };
featureHeader(
  s4, "03", "Aprove o post antes de ir ao ar",
  "O creator sobe o conteúdo na plataforma. Você assiste, aprova ou pede alterações com um feedback escrito, tudo antes da publicação.",
  0.7, 10.6, 0.62, 32
);
{
  const w = 8.2, h = w / (1756 / 879);
  shot(s4, SHOT3, (13.333 - w) / 2, 2.75, w, h);
}

pres.writeFile({ fileName: OUTFILE })
  .then((f) => console.log("gerado:", f));
