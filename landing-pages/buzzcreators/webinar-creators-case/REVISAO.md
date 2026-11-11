# Revisao LP — buzzcreators/webinar-creators-case

**Data:** 2026-11-11
**Auditores:** passada de design (criterios frontend-design + GUIDELINES) e passada de a11y/HTML (Web Interface Guidelines), as duas feitas pelo agente. Checks deterministicos: `check_gtm_region.py`, `bump_mobile_type.py --dry-run`, grep de em-dash/SEO/ancora, parse do JSON-LD.

## Decisoes preservadas (nao sao achados)

- Form ao lado do hero (override da §10, pedido do briefing). No mobile vem logo depois do subtitulo.
- H1 do briefing, que abre pelo ganho (§3/§5). Alternativa pela dor segue anotada no `copy.txt`.
- `data-perpetuo-next="/webinar-creators-case-confirmado"` no wrapper do form e o registrador no `<script>`.

## Aplicado automaticamente (6 criticos)

- [x] **Indicador do header duplicava o hero (§3).** `<span class="header-meta">Webinar gratuito</span>` repetia o overline "Webinar gratuito · Assista agora" e nao estava no `copy.txt`. Removido, junto com as regras CSS `.header-meta`.
- [x] **Contraste do `.base-tag` ("A base").** Laranja `#ff7300` sobre branco dava ~2,9:1 em texto de 14px (reprova AA). Trocado para `var(--primary)` (`#6a3895`, ~7,6:1).
- [x] **Piso tipografico mobile (§20).** `.urgency h2` passou de `clamp(28px…)` para `clamp(34px…)` e `.final h2` de `clamp(30px…)` para `clamp(34px…)`, porque o MAX e 46px (faixa de display, piso 34px). Desktop nao muda.
- [x] **`pattern` do telefone invalido.** Com a flag `v` (Chrome 114+), `(` e `)` sem escape dentro da classe derrubam o regex e o navegador ignora o pattern. Escapado: `[0-9\(\)\+\s\-]{8,20}`. So afeta o form mock.
- [x] **Ellipsis (§5).** "Liberando acesso..." virou "Liberando acesso…".
- [x] **OG image (§18).** `assets/og-webinar-creators-case.png` gerada em 1200×630 a partir do `og-template.html`, com o `logo-color.png`, o titulo do `og:title` e o overline da copy. Arquivo unico, sem `og-image.png`.

## Checks que passaram

- GTM: `status: ok`, `expected: null`, nada injetado (`tracking.json` da Buzzcreators esta null). Sem `--write-stamp`, que fica pra quando o container existir.
- Em-dash: 0. Fidelidade da copy: todos os textos visiveis batem com o `copy.txt` (aspas curvas sao cosmetica permitida). Sem pull-quote, kicker ou punchline inventada. A frase-ancora do CTA final esta literal.
- SEO: 1 description, 1 robots, 10 `og:`, 4 `twitter:`, 1 JSON-LD (parseia: Organization, WebPage, Event), 1 canonical.
- hreflang: LP unica, sem irmas `-es`/`-pt`. OK omitir.
- Logo: `logo-color.png` (PNG, §19 ok), header e footer apontam pra `https://buzzcreators.com.br` com `target="_blank"`.
- Ancora: o CTA final usa `href="#formulario"`, nenhum JS grava hash e nenhum link absoluto leva `#`. O build do guarda-chuva injeta a trava (§22).
- Secoes-tipo: problema em lista com X vermelho, aprender em grid com ✓, urgencia escura com tag rotacionada (uma vez so), speaker com foto circular.
- `prefers-reduced-motion` desliga transicoes e o scroll suave. Skip-link, labels e `focus-visible` estao presentes.

## Melhorias opcionais (6)

- [ ] **Lista do hero some no mobile** (`.hero-list { display: none }` abaixo de 981px). E consequencia de puxar o form pra cima, e os 4 itens reaparecem mais abaixo na pagina. Se quiser mostrar, da pra colocar a lista depois do form no mobile.
- [ ] **Foto do speaker pesada:** `bruno-filho.png` tem 451 KB para exibir em 200px. Exportar em WebP ou JPG a ~400px deixaria a imagem com menos de 40 KB.
- [ ] **`alt="Foto de Bruno Filho"`:** o "Foto de" e redundante para leitor de tela. Basta `alt="Bruno Filho"`.
- [ ] **JSON-LD e manifest:** `Organization.url` saiu fixo como `https://buzzcreators.com.br`, sem `sameAs`, porque o `brand-manifest.json` nao tem bloco `regions`. Migrar o manifest e regerar.
- [ ] **Organization.url com `{{DOMAIN}}`:** `@id` e `url` estao certos, mas o `logo` depende de `{{BRAND_LOGO_PNG_PATH}}`. Confirmar no build do guarda-chuva que o placeholder resolve.
- [ ] **`bump_mobile_type.py` sugere +1px** em labels e captions (`.eyebrow`, `.form-intro`, `.stat-label`, `.footer` etc.). Todos ja estao no piso de 14px da tabela §20, entao fica opcional.

