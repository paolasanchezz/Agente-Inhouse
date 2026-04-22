# Notion IDs — Fonte Unica de Verdade

> Este arquivo e o unico lugar onde IDs de paginas/pastas do Notion ficam hardcoded.
> Qualquer skill que precise publicar no Notion le os IDs daqui.
> Se um ID mudar no workspace, atualizar SO este arquivo.

---

## Paginas raiz por tipo de entrega

| Chave | ID | Uso |
|---|---|---|
| `entregas` | `33b3934026fd80ceb414dd22cb7dbe1f` | Pasta **Entregas** — copy, traducao, landing page, relatorios meta-ads |
| `newsletter` | `33c3934026fd80778073f1868c5bf11c` | Pagina raiz **Newsletter** — publicacoes semanais por marca |

---

## Como usar nas skills

Sempre que uma skill precisar de um `parent` id para `mcp__*__notion-create-pages`:

1. Leia este arquivo.
2. Selecione a chave apropriada (`entregas` para copy/traducao/LP/meta-ads; `newsletter` para newsletters).
3. Use o valor da coluna ID **exatamente** — sem buscar via `notion-search`, sem hardcode local na skill.

---

## Quem consome

| Skill / CONTEXT | Chave usada |
|---|---|
| `copy-criar`, `copy-revisar` | `entregas` |
| `trad-traduzir`, `trad-revisar`, `trad-pipeline` | `entregas` |
| `lp-preparar`, `lp-publicar` | `entregas` |
| `meta-ads-trends`, `meta-ads-geral` | `entregas` |
| `news-gerar`, `news-pesquisar`, `news-pipeline` | `newsletter` |

---

## Quando atualizar

- Pasta do Notion foi movida ou renomeada → atualizar o ID da chave correspondente aqui.
- Nova pasta raiz para outro tipo de entrega (ex: pesquisa, planejamento) → adicionar nova linha na tabela e documentar em "Quem consome".
- Nunca espalhar o ID novamente nas skills — sempre apontar para este arquivo.
