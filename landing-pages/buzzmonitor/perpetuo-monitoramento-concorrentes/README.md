# LP · perpetuo-monitoramento-concorrentes (par captura + tks)

Par de páginas de **webinar perpétuo ao vivo**, clonado do par `perpetuo-social-listening` e adaptado pro tema de **monitoramento de concorrente**. A captura inscreve na próxima sessão da série; a thank-you confirma a vaga e entrega o link da sala.

| Página | Slug | Papel | robots |
|---|---|---|---|
| Captura | `perpetuo-monitoramento-concorrentes` | hero + form nativo ClickMeeting + "o que você vai aprender" + autoridade | noindex |
| Thank-you | `perpetuo-monitoramento-concorrentes-confirmado` | confirmação em 2 estados + link da sala + Google Agenda | noindex |

**Série ClickMeeting:** `recurring_config_id` **18043** ("Como construir um monitoramento de concorrentes"), diária às **09:00 BRT**, sessão de **25 min**, `room_pin` 692-573-549, tz `America/Sao_Paulo`. Registro exige nome, sobrenome, e-mail e **empresa** (campo 10 — sem ele a API devolve 422 e a inscrição não acontece). Página pública da série: `https://elifegroup.clickmeeting.com/como-construir-um-monitoramento-de-concorrentes/register`.

**Fluxo:** captura chama `/api/next-webinar?series=concorrentes-br` pra mostrar a data → o form posta em `/api/clickmeeting-register` (`series: 'concorrentes-br'`) → grava `bm_webinar_confirmation` no `sessionStorage` → redireciona pra `/perpetuo-monitoramento-concorrentes-confirmado`. Se o storage falhar, manda direto pra sala do ClickMeeting.

As duas serverless functions vivem em [`landing-pages/buzzmonitor/_clickmeeting-api/`](../_clickmeeting-api/) (cópia canônica) e são servidas pelo `extra_files` do manifesto em `landing-pages/dominios/webinar-buzzmonitor-com/extras/api/`. **Mudança nelas exige editar as duas cópias.**

**Thank-you, 2 estados:**
- **A (veio do form):** lê o `sessionStorage`, saúda pelo primeiro nome, mostra a sessão, botão "Acessar a sala" e link do Google Agenda. Dentro da janela ao vivo (start até start+40min, ou `in_progress` da API), aparece a faixa "acontecendo agora" e o botão vira "Entrar na sala agora".
- **B (visita direta / storage bloqueado / sem JS):** avisa que o link está no e-mail, busca a próxima sessão na API e oferece volta pra captura. Sem JS, o `<noscript>` cobre.

> 🔁 **Modelo trocado em 2026-09-02.** Antes desta data o par era **on-demand**: form Jotform `261904654263661` + despachante `data-perpetuo-next` → thank-you com o vídeo `fG4KpFnwbb4` embedado do YouTube. Com a série perpétua criada, virou par ao vivo no mesmo padrão das outras 6 séries do domínio. O Jotform e o vídeo saíram das duas páginas; o par irmão `perpetuo-social-listening` segue no modelo antigo.
>
> Entre 2026-08-12 e 2026-08-26 a captura era um **mock** que redirecionava certo mas não gravava lead nenhum — todo mundo que preencheu nessa janela foi perdido.

## CTA comercial da thank-you (2026-09-10)

Os dois CTAs "Teste a Buzzmonitor" da thank-you (header + bloco final) apontam pra
`content.buzzmonitor.com/monitoramento-com-ia` com
`utm_source=webinar&utm_medium=lp-webinar-perpetuo&utm_campaign=perpetuo-monitoramento&utm_content=agradecimento-perpetuo-monitoramento`.
O `utm_content` entrou em 2026-09-10 — antes o link ia sem ele, então o lead chegava no CRM sem
dizer **qual** página de agradecimento o gerou. Convenção em
[`conhecimento/config/convencao-utm.md`](../../../conhecimento/config/convencao-utm.md)
(`utm_source` = fonte do lead, `utm_content` = `{tipo-de-pagina}-{conteudo}`).

O bloco final também trocou de copy na mesma data: "Quer adiantar o começo? / Abra sua conta e
chegue na sessão com a plataforma já na mão" virou "Quer começar a monitorar agora? / Teste a
plataforma grátis por 14 dias e chegue na sessão com o seu concorrente já no radar" — headline
ancorada na solução do webinar (monitorar concorrente) em vez de na logística da sessão.

**Divergência a resolver:** as outras 6 thank-you de perpétuo usam `utm_source=perpetuo` e só 2
parâmetros. Esta usa `webinar` + `medium` + `campaign`. Ver §5 do doc de convenção.

## Fonte da copy (2026-08-12)

Briefing da Catharina: título "como construir um monitoramento de concorrentes", promessa "montar um monitoramento de concorrente que avisa antes do cliente avisar", e o objetivo do webinar (criar tema dedicado ao concorrente com variações de grafia, comparar marca x concorrente num dashboard de benchmarking competitivo, configurar AI Insights + Buzz Pills pra avisar quando o concorrente se mexer). Cards em **nível teaser** (sem catálogo de feature), igual ao par social-listening. Sem stat inventada.

## Pendências antes de finalizar

- [x] **OG dedicada:** gerada em 2026-09-02. `assets/og-source.html` + `assets/render_og.py` (dark premium, mesmo eixo do hero; headline "Saiba do concorrente antes do seu cliente"), output `assets/og-perpetuo-monitoramento-concorrentes.png` (1200×630). **Uma cópia física só**, aqui na LP-mãe: a thank-you aponta pro mesmo arquivo (exceção de OG compartilhada entre irmãs, GUIDELINES §18). Antes as duas páginas reusavam a OG do par `primeiro-listening-5-passos`.

> ⚠️ **O aviso `asset referenciado inexistente` do `build_umbrella.py` nos pares perpétuos é falso alarme.** O arquivo existe e **chega no dist**: a resolução procura o basename em `brand/{marca}/assets/` e na pasta da LP que referencia, e só pula se o destino já foi copiado. Quando uma LP aponta pra OG de outra, o aviso aparece se ela vier **antes** da LP dona na ordem do manifesto (era o caso: `perpetuo-*` nos índices 25-32, `primeiro-listening-5-passos` no 33) — a dona copia depois e a URL responde 200 em produção. Não confundir com OG de verdade quebrada: confira `test -f` no source antes de sair caçando bug.
- [x] **Form real:** série ClickMeeting `18043` integrada em 2026-09-02 (form nativo + serverless functions do guarda-chuva). Nada a configurar em painel de form.
- **Dados de autoridade (Victor):** confirmar números (1.000+/300+/500+/10mil) e uso das marcas.
- **Flip `index`** quando for a versão final (hoje `noindex` de review).

## Construção

Captura **dark premium**; tks **clara** (fundo branco). Anti-IA aplicado (0 em-dash, "a Buzzmonitor" feminino). Publicar via fluxo CI: worktree a partir da main + entrada no manifesto + PR pela web (sem `gh` nesta máquina; o merge-bot auto-mergeia conteúdo).