## Nice-to-haves (2)

- [ ] `.step h3` usa `clamp(22px, 2vw, 22px)`, que na pratica e 22px fixo. Da pra simplificar para `font-size: 22px`.
- [ ] O CTA final usa fundo `neutral-100`. A §8 sugere fundo de destaque, mas aqui a escura e a urgencia logo antes, e duas escuras seguidas pesariam.

## Proximos passos

- Design aprovado? -> `/lp-integrar-form buzzcreators/webinar-creators-case "{snippet do Jotform compartilhado}"`, mantendo o `data-perpetuo-next` do wrapper.
- Publicar o par -> `/lp-publicar buzzcreators webinar-creators-case webinar.buzzmonitor.com`

---

## v2 — redesign pedido pelo time (2026-11-11)

O feedback foi "muito extensa e muito branca", com referencia em `buzzcreators.com.br/gestao-de-influenciadores`. Esta e uma mudanca estrutural pedida pelo time, nao um critico de auditoria. Estrutura nova e decisoes no `README.md`.

Checado na v2:

- [x] Em-dash: 0. Os textos mantidos continuam literais do `copy.txt`, e os cortes estao anotados la.
- [x] 375px: sem scroll lateral, H1 e H2 de urgencia com 34px. Altura da pagina caiu de 7.982px para 6.477px.
- [x] Contraste na faixa roxa: texto branco e `rgba(255,255,255,.86)` sobre `#3a1652`, e laranja `#ff8119` sobre `#3a1652` (~6:1). CTA laranja com texto `#2c1040`.
- [x] Redes no rodape com `aria-label` por rede, icones `aria-hidden` e nova aba.
- [x] CTA comercial com `utm_source=webinar&utm_content=captacao-perpetuo-creators-case` (convencao-utm §2/§3) e sem `#` na URL.
- [x] Politica de privacidade apontando pra `https://buzzmonitor.com.br/privacidade` no form e no rodape.
- [x] O nome do speaker virou `<h3>` dentro da secao de fechamento, que e rotulada pelo H2 da urgencia.
- Itens da v1 que deixaram de valer: "Lista do hero some no mobile" continua igual. "CTA final em neutral-100" e o `.step h3` sairam junto com as secoes cortadas.

---

## Integracao do form (2026-11-11)

- [x] Form mock trocado pelo embed do Jotform `261904654263661` dentro de `<div class="jotform-embed" data-perpetuo-next="/webinar-creators-case-confirmado">`, sem a classe `form` (evita o card dentro do card).
- [x] JS do mock removido (validacao, UTMs em hidden e `redirectToThanks`). Ficou so o registrador do `bmPerpetuoNext`.
- [x] Wrapper CSS canonico `.jotform-embed iframe` adicionado.
- [x] Testado no navegador: o iframe carrega com `parentURL`, o `bmPerpetuoNext` e gravado e nao ha scroll lateral a 375px. Os 404 do console sao o logo do brand, que nao existe no servidor local. **Nenhum envio de teste foi feito**, porque ele criaria um lead real.
- [ ] Decidir se o form compartilhado serve: ele so tem nome, e-mail e empresa, e o opt-out cita a Buzzmonitor (ver README).
- Restos inofensivos: as regras CSS `.field*` do mock seguem no `<style>` sem uso.

---

## v3 — feedback do time (2026-11-11)

- [x] Laranja reduzido a micro-detalhe nas duas paginas (eyebrow, setas, marcador dos pilares e foco de teclado). CTA do fechamento virou botao branco com texto roxo, tag "E no final" branca com texto roxo e destaque do H1 em sublinhado roxo.
- [x] Secao de clientes adicionada antes do fechamento: 4 numeros + logos em 2 imagens com `alt` listando as marcas. A 375px fica sem scroll lateral.
- [x] Numeros da secao de clientes em roxo `#6a3895` sobre branco (~7,6:1). O laranja da imagem original ficaria em ~2,6:1.
- [x] Video da tks conferido no navegador: id `kR0Iq1bFWLc` ("Webinar Buzzcreators"), tocando no mudo a partir de 3:00.
- Nota: no preview local, enviar o Jotform leva para a tks fixa do form no ar (`perpetuo-social-listening-confirmado`, outro video). O despachante de la nao enxerga o destino gravado em `localhost`, porque o `sessionStorage` e por dominio. Em producao as duas paginas ficam em `webinar.buzzmonitor.com` e o encaminhamento funciona. So da para testar esse fluxo depois de publicar.

