# LP Cxpress — institucional

**Reconstruída em:** 2026-10-06
**Copy-fonte:** `copy.txt`
**Destino:** `content.cxpress.io/institucional` (guarda-chuva, deploy via CI)
**Região:** brasil · `<html lang="pt-BR">` · GTM `GTM-T4XDWHL3`
**Formulário:** Jotform `261045149477663` (form de Meta, trocado em 2026-10-06; antes `261034073026647`, o de Google Ads)

## Por que foi reconstruída

A versão anterior era uma **portada do WordPress** de `home.cxpress.io`, capturada em 26/08.
Nunca passou pelo sistema de design das LPs Cxpress: trazia 42 imagens do WP, CSS herdado do
tema e, principalmente, **nenhuma declaração de `font-family` no `body`**, o que jogava 46
elementos para Times New Roman no navegador. Era a causa do "por que ela está tão feia".

O gatilho foi a campanha: os 3 vídeos novos de `[conversao][institucional]` (INSTT 2, 3 e 4)
apontam para cá. São demos do Enrico, cada uma abrindo com uma pergunta:

| Vídeo | Pergunta que abre |
|---|---|
| 1 | "Enrico, eu quero automatizar todo o atendimento da minha empresa e quero um tom de voz em cada [canal]" |
| 2 | "Enrico, todos os meus clientes estão reclamando do atendimento da minha empresa e eu não tenho visibilidade. Como a Cxpress me ajuda?" |
| 3 | "Me mostra como a Cxpress consegue unir todo o atendimento" |

A página antiga abria com posicionamento genérico. Quem clicava depois de ouvir a própria dor
não reencontrava ela em lugar nenhum.

## Estrutura

| # | Seção | Fundo |
|---|---|---|
| 1 | Hero + ficha "Oito canais numa fila única" | claro |
| 2 | **Demonstração** (Jotform) | escuro |
| 3 | As três perguntas | off |
| 4 | A plataforma em números (80% / 50% / 8) | escuro |
| 5 | Sem Cxpress e com Cxpress | claro |
| 6 | Para quem é | off |
| 7 | Fecho + esteira de 42 logos | claro |

### A seção "As três perguntas"

São as 3 perguntas dos vídeos, em primeira pessoa, na mesma ordem de peso. Quem vem do
anúncio 2 lê a própria frase na página.

Não é enfeite: nesta conta o casamento anúncio-LP é a variável que mais mexe em conversão.
`banimento-whatsapp` converteu **20,0%** (115 visitas) contra **3,2%** da `tempo-de-resposta`
(154 visitas), mesmo Jotform e mesmos campos.

### Formulário na 2ª seção

Estava na **8ª de 8**, a 75% do arquivo. Subiu para logo depois do hero.

Medido com emulação 375×812: **1,89 tela de scroll, 19% da página**. A `banimento-whatsapp`,
a que mais converte na conta, tem o form a 1,9 tela.

## Números: o que pode e o que não pode

Os 3 big numbers (**80%** dos tickets por IA, **50%** de redução no tempo médio de
atendimento, **8 canais**) são claims públicos da própria marca, herdados da página anterior,
que veio do site institucional. Mantidos literais.

⛔ **Não usei** os números de `conhecimento/produto/cxpress/bignumbers-paginas.md` (94%
resolvido por IA, -60% de equipe, 15x produtividade). O alerta 1 daquele arquivo é explícito:
são cases de serviço da Elife com o Agente Sentinela, **não da plataforma Cxpress**, e só
podem aparecer em página de produto se o Victor confirmar o enquadramento.

## O que saiu

| Removido | Motivo |
|---|---|
| As 42 imagens do WordPress (2,51 MB) | o sistema de design usa SVG inline e tipografia, não sprite de ícone. Ficaram órfãs e saíram do deploy. `planos` tem cópias próprias, não quebrou nada |
| Seção de abas "Soluções integradas" | 4 parágrafos institucionais sem nada concreto. O conteúdo útil (IA, CRM com histórico, gestão com dashboards) virou as 3 perguntas |
| "crie uma comunidade de clientes fidelizados!" | única exclamação da página |
| "Tickets distribuídos **de forma** automática ou manual" | "de forma X" é filler proibido pelo `regras-anti-ia.md`. Virou "distribuídos automaticamente ou pela equipe" |

