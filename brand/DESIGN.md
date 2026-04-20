# Design System — Grupo Elife

## Como usar este arquivo

Este arquivo e o ponto de entrada do sistema de marca para o agente.
Para carregar a identidade visual de uma marca, leia os seguintes arquivos:

1. `brand/{marca}/brand-manifest.json` — identidade, voz, mensagens-chave
2. `brand/{marca}/tokens.json` — tokens de design (cores, tipografia, espacamento)
3. `brand/{marca}/generation-rules.json` — regras de geracao para IA
4. `brand/{marca}/BRANDBOOK.md` — diretrizes detalhadas, do's & don'ts

## Marcas Disponiveis

| Marca | Diretorio |
|---|---|
| Buzzmonitor | `brand/buzzmonitor/` |
| Buzzcreators | `brand/buzzcreators/` |
| Cxpress | `brand/cxpress/` |
| Elife | `brand/elife/` |

## Hierarquia de Prioridade

1. `tokens.json` — valores exatos (hex, px, font-family). Fonte de verdade para codigo.
2. `generation-rules.json` — regras de composicao (layout, uso de cor, tipografia por contexto).
3. `BRANDBOOK.md` — contexto qualitativo, exemplos de voz, do's & don'ts.
4. `brand-manifest.json` — identidade, tom de voz numerico, mensagens-chave.
5. `conhecimento/produto/{marca}/` — conhecimento de produto (NAO duplicar aqui).

## Integracao com Figma

Tokens em `tokens.json` seguem o formato W3C DTCG, compativel com Figma Variables.
Use `get_variable_defs` do Figma MCP para sincronizar tokens do Figma para o JSON local.

## Regras Globais

- Nunca misturar identidades visuais entre marcas
- Todas as marcas pertencem ao Grupo Elife — manter coerencia no footer/rodape
- Logo do Grupo Elife aparece como "powered by" ou no footer de materiais das sub-marcas
- Acessibilidade: WCAG AA minimo (contraste 4.5:1 para texto)
- Em codigo gerado, usar CSS variables (`var(--color-primary)`) em vez de hex hardcoded

## Adicionar Nova Marca

1. Copiar `brand/_shared/` como base
2. Criar pasta `brand/nome-da-marca/`
3. Preencher `brand-manifest.json`, `tokens.json`, `generation-rules.json`
4. Criar `BRANDBOOK.md` seguindo o template
5. Adicionar logo em `assets/logos/`
6. Registrar nesta tabela acima