---

## Form revertido para mock (2026-11-11)

- [x] O Jotform compartilhado `261904654263661` saiu. O time vetou formulario compartilhado com outros webinars, e o form leva o lead para a tks de social listening.
- [x] Form mock restaurado com os 6 campos do briefing. Sairam o `data-perpetuo-next` e o registrador `bmPerpetuoNext`, que so faziam sentido com form compartilhado.
- [x] Fluxo testado no preview: preencher o mock leva para `/webinar-creators-case-confirmado`, com "Pronto, {nome}!" e o video `kR0Iq1bFWLc` tocando no mudo a partir de 3:00.
- [ ] Integrar o Jotform exclusivo quando o time enviar, com a Thank You Page do Jotform apontando direto para a tks.

---

## v5: tks enxuta + revisao anti-IA (/copy-revisar, 2026-11-11)

**Tks:** ficou so titulo + video + botao "Conhecer o Buzzcreators", a pedido do time. A tela final do player troca "Ver o resumo" (a secao saiu) por "Conhecer o Buzzcreators".

**Anti-IA** (regras de `conhecimento/editorial/regras-anti-ia.md`, aplicadas no HTML e no `copy.txt`):
- [x] Trios viraram pares: cenario ("muitas lojas e vendedores..."), influenciador famoso ("Caro e falando com...") e a virada ("conhece o produto e fala como o cliente, com o sotaque da cidade").
- [x] Filler 2.0 removido: "Treinamento de verdade" virou "Treinamento com influenciadores", saiu o "na prática" do Pilar 1 e o "exatamente" do Pilar 3.
- [x] "100% gratuito" saiu do microcopy, que agora diz "Acesso imediato · 12 minutos". Repetia "Webinar gratuito" e "de graça".
- [x] Frase incompleta: "esteja cometendo agora" virou "esteja cometendo esse erro agora".
- [x] Grafia do brandbook: "comunicações da Buzzcreators" virou "do Buzzcreators".
- Contagem final: 0 em-dash nas 2 paginas, 2 antiteses (limite 2), 1 exclamacao, 0 emoji, nenhum filler da lista.
- Mantidos de proposito: o H1 do briefing (trio "sem e-commerce, sem influenciador famoso e sem anúncio"), os 3 caminhos (dado do video) e "O segredo estava atrás do balcão" (gancho aprovado).

---

## v6: sem os 3 caminhos caros (2026-11-11)

- [x] A secao "O cenário / Os 3 caminhos caros" saiu a pedido do time. Influenciador famoso, e-commerce e midia paga nao estao errados; a LP so destaca a estrategia diferente.
- [x] O card "A virada" virou uma secao propria, "A estratégia", com card roxo centralizado e H2 "Essa marca olhou para dentro".
- [x] Texto do card sem comparacao com as outras estrategias: saiu o "Em vez de buscar alguém famoso lá fora". Ficou "A rede percebeu que o vendedor já conhece o produto e fala como o cliente, com o sotaque da cidade. E a audiência dele é o cliente em potencial que mora a 15 minutos da loja."
- [x] Antitese-por-negacao caiu para 1. Em-dash: 0. A 375px fica sem scroll lateral, com H2 de 30px.
- Ainda ha um eco das outras estrategias no H1 do briefing ("sem e-commerce, sem influenciador famoso e sem anúncio"). Mantido porque e o titulo aprovado; trocar se o time quiser tirar toda comparacao.
- [x] Ajuste da v6: o "Em vez de buscar alguém famoso lá fora, ela percebeu que..." voltou ao card, a pedido do time. A antitese-por-negacao volta a 2, no limite.

## v7, form exclusivo (2026-11-11)

- Mock trocado pelo Jotform exclusivo `263146158898674` dentro de `.jotform-embed` (wrapper CSS canonico ja existia). JS do mock removido inteiro. Linha legal do mock removida (o form traz o opt-out). Conferido em 1366px e em largura mobile: iframe ocupa o card sem overflow. Form nao foi submetido (lead real).
