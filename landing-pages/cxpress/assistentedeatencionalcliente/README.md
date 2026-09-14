# LP Cxpress — assistentedeatencionalcliente

> ## WIP — publicada, ainda em ajuste
>
> Mergeada em 2026-09-14 com o Victor ciente de que a pagina **ainda vai ser ajustada**. Enquanto
> esta secao existir, trate a LP como inacabada e confira as pendencias abaixo antes de mandar
> trafego pra ela.
>
> **O que falta, em ordem de impacto:**
>
> 1. **A submissao do formulario e mock** (`action="#"` + `preventDefault()`). O Paso 2 do quiz e o
>    unico ponto de captura da pagina, entao **hoje ela nao gera nenhum lead** — e falha em
>    silencio, sem erro no console. Integrar via `/lp-integrar-form` antes de investir midia.
> 2. **OG image nao existe.** `assets/og-assistentedeatencionalcliente.png` e referenciada mas nao
>    foi gerada, entao todo compartilhamento sai sem imagem. O `build_umbrella.py` so avisa, nao
>    quebra o build, entao passa despercebido.
> 3. **As estatisticas precisam de validacao.** "+220%", "15x" e "98%" sao creditadas ao "reporte
>    interno Concierge, de 2025", que nao existe no repositorio. O BRANDBOOK da Cxpress nao tem
>    cases validados. Confirmar com quem produziu o reporte que podem ser publicadas nesses termos,
>    ou tirar os numeros e manter a secao qualitativa.
> 4. **Traducao ES-LATAM do quiz nao foi validada com o time** (ja registrado nas pendencias
>    abaixo pela autora).
>
> Ao fechar cada item, marque na secao **Estado** e apague a linha correspondente daqui. Quando os
> quatro sairem, apague este bloco inteiro.


> **Slug renomeado de `quiz-atendimento-latam` em 2026-09-02** e migrado do modo solo (`.vercel.app`) para o guarda-chuva `content.cxpress.io` (deploy via CI, nao mais Vercel CLI direto — ver `landing-pages/dominios/content-cxpress-io/manifest.json`). Historico de deploys solo abaixo preservado pra auditoria.

**Gerado em:** 2026-09-02
**Copy-fonte:** `copy.txt` (output de /lp-preparar, traduzida de PT-BR para ES-LATAM via /trad-traduzir — ver `traducao/entregas/2026-09/quiz-atendimento-latam-es-latam.md`)
**Idioma:** ES-LATAM (`es-419`), tratamento tú

## Estrutura

- HERO — banner full-bleed com video `assets/hero-monkey-running.mp4` (fornecido pelo usuario, LP-local, mudo/loop/playsinline, poster = `assets/hero-samir-dispositivos.png`), H1 (dor) + SUB + CTA num card branco solido (padding + shadow) sobre o video (desktop, garante legibilidade) / video completo abaixo do texto sem card, ja que o mobile ja tem fundo branco natural (`<980px`). Autoplay via JS so roda se `prefers-reduced-motion` NAO estiver ativo (senao fica no poster).
- QUIZ (2 passos) — id="quiz", interativo via JS vanilla:
  - Paso 1: pergunta diagnostica multi-select (checkbox, maximo 2 opcoes) com 5 dores, titulo + descricao cada
  - Paso 2: formulario real de contato (Nombre, Correo de trabajo, Cargo, Telefono, Sitio web da empresa, preferencia WhatsApp/Llamada) — campos reais, submissao ainda mock (`action="#"`, sem backend)
- CLIENTES — ticker animado de logos (14 clientes reais) + label italico "Más de 800 clientes confían en nosotros", mesmo padrao visual de `agente-concierge-latam`
- RESULTADOS — kicker "La prueba" + H2 "Resultados de empresas que potenciaron a sus equipos con Cxpress" + 3 stats com count-up (+220%, 15x, 98%) em grid com divisores, mesmo padrao visual de `agente-concierge-latam` + disclaimer + mascote Samir (`assets/samir-resultados.png`) no canto superior direito da secao
- BENEFICIOS — kicker "Qué hace por ti" + H2 "Transforma conversaciones en más engagement y ventas" + grid bento (4 tiles, texto na mesma cor do H2), mesmo padrao visual/copy literal de `agente-concierge-latam` (secao inteira copiada de la, pedido explicito do usuario; mascote removido do tile 01 a pedido posterior)