## Correção de overflow (vale para as LPs irmãs)

O `.eyebrow--pill` do sistema tem **`white-space:nowrap`**. Eyebrow comprido estoura o
viewport no celular e empurra a página inteira para o lado.

Aqui o pill media 418px numa tela de 375. Corrigido de duas formas, de propósito:

1. Texto encurtado para "Plataforma de atendimento digital" (o "· Cxpress" era redundante, a
   logo está no header).
2. Rede de segurança no CSS, para não depender de contagem de caractere:
   ```css
   @media (max-width:640px){ .eyebrow--pill{white-space:normal;text-align:center;line-height:1.45} }
   ```

⚠️ **A `webinar-whatsapp-equipe` tem o mesmo defeito, e pior.** Medido com emulação 375×812:
pill de **722px**, `scrollWidth` 742 contra `clientWidth` 375. A página inteira rola de lado
no celular. O README dela afirma "Overflow horizontal a 375px: nenhum", o que está errado,
provavelmente por medição sem emulação mobile de verdade. **Não corrigi** (fora do escopo
pedido). A `black-friday-atendimento-b` está limpa, porque o pill dela é curto.

## Validações rodadas

| Checagem | Resultado |
|---|---|
| Tags balanceadas | section 7/7 · main 1/1 · body 1/1 · script 4/4 · ul 2/2 |
| Pacote SEO §15 | title 1 · canonical 1 · robots 1 · og 10 · twitter 4 |
| JSON-LD | parseia; Organization + WebPage + SoftwareApplication |
| GTM | `GTM-T4XDWHL3` no head e no noscript |
| Jotform | `261045149477663`, um único embed |
| em-dash / exclamação | 0 / 0 |
| Filler ("de forma", "de maneira", "realmente"...) | 0 |
| `<img>` sem `alt` | 0 de 86 |
| Assets quebrados | 0 |
| Logo web-safe §19 | `logo-primary.svg` e `logo-reversed.svg`: 0 `<text>` |
| `href="/"` na logo | 0 (aponta para `home.cxpress.io`, target `_blank`) |
| Âncoras mortas | 0 |
| Overflow horizontal a 375px | nenhum (medido com emulação, não com `--window-size`) |
| Times New Roman | 0 elementos (era 46) |
| `build_umbrella.py` | OK, 73 LPs, 0 aviso para este slug |
| `check_gtm_region.py` | 65 OK, 0 bloqueio |

## Pendências e decisões em aberto

1. ~~**O Jotform é o de Google Ads.**~~ Resolvido em 2026-10-06: trocado pelo `261045149477663`
   (o de Meta), coerente com o container `GTM-T4XDWHL3` e o tráfego INSTT. A página de
   agradecimento pós-submit passa a ser a configurada nesse form, no painel do Jotform.
2. **O botão "Enviar" do Jotform é verde-água** e briga com a paleta azul da página. É tema
   do Jotform, não dá para estilizar daqui (iframe cross-origin). Ajuste no painel do Jotform.
3. **OG image:** `assets/og-institucional.png` foi mantida da versão anterior. Vale regerar
   com o título novo (`assets/og-template.html` + `assets/render_og.py`).

## Estado

- [x] HTML gerado no sistema de design
- [x] Formulário integrado e reposicionado
- [x] Validações e gates do repo
- [ ] Publicado — `/lp-publicar cxpress institucional content.cxpress.io`

⚠️ **A publicação precisa de worktree a partir de `origin/main`.** O tree local está em
`claude/lp-bf-ordem`, branch de outra tarefa e dezenas de commits atrás; editar o manifesto
daqui apagaria LPs que estão no ar.

## Sistema de design

Herdado da `black-friday-atendimento-b` (CSS idêntico): paleta de 2 cores (preto `#0E1116` +
azul `#2B5CE6`) mais neutros. Componentes reaproveitados: `hero` + `ficha`, `inscricao` /
`insc__grid` / `form-card`, `dores` + `ver__ck`, `bignum` / `nums`, `fecho`, esteira de
clientes, `header` / `footer`.

Dois componentes novos, escritos no mesmo vocabulário: `.comp` (comparativo sem/com, duas
colunas, a da direita no preto da marca) e `.setores` (chips de segmento).
