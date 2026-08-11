# Revisao LP — buzzmonitor/teste-de-maturidade

**Data:** 2026-07-29
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel Labs)
**Contexto:** esta LP foi construida inteiramente no Webflow via MCP (varias sessoes de iteracao com o usuario) e depois portada para o pipeline do repositorio para publicacao via Vercel. O design/estrutura ja foi aprovado pelo usuario passo a passo durante a construcao no Webflow — a revisao abaixo trata isso como contexto, nao ignora.

## Aplicado automaticamente (1 critico)

- [x] `scroll-margin-top` ausente no alvo `#quiz` — o nav fixo (80px) cobria o topo da secao ao navegar via ancora (`#quiz`, usado pelo CTA do nav e do hero). Corrigido: adicionado `scroll-margin-top: 96px` ao seletor `.quiz`.

## Excecoes documentadas (desvio deliberado do GUIDELINES.md, aprovado explicitamente pelo usuario)

Estes 3 pontos violam regras gerais do `GUIDELINES.md`, mas foram decisoes explicitas do usuario, tomadas e revisadas repetidas vezes durante a construcao no Webflow. Nao foram revertidos.

- [x] **Beneficios em lista vertical, nao grid** (GUIDELINES §8 pede grid 2-3 colunas para a secao de beneficios, com contraste lista-vs-grid entre problema e beneficio). O usuario pediu explicitamente o formato de lista com numero + texto lado a lado ("estava perfeito", "so mude a copy") apos eu ter tentado o formato em grid de 4 quadrados e ele pedir para reverter.
- [x] **Cards empilhados sem secao de respiro** entre "Quais os beneficios" e "Como funciona" (GUIDELINES §2 recomenda intercalar cards com secoes mais aereas). Pedido explicito: "adicione na mesma dobra mas depois dessa parte, nao modifique o que ja foi feito em nada".
- [x] **Sem secao dedicada de "Problema/contexto"** na estrutura minima (GUIDELINES §6). A copy aprovada pelo usuario nao pede esse bloco separado — o Hero ja contextualiza a dor via texto corrido. Por GUIDELINES §9 ("copy dita estrutura"), nao inventamos secao que a copy nao pede.

## Melhorias opcionais (5)

Para o usuario decidir. Aplicar via Edit manual ou pedir `/lp-revisar` novamente.

- [ ] Contraste do texto branco sobre laranja (`#EB7C2E`) nos botoes `.btn-orange` esta no limite do AA para texto normal (passa como "large text" em bold 14-16px, mas vale confirmar com ferramenta de contraste se quiser robustez extra).
- [ ] `.footer__bottom a` ("Politica de Privacidade e uso de Cookies") aponta para `href="#"` — link morto ate existir uma pagina real de politica.
- [ ] Alt text dos 11 logos de clientes e generico ("Cliente Buzzmonitor" repetido) — poderia nomear cada empresa (Claro, Casas Bahia, Ampla, Salon Line, Visa, Shein, sa365, Globoplay, Hotmart, Mestica, Content House) para SEO/a11y mais precisos.
- [ ] Links do menu do nav ("Recursos", "Planos", "Clientes") apontam para ancoras (`#recursos`, `#planos`, `#clientes`) em `buzzmonitor.com` que nao foram validadas — confirmar se essas secoes existem de fato na home antes de publicar, ou trocar por paginas reais.
- [ ] Sem estilo customizado de `:focus-visible` — o outline padrao do navegador funciona (nao foi removido), mas poderia ganhar um anel on-brand (laranja) para reforcar identidade visual no teclado.

## Nice-to-haves (2)

Estilistico. Ignorar e aceitavel.

- [ ] Hover state (scale/shadow leve) nos `.benefit-card` e `.howworks-card` para reforcar affordance de cartao.
- [ ] `.logos__title` e `.howworks__label` sao `<p>`, nao headings reais — funcional, mas `<h2>`/`<h3>` dariam hierarquia semantica mais robusta.

## Checks mecanicos (todos OK)

- em-dash no HTML: 0
- meta description: 1 | meta robots: 1 | og: 10 | twitter: 4 | JSON-LD: 1 (parseia OK) | canonical: 1
- GTM: `GTM-WFJVK858` (Brasil) presente no `<head>` e `<noscript>`, correto para a regiao
- Logo SVGs (`logo-primary.svg`, `logo-reversed.svg`): 0 `<text>` vivo, raster (base64) — renderizam certo em qualquer navegador
- OG image: `assets/og-image.png`, 1200x630, gerada via Chrome headless
- Logo header/footer: linka para `https://buzzmonitor.com/` (home real da marca), `target="_blank" rel="noopener"` — nao usa `href="/"`

## Proximos passos

- Design ja aprovado (construido e iterado no Webflow) — nao precisa de `/lp-integrar-form`, o CTA final ja linka direto pro Jotform real (`https://form.jotform.com/261735831186058`).
- Proximo: `/lp-publicar buzzmonitor teste-de-maturidade [dominio]`.