## Estado

- [x] HTML gerado
- [ ] OG image 1200×630 → `assets/og-assistentedeatencionalcliente.png` (ainda nao gerada — template em `.claude/skills/lp-gerar/og-template.html` + Chrome headless; confirmado como o unico aviso do `build_umbrella.py`)
- [x] Revisao (frontend-design review + web-design-guidelines) — 5 criticos aplicados, ver `REVISAO.md`
- [ ] Formulario integrado — campos do Paso 2 sao reais mas a submissao e mock (JS local, sem backend). Plano do usuario: migrar pra Jotform (o proprio quiz/form sera a captura de lead, sem form adicional na LP)
- [x] Publicado (historico, modo solo) — `https://cxpress-lp-quiz-atendimento-latam.vercel.app/quiz-atendimento-latam`, 2026-09-02
- [ ] Publicado em `content.cxpress.io/assistentedeatencionalcliente` — entrou no manifesto do guarda-chuva em 2026-09-02, aguardando merge do PR na main pro CI deployar (nunca `vercel deploy` direto nesse dominio)

## Pendencias / decisoes registradas

- **Quiz Paso 1 e o roteiro real** (pergunta + 5 dores) fornecido pelo usuario em PT-BR e traduzido/adaptado por mim para ES-LATAM (mesmo tratamento tu e vocabulario do resto da LP). Paso 2 e um formulario de contato real (campos + rotulos), mas a submissao continua mock ate a integracao via `/lp-integrar-form`. Validar a traducao com o time antes de publicar em producao.
- **Copy publicada no Notion pulada.** MCP do Notion nao estava conectado nesta sessao — `copy.txt` local e a fonte-verdade; publicar manualmente no Notion (pasta Entregas) quando o MCP estiver disponivel, ou rodar `/lp-preparar` novamente.
- **brand-manifest da Cxpress sem bloco `regions`.** Usado `websites.latam` (`https://home.cxpress.io`) como home regional; JSON-LD `Organization` ficou sem `sameAs` (LinkedIn/Instagram) por falta desse dado estruturado. Migrar o manifest pro formato `regions` (ver `.claude/skills/lp-gerar/SKILL.md` Passo 1) resolve para as proximas LPs.
- **Sem LPs irmas** com esse slug — SEM bloco `hreflang`, so `canonical`.
- **Secoes Clientes, Resultados e Beneficios reaproveitam o padrao visual/CSS de `landing-pages/cxpress/agente-concierge-latam/`** (pedido explicito do usuario: mesma fonte e estilo). Ticker de logos LP-local (`assets/clientes/`, 14 arquivos copiados de `agente-concierge-latam/assets/clientes/`), kicker italico Bitter, stats com count-up JS e divisores verticais. Titulos e copy das tres secoes vieram literais de `agente-concierge-latam` (a secao Beneficios foi copiada inteira, texto e estrutura, a pedido do usuario).
- **Video do hero (`hero-monkey-running.mp4`) pesa ~8,7MB sem compressao/otimizacao** (arquivo bruto fornecido pelo usuario). Pode impactar o score de Performance do PageSpeed (ainda nao coletado nesta sessao). Considerar recomprimir (H.264, bitrate menor) antes de rodar `/lp-health-check` ou campanha paga.

## Deploy

### Atual — guarda-chuva `content.cxpress.io` (via CI)

- **URL publica (apos merge):** https://content.cxpress.io/assistentedeatencionalcliente
- **Manifesto:** `landing-pages/dominios/content-cxpress-io/manifest.json` (entrada `assistentedeatencionalcliente` adicionada em 2026-09-02)
- **Build local validado:** `build_umbrella.py` OK (unico aviso: OG image ainda nao gerada, esperado) + gate GTM `ok` (regiao `latam` resolvida via `<html lang="es-419">`, container `GTM-WRQ47B9R` bate)
- **Como atualizar:** editar `landing-pages/cxpress/assistentedeatencionalcliente/`, commitar + abrir PR (`/commit`). PR so-conteudo mergeia sozinho (merge-bot) e o CI deploya a main inteira com smoke test automatico. NUNCA `vercel deploy` manual nesse dominio (bloqueado por hook).

