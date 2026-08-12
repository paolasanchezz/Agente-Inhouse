# Revisao LP — cxpress/plataforma-atendimento-clinicas

**Data:** 2026-08-12
**Auditores:** frontend-design (review mode) + web-design-guidelines + checks deterministicos (GTM, SEO, em-dash, fidelidade de copy)

## Contexto

LP duplicada de `banimento-whatsapp-clinicas` (ja em producao) com edicoes pontuais: H1+SUB do hero, H2 da secao Plataforma, remocao da secao FECHO. Slug ajustado de `atendimento-clinicas` (pedido original) para `plataforma-atendimento-clinicas` porque o primeiro ja pertence a outra LP ao vivo, alvo de campanhas ativas — decisao confirmada com o usuario antes de gerar.

## Checks deterministicos — todos OK

- GTM: `GTM-T4XDWHL3` presente e correto pra regiao `brasil` (stamp gravado em `.tracking.lock`)
- SEO: description=1, robots=1, og=10, twitter=4, JSON-LD=1 (parseia), canonical=1
- Em-dash no HTML: 0 ocorrencias
- Logo navbar/footer: aponta para `https://home.cxpress.io` (nao `/`), `target="_blank" rel="noopener"` OK
- OG image: `assets/og-plataforma-atendimento-clinicas.png`, 1200x630, sem duplicata `og-image.png`
- Balanco de tags: 8 `<section>`/8 `</section>`, 2 `<style>`/2 `</style>` — remocao da FECHO nao deixou tag orfa
- Fidelidade de copy: H1/SUB/H2 novos batem literalmente com `copy.txt`; nenhuma referencia orfa a `#fecho-title` ou `.fecho`

## Aplicado automaticamente (3 achados)

- [x] CSS morto da secao FECHO (`.fecho`, `.fecho__pills`, `.fecho__inner`, `.fecho h2`, `.linha2`) — removido do `<style>` (causado diretamente pela remocao da secao)
- [x] `.btn--light` — removido (usado exclusivamente pelo CTA da FECHO, agora sem uso)
- [x] JSON-LD `SoftwareApplication.description` — atualizado de "API oficial do WhatsApp: multiplos atendentes..." (herdado, desalinhado) para o novo posicionamento ("centraliza WhatsApp, redes sociais, telefonia, webchat e e-mail...")
- [x] Comentario CSS obsoleto `/* Banimento: CTAs no verde... */` — corrigido pra nao referenciar o tema errado

## Nao aplicado — fora do escopo desta duplicacao (2 achados CRITICO no padrao WCAG, mas sistemicos)

Estes 2 achados sao **identicos no LP-fonte `banimento-whatsapp-clinicas` (ja em producao)** e afetam o design system compartilhado por varias LPs Cxpress (mesmo componente de botao, mesmos GIFs de `brand/cxpress/assets/plataforma/`). Corrigir so nesta LP criaria inconsistencia visual com as ~40 LPs irmas que usam o mesmo padrao. Decisao: nao aplicar unilateralmente — precisa de decisao de marca/design system, nao de um fix pontual.

- [ ] **Contraste do CTA verde (`#21CC78` com texto branco) ≈ 2.1:1** — abaixo do minimo AA (4.5:1 texto normal / 3:1 texto grande). Afeta navbar, hero e secao Prova (mesmo botao compartilhado). Sugestao se decidirem corrigir: escurecer para o tom de hover `#1AAE63` (ou mais escuro) ou trocar pra texto escuro sobre verde claro.
- [ ] **GIFs autoplay em loop sem pausa** (`plataforma-canais.gif`, `plataforma-chatbot-ia.gif`, `plataforma-dashboard.gif`) — o `prefers-reduced-motion` do CSS nao afeta GIF. Sugestao: migrar pra `<video autoplay muted loop>` pausavel via JS quando `prefers-reduced-motion: reduce`.

Sinalizado tambem como sugestao de tarefa separada (fora desta LP) para auditoria cross-LP.

## Melhorias opcionais (4)

- [ ] **Overline do hero desalinhado com o novo H1** — overline continua "API oficial do WhatsApp · Cxpress" (foco estreito), enquanto H1/SUB novos promovem posicionamento omnichannel mais amplo. Considerar algo como "Atendimento omnichannel · Cxpress".
- [ ] **Pagina perdeu o CTA final antes do footer** — a FECHO era a unica secao de "pausa" (fundo escuro) e o ultimo CTA da pagina. Com a remocao, o ultimo CTA visivel fica na secao Prova, bem antes do fim; o fluxo vai direto de "Quem Somos" (fundo branco) pro footer (navy) sem transicao. Nao e quebra tecnica (GUIDELINES §6 permite cortar secoes), mas vale considerar se falta reforcar um CTA mais perto do fim.
- [ ] **Alt text longo na prova social** (lista 10 nomes de clientes) — funciona, mas um alt mais curto seria mais rapido em leitor de tela.
- [ ] **`fill="#6b7280"` hardcoded em 2 SVGs** (icones WhatsApp/ChatGPT na secao Quem Somos) em vez de custom property — so inconsistencia de manutencao, sem impacto visual/funcional.

## Nice-to-haves (3)

- [ ] H2 da secao Plataforma termina com "!" — unico heading da pagina com exclamacao, quebra consistencia tonal com os demais H2 (mais sobrios). Considerar remover o "!".
- [ ] Novo H2 da secao Plataforma e mais generico/promocional que o original, que amarrava com a dor especifica do H1 anterior — registrado pra quem aprovar a copy, nao e erro tecnico.
- [ ] Linhas em branco superfluas e alguns estilos inline (`style="list-style:none"` etc.) — cosmetico, sem efeito em runtime.

## Proximos passos

- Formulario herdado da referencia (Jotform `261027639617663`) — confirmar com o usuario se e o form certo pra esta LP ou se precisa trocar via `/lp-integrar-form cxpress/plataforma-atendimento-clinicas "<snippet>"`
- Design aprovado sem mudar form? -> `/lp-publicar cxpress plataforma-atendimento-clinicas [dominio]`
- Rever mais algum achado? -> editar e rodar `/lp-revisar cxpress/plataforma-atendimento-clinicas` novamente
