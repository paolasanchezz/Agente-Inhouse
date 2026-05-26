# Deploy do Dashboard CM Buzzmonitor

> **Skill preferida:** `/dashboard-atualizar` orquestra todo o fluxo abaixo (gera, lida com gate de regressao, deploya, valida). Use o fluxo manual abaixo apenas para debug isolado ou recovery quando a skill estiver fora de alcance.

> **Inegociavel:** deploy NUNCA sai de `dashboard/` no repo. Roda sempre da **pasta sibling fora do repo**.

## Localizacao da sibling

```
C:/Users/titof/Downloads/Claude/dashboard-buzzmonitor-brasil/
├── index.html        ← cópia do dashboard/relatorio-semanal-buzzmonitor-brasil.html
├── middleware.js     ← Basic Auth (user: inhouse, pass: inhouse@77)
├── vercel.json       ← headers de seguranca
├── package.json
└── .vercel/          ← link Vercel (projectId: prj_ck2DquIyOTmxz5Q823q0bgYVvDKe)
```

Mesmo padrao guarda-chuva usado pelas LPs (ver `landing-pages/CONTEXT.md`). A sibling fica **fora do repo** pra evitar que o HTML (com PII e valores comerciais) vaze pro git.

## Por que sibling?

1. **Segredo:** `.gitignore` da raiz exclui o HTML gerado. Sibling separa fonte (codigo de geracao no repo) de saida (HTML deployado).
2. **Middleware Basic Auth:** projeto Vercel exige `middleware.js` na raiz pra interceptar requests. Botar no repo polui com config que so importa pro deploy.
3. **`cd dashboard && vercel deploy` quebra o site** — esse path nao tem middleware nem vercel.json. Resultado: 404 publico, 401 no rollback.

## Fluxo correto (do zero)

```powershell
# 1. Gerar HTML novo (smoke test embutido — bate se YtD mudou)
uv run --python 3.12 --with "psycopg[binary]" python dashboard/gerar_relatorio.py

# Se smoke test falhar:
#   - rodar dashboard/_smoke_test.py ou listar fechamentos pra ver o novo deal
#   - atualizar EXPECTED_FECH_YTD_2026 e EXPECTED_FECH_VALOR_YTD_2026 em gerar_relatorio.py
#   - re-rodar

# 2. Copiar HTML pra sibling
cp dashboard/relatorio-semanal-buzzmonitor-brasil.html "C:/Users/titof/Downloads/Claude/dashboard-buzzmonitor-brasil/index.html"

# 3. Deploy da sibling
vercel deploy --prod --yes --cwd "C:/Users/titof/Downloads/Claude/dashboard-buzzmonitor-brasil"

# 4. Se aliasing nao apontar pro alias principal (acontece se houve rollback recente):
vercel promote <dpl_id> --cwd "C:/Users/titof/Downloads/Claude/dashboard-buzzmonitor-brasil"

# 5. Verificar
curl -u "inhouse:inhouse@77" "https://dashboard-buzzmonitor-brasil.vercel.app/" -o tmp/check.html -w "%{http_code}\n"
# 200 + bytes batem com index.html da sibling = OK
```

## Rollback de emergencia

```powershell
vercel rollback <dpl_id_anterior_READY> --yes --cwd "C:/Users/titof/Downloads/Claude/dashboard-buzzmonitor-brasil"
```

Listar deploys disponiveis: `vercel ls dashboard-buzzmonitor-brasil --cwd "C:/Users/titof/Downloads/Claude/dashboard-buzzmonitor-brasil"`.

## Incidente 2026-05-25 (referencia)

Fiz `cd dashboard && vercel deploy` direto (criei `.vercel/project.json` e `.vercelignore` em `dashboard/`). Deploy "subiu" mas sem middleware e sem `index.html`. Site retornou 404 no root. Rollback restaurou em ~30s. Causa raiz: padrao sibling nao estava documentado no `dashboard/`. Este arquivo existe pra evitar repeticao.