### Historico — modo solo (`.vercel.app`, ate 2026-09-02, antes da migracao de slug/dominio)

- **URL publica:** https://cxpress-lp-quiz-atendimento-latam.vercel.app/quiz-atendimento-latam
- **Modo:** solo (sem dominio custom fornecido)
- **Projeto Vercel:** `cxpress-lp-quiz-atendimento-latam` (org `elife-group`)
- **Sibling:** `D:/Meus documentos/Downloads/cxpress-lp-quiz-atendimento-latam/` (fora do repo)
- **Deploy ID (inicial):** `dpl_9QTrd9NCPQxUwTA19ob32oDGsDxn`
- **Deploy ID (hero atualizado):** `dpl_AP78GFTo3CNfoVGkiY2CgwBdCaqM`
- **Deploy ID (secoes Clientes/Resultados no estilo agente-concierge-latam):** `dpl_C5X5V6bxdjJTSUUSxi1buMa2Yorx`
- **Deploy ID (mascote Samir em Resultados):** `dpl_42E5BKpK1AwQdEUa93byT9Nhei3y`
- **Deploy ID (hero trocado por samir 3.png):** `dpl_5zZ8KQCuCrQfdhoztK9Ev7mBnmss`
- **Deploy ID (hero trocado por video, depois revertido de volta pra samir 3.png):** `dpl_HTZWXHKXC4DJPteZ4QqkHAsoYru6` (video) → revert commit `24d0b8a`
- **Deploy ID (mascote Resultados trocado para samir 2.png):** `dpl_6vMjxRqhGnAsd9bkMDNHkpzvDvyh`
- **Deploy ID (mascote Resultados maior + espaco hero-quiz + secao Beneficios nova):** `dpl_7gKUoogqscsfq59VrBFHcmewwMmy`
- **Deploy ID (hero trocado por video monkey-running.mp4):** `dpl_EvwtWXUeHPM12KTxvbcCa6FHoShx`
- **Deploy ID (card branco no hero + mascote removido do tile 01 + cor do texto dos tiles):** `dpl_Bq9uMMYJWx49b6d548aXbTdgWr92`
- **Data:** 2026-09-02
- **Certificado:** Google Trust Services (WR1), valido ate 2026-11-27
- **Headers de seguranca:** 7/7 ativos (HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy, COOP, CSP)
- **GTM:** `GTM-WRQ47B9R` (LATAM), 3/3 tokens servidos (gtm.js + ns.html + ID)
- **PageSpeed:** nao coletado (API publica retornou 429 Too Many Requests nesta sessao) — rodar manualmente em https://pagespeed.web.dev/ quando possivel
- **Nota:** o projeto Vercel solo `cxpress-lp-quiz-atendimento-latam` continua no ar por enquanto (nao foi desativado) — decidir com o Victor se despublica depois que `content.cxpress.io/assistentedeatencionalcliente` estiver confirmado no ar.

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `./assets/hero-monkey-running.mp4` (hero, LP-local — fornecido pelo usuario, video 1280×720, ~9s, mudo/loop, origem `criativos/cxpress/brasil/Marketing day/Monkey_running_toward_smartphone_202609021857.mp4`)
- `./assets/hero-samir-dispositivos.png` (poster/fallback do video do hero, LP-local, 1916×821. Historico: 1a imagem `Design sem nome (7).png` → `samir 3.png` → video `Blue_monkey_leaping...` (revertido) → agora poster do video `monkey running`, todas de `criativos/cxpress/brasil/Marketing day/`)
- `./assets/clientes/cliente-{01..40 esparsos}.png` (14 logos reais no ticker — copiados de `landing-pages/cxpress/agente-concierge-latam/assets/clientes/`)
- `./assets/samir-resultados.png` (mascote na secao Resultados, LP-local — fornecida pelo usuario, 1230×1278, PNG transparente. Trocada: original `samir.png` com medalha/crown, agora `samir 2.png` com medalha de fita verde, ambas em `criativos/cxpress/brasil/Marketing day/`)
