---
name: pocket-event
description: Gera a landing page de um Pocket Event (mini-encontro de 10 vagas da Buzzmonitor) a partir dos dados do encontro, sem escrever HTML. Mesmo caminho da automacao do formulario — valida contra as listas fechadas, renderiza o template versionado, inscreve o slug no manifesto de evento.buzzmonitor.com e entrega por PR. Usar quando alguem pedir LP de Pocket Event no chat, ou pra ensaiar/depurar o automatismo sem passar pelo Google Forms.
argument-hint: "[--dry-run] [\"titulo\"] [nicho] [modulo] [AAAA-MM-DD] [horario] [speaker]"
allowed-tools: Read, Bash, Skill
version: 1.0.0
---

# Skill: Pocket Event (LP por formulario, rodada a mao)

Caminho manual pro mesmo automatismo do `integracoes/google/README.md`. Voce nao escreve
HTML nem inventa conteudo: monta o JSON da solicitacao e deixa os scripts decidirem.

## Regra que nao se quebra

**Nao editar `landing-pages/buzzmonitor/pocket-*/` a mao.** Essas pastas sao geradas e
recriadas quando a solicitacao e reprocessada. Mudanca que vale pra toda edicao vai no
`index.html.tmpl`; mudanca de uma edicao se faz refazendo a solicitacao.

Nao invente nome, cargo ou bio de speaker: se a pessoa nao esta em `speakers.json`, **pare
e peca o cadastro** (PR revisado). Cadastro e o que garante que a bio no ar foi lida por
alguem antes.

## Passo 1 — reunir os dados

Perguntar o que faltar, sempre oferecendo as opcoes validas:

```bash
py landing-pages/build/render_pocket_event.py --form-spec
```

| Campo | Regra |
|---|---|
| `titulo` | 12 a 60 caracteres, sem ponto final, sem travessao, sem aspas |
| `nicho` | exatamente um valor da lista |
| `modulo` | exatamente um valor da lista (grafias oficiais do BRANDBOOK) |
| `data` | `AAAA-MM-DD`, entre amanha e 180 dias a frente |
| `horario` | exatamente um valor da lista |
| `speaker` | `id` ou nome de quem esta em `speakers.json` |

## Passo 2 — validar sem escrever nada

```bash
py landing-pages/build/pocket_event_job.py solicitacao.json --dry-run
```

O relatorio traz `criadas`, `recusadas` (com o motivo de cada recusa) e `ignoradas` (slug
que ja existe). Recusa: corrigir o dado e repetir. Nunca contornar o validador.

## Passo 3 — gerar de verdade

```bash
py landing-pages/build/pocket_event_job.py solicitacao.json
```

Cria `landing-pages/buzzmonitor/{slug}/` e inscreve o slug no manifesto de
`evento.buzzmonitor.com`. Conferir antes de entregar:

```bash
py landing-pages/build/check_gtm_region.py landing-pages/buzzmonitor/{slug}
py landing-pages/build/check_mobile_type.py landing-pages/buzzmonitor/{slug}
REPO_ROOT="$PWD" py landing-pages/build/build_umbrella.py \
  landing-pages/dominios/evento-buzzmonitor-com/manifest.json /tmp/dist-pocket
```

## Passo 4 — entregar

Rodar `/commit`. O diff so toca conteudo (LP + manifesto), entao o `lp-pr.yml` auto-mergeia
e o `lp-deploy.yml` publica com smoke e rollback.

**Nunca** rodar `vercel deploy` aqui: `evento.buzzmonitor.com` e guarda-chuva migrado pro CI
e deploy manual e bloqueado por hook (CLAUDE.md, Regra No 1).

## Quando NAO usar esta skill

- LP que nao e Pocket Event: `/lp-pipeline`.
- Mudar o visual ou a copy fixa de todas as edicoes: editar `index.html.tmpl` e abrir PR.
- Tirar uma edicao do ar: remover slug do manifesto e decisao humana, nunca auto-merge.

## Referencias

- Runbook da automacao: `integracoes/google/README.md`
- Template, opcoes e limites: `landing-pages/build/templates/pocket-event/`
- Workflow: `.github/workflows/pocket-event-novo.yml`
- Contexto de LP: `landing-pages/CONTEXT.md` §2.8
