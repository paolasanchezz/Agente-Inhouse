# atendimento-clinicas

LP do guarda-chuva **content.cxpress.io** (projeto Vercel `cxpress-lp-playbook-whatsapp2026`).

> **Fonte recuperada retroativamente em 2026-06-16** a partir do deploy production `dpl_ESQB5LVKyK3EDf3T6tsutiGdv7uF`.
> A LP estava no ar mas nao tinha source no repo (anti-padrao §7.1 — "LP publicada so na sibling").
> Paths de deploy (`/assets/cxpress/...`) revertidos para a convencao do repo
> (brand -> `../../brand/...`, LP-local -> `./assets/...`); reversao verificada
> byte-a-byte contra o HTML do live.

- **lang:** `pt-BR`
- **Formulario:** Jotform `261045149477663` ("CXPRESS BR | MKT | LPs - Proposta | REMARKETING"). Atencao: esta LP **nao** entrou na unificacao do PR #374 (2026-08-26). Hoje apenas duas LPs embedam este form: esta e a `banimento-whatsapp-clinicas`. As LPs de proposta que entraram na unificacao usam o `261027639617663`. A pagina de agradecimento pos-submit e configurada no Jotform, nao no embed, entao ela acompanha este form.
- **Assets LP-local recuperados:** plataforma/clientes-cxpress.png, plataforma/mockup-plataforma-laptop.png, plataforma/plataforma-canais.gif, plataforma/plataforma-chatbot-ia.gif, plataforma/plataforma-dashboard.gif, og-atendimento-clinicas.png (OG)

## Atualizacao de preco — 2026-08-28

Novo preco minimo de plano da Cxpress: **R$ 1.750**. A chamada de preco desta LP passou a
`Planos a partir de R$ 1.750`, **sem** mencao a quantidade de acessos — por decisao do usuario,
o detalhamento de acessos fica restrito a LP canonica de precos (`/planos`), que segue intacta
com "A partir de R$ 1.750 por mes, com 5 acessos de operador". Alteracao aplicada em bloco nas
9 LPs BR da Cxpress que citavam preco fora da `/planos`.

As LPs LATAM (`USD 260/mes`) e PT-PT (`295 EUR/mes`) **nao** foram alteradas: os valores oficiais
em USD/EUR ainda nao foram definidos e seguem defasados em relacao ao minimo BR.
