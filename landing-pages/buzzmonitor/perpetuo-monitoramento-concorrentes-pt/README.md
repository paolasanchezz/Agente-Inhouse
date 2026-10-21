# LP · perpetuo-monitoramento-concorrentes-pt (par captura + tks) · PT-PT

> **Voltou a ser on-demand em 2026-10-21 (pedido da Catharina).** A captura usa de novo o Jotform de perpétuo `261904654263661` com `data-perpetuo-next="/perpetuo-monitoramento-vsl-pt-confirmado"`: quem preenche cai na tks **com vídeo** do par VSL. Não inscreve mais na série ClickMeeting 18086. A tks `perpetuo-monitoramento-concorrentes-pt-confirmado` (confirmação de sessão ao vivo) continua publicada, mas nenhuma captura leva mais pra ela. O resto deste README descreve o modelo ao vivo (histórico).

Par PT-PT do webinar perpétuo **ao vivo** de monitorização de concorrentes. Nasceu em 2026-08-25
como duplicação 1:1 do par PT-BR [`perpetuo-monitoramento-concorrentes`](../perpetuo-monitoramento-concorrentes/README.md)
no modelo on-demand (form mock + vídeo gravado na tks) e passou a webinar ao vivo em 2026-09-04,
ligado à série ClickMeeting **18086** (Portugal).

| Página | Slug | Papel | robots |
|---|---|---|---|
| Captura | `perpetuo-monitoramento-concorrentes-pt` | hero + form nativo ClickMeeting + "o que vai aprender" + autoridade | noindex |
| Thank-you | `perpetuo-monitoramento-concorrentes-pt-confirmado` | confirmação em 2 estados (link da sala + data da sessão) + CTA | noindex |

**Fluxo:** captura → o form posta em `/api/clickmeeting-register` (`series=concorrentes-pt`),
que inscreve na próxima sessão da série → a resposta traz a **ligação pessoal da sala**, guardada
em `sessionStorage` → redirect para `/perpetuo-monitoramento-concorrentes-pt-confirmado`, que
mostra o botão de entrar na sala, a data da sessão e o "adicionar ao Google Calendar". CTA final
leva para `content.buzzmonitor.com/monitoramento-manual-pt` (conteúdo próprio da versão PT,
diferente do CTA da versão PT-BR — pedido explícito da Catharina, 2026-08-25).

## Série ClickMeeting (18086)

| Campo | Valor |
|---|---|
| `recurring_config_id` | `18086` |
| Chave `?series=` | `concorrentes-pt` |
| Nome | Como construir um monitoramento de concorrentes  Portugal |
| `room_url` | `elifegroup.clickmeeting.com/como-construir-um-monitoramento-de-concorrentes-portugal` |
| `room_pin` | 355-724-775 |
| Horário | **10:00 hora de Lisboa** (= 06:00 BRT), sessão de 30 min, diária |
| Timezone | `Europe/Lisbon` |

**Data na página é formatada no cliente.** O `next-webinar.js` devolve `formatted_full_pt` em
`pt-BR` + `America/Sao_Paulo`; usar esse campo aqui anunciaria 06h00 em vez de 10h00. As duas
páginas formatam a partir de `starts_at` com `Intl.DateTimeFormat('pt-PT', { timeZone: 'Europe/Lisbon' })`,
mesmo padrão das LPs ES (que formatam em `es-MX` / Cidade do México).

**E-mail de confirmação sai no pack `br`.** O ClickMeeting não tem código `pt-PT` (só pl, en, de,
ru, es, fr, it, br). As mensagens de erro do formulário, essas sim, saem em PT-PT
(`MESSAGES.pt` no `clickmeeting-register.js`).

## Destinos: nada aponta para buzzmonitor.com

Decisão do Victor (2026-09-04): esta é uma LP **PT**, então nenhum link dela pode levar ao
`buzzmonitor.com`, que é o site focado em BR. Todos os destinos externos das duas páginas (logo do
header, logo do rodapé, link do rodapé, CTA "Falar com especialista" da tks e CTA final da tks)
apontam para:

```
https://content.buzzmonitor.com/monitoramento-manual-pt?utm_source=webinar&utm_medium=lp-webinar-perpetuo&utm_campaign=perpetuo-monitoramento-pt&utm_content=botao-lp-monitoramento-pt
```

**Única exceção:** o link da **política de privacidade** no consentimento do formulário segue em
`buzzmonitor.com/politica-de-privacidade/`. É link legal, não destino de marketing: mandar quem
procura a política para uma LP de campanha seria errado. Se existir versão PT da política, trocar
por ela.

O link do rodapé deixou de se chamar "buzzmonitor.com" e passou a "Saber mais", para o texto não
prometer um destino diferente do que o link abre.

**Convite de moderador:** série mapeada em `.claude/skills/convites-moderador/config.json` para
`manuela.martins@elifeportugal.com` e `raquel.oliveira@buzzmonitor.com`. Como a sessão começa
06:00 BRT e o cron roda 07:00 BRT, o convite desta série é sempre para a sessão do dia seguinte.

## Origem da copy

Duplicação pedida pela Catharina (2026-08-25) do par PT-BR `perpetuo-monitoramento-concorrentes`
(fonte original: briefing de 2026-08-12). Mesma estrutura e mesma copy, traduzida para PT-PT
seguindo `conhecimento/linguistico/pt-portugal/padrao-linguistico.md` (Regras de Ouro: "está a
funcionar", "utilizador(es)", possessivo com artigo, "folha de cálculo", "captura de ecrã",
"monitorização"/"monitorizar") e `conhecimento/editorial/regras-anti-ia.md`.

Em 2026-09-04, com a virada para ao vivo, a copy de "preencha e assista" deu lugar a copy de
inscrição ("Garanta o seu lugar", "30 minutos", CTA final para a próxima sessão) e a tks trocou o
vídeo pela confirmação. Vocabulário PT-PT do formulário: **"Apelido"** (não "Sobrenome"),
**"ligação"** de acesso (não "link"), "A enviar...", "Erro de ligação".

## Pendências antes de finalizar

- **Link do WhatsApp (header da tks):** o CTA "Falar com especialista" aponta hoje para a LP
  `monitoramento-manual-pt` (saiu o temp `buzzmonitor.com` em 2026-09-04). Trocar pelo link de
  WhatsApp quando a Catharina mandar.
- **OG dedicada:** hoje reusa `og-primeiro-listening-5-passos.png`. O par PT-BR já ganhou a sua
  (`og-perpetuo-monitoramento-concorrentes.png`); gerar a versão PT com o mesmo
  `assets/og-source.html` + `render_og.py` do par BR.
- **Vídeo gravado aposentado:** o embed do YouTube `fG4KpFnwbb4` saiu da tks. Se algum dia a
  versão on-demand voltar a ser útil, ela vive no histórico do Git (commit anterior a 2026-09-04).
- **Dados de autoridade (Victor):** confirmar números (1.000+/300+/500+/10mil) e uso das marcas —
  os mesmos números e marcas do par PT-BR foram mantidos por pedido de duplicação 1:1.
- **Flip `index`** quando for a versão final (hoje `noindex` de review).

## Construção

Captura **dark premium**; tks **clara** (fundo branco). Anti-IA aplicado (0 em-dash, "a
Buzzmonitor" feminino). Publicar via fluxo CI: entrada já existe no manifesto de
`webinar.buzzmonitor.com`, então é PR na main e o `lp-deploy.yml` publica (sem sibling, sem deploy
manual).
