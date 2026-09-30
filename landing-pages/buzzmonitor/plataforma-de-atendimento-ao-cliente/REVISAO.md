# Revisao LP — buzzmonitor/plataforma-de-atendimento-ao-cliente

**Data:** 2026-09-29 (2 rodadas)
**Hospedagem:** Leadpages (org Tami Buzzmonitor), slug `plataforma-de-atendimento-ao-cliente`, pageId `hzergrs5nakbwt2k0bvimpd3` — **publicada**
**Auditores:** ui-craft design-reviewer + a11y-auditor
**Adaptacao do /lp-revisar:** LP fora do pipeline Vercel/CI: sem git pull, GTM, hreflang, logo regional e OG por script (head e tracking sao da Leadpages). Em-dash: 0.
**Fonte:** `index.html` (dev, CSS/JS inline) · `build/` (styles.css, page.js, form.js, form-src.html, leadpages.html e scripts `_build_*.js` que regeram tudo)

## Rodada 1 — aplicado
Contraste de botoes laranja (texto escuro), skip-link + `<main>`, foco roxo em secoes claras, `<h2>` no plano, `role=group` no form, pausa de animacoes, nome acessivel dos carrosseis, reveal so com JS, eyebrow das abas, pill ativa, `scrollTo` com reduced-motion, preco R$ 1.790, secao do WhatsApp e chip de licencas removidos.

## Rodada 2 — aplicado automaticamente
- [x] Menu quebrava em 360-390px (logo 38px + CTA): logo 30px, CTA compacto, gap menor; cabe em 375px (botao termina em 359px)
- [x] Foco laranja (< 3:1) no menu, hero e faixa de logos: outline roxo; botao de pausa com anel duplo
- [x] Skip-link e ancoras nao moviam o foco: o alvo recebe `tabindex=-1` e foco
- [x] Palavra "multicanal" do H1 sobre o brilho pessego: cor `#B8500A`
- [x] Bordas dos campos do form (~1,7:1): `#857796` (> 3:1); fonte 16px (evita zoom no iOS); select vazio em cor de placeholder; checkbox/foco em roxo
- [x] `autocomplete` em nome e empresa; landmark `role=main` duplicado removido do form; espaco em "Privacidade. Os" (ajuste mecanico)
- [x] Deteccao do editor restrita a `blob:`/`about:`/ancestral leadpages.com (nao desliga o form em preview `*.leadpages.com`); no editor aparece um placeholder no lugar do form
- [x] Pausa nao congela mais H1/subtitulo/CTA invisiveis; botao de pausa vai para o inicio do DOM, rotulo fixo + `aria-pressed`
- [x] Selos 5+5 em 376-1199px; respiro entre colunas e teto de 1440px no hero; `line-height` do H1 evita cortar descendentes
- [x] Espaco excessivo entre hero, logos e primeira secao reduzido; costura do marquee alinhada; logos a 60% de opacidade
- [x] Tilt do preco responsivo (transicao curta apos o reveal); numero com `tabular-nums`

## Pendencias suas / a verificar
- [ ] **Teste de envio real do formulario** na URL publicada. O Jotform agora roda em `srcdoc` (origem da LP) e o reCAPTCHA invisivel pode nao liberar o envio se a chave nao aceitar o dominio. Enviar um lead de teste e confirmar que chega no Jotform/CRM com UTM/gclid. Se falhar, volta-se ao iframe publico.
- [ ] **Quantidade de licencas** do plano (nao consta em nenhum projeto); chip removido.
- [ ] Depoimentos em imagem (4 PNG) sem texto acessivel por card; nomes das marcas dos logos.
- [ ] Dominio proprio: a URL `lpcontent.net` sai com `noindex` e barra de Preview.

## Melhorias opcionais (nao aplicadas)
- [ ] Selos: trocar `font-size:0` por `.bz-sr` + `role="list"`; `aria-hidden` nos SVG; tooltip/`title` visivel (estrela, celular e envelope sao ambiguos)
- [ ] Rotulos visiveis persistentes no form (hoje so placeholder), indicacao de obrigatorio, dica do telefone via `aria-describedby`, nomear o grupo do checkbox
- [ ] Tela de agradecimento do Jotform (fora do tema) e altura do iframe apos o envio
- [ ] Contador do preco: `aria-label` com o valor final; comecar de valor proximo para evitar o flash "0"
- [ ] `scroll-padding-top` no `html`; `<em class="bz-grad">` do H1 como `<span>`; `.bz-top{display:contents}` (landmark banner em navegadores antigos)
- [ ] Faixa de logos aparece duas vezes com a mesma frase; nomes reais das empresas no `aria-label`
- [ ] Costura horizontal entre hero e faixa de logos (aurora cortada por `overflow:hidden`)
- [ ] Hover dos selos >= 1200px e pulso da tag do preco (sugerem clique); borda giratoria do card do form
- [ ] Modo editor: menu fica transparente (scroll handler nao roda)

## Nice-to-haves
- [ ] `clamp()` em `rem`; avisos de "abre em nova aba"; atribuicao do reCAPTCHA (badge oculto)
- [ ] Copy legal do form em PT-PT ("Os meus dados"): e texto do cliente, so sinalizar
