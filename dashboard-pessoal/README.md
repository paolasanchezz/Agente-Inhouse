# Dashboard CM pessoal · Buzzmonitor Brasil

Versão **local-only** do [dashboard-buzzmonitor-brasil.vercel.app](https://dashboard-buzzmonitor-brasil.vercel.app/) com:

- **Seletor de período** — presets (7d / 15d / 30d / 90d / MtD / YtD) + date picker custom
- **Mesmas regras CM** do dashboard oficial (filtro UTM/blog/material/eventos + regra 90d + whitelist/blacklist)
- **Brasil-only** (LATAM não tem UTM no banco)
- **Roda no seu PC** — só você acessa

## Por que local-only?

O dashboard oficial é HTML estático gerado por build. Esta versão é **dinâmica** (seletor de período faz fetch ao banco em tempo real), o que exige um backend Python rodando. Tentamos serverless no Vercel mas o Supabase Direct connection (`db.PROJ.supabase.co`) só aceita IPv6, e o Vercel Lambda é IPv4-only. O pooler do Supabase é a saída, mas requer habilitar a role `looker_readonly` em "Pooler Configuration" no dashboard Supabase. Pra evitar essa configuração extra, mantemos local.

## Arquitetura

```
dashboard-pessoal/
├── api/
│   └── dashboard.py        ← handler HTTP (recebe ini/fim, devolve JSON)
├── public/
│   └── index.html          ← front estático (HTML + CSS + JS, sem framework)
├── lib/
│   ├── datas.py            ← cálculo de períodos (atual/anterior/MtD/YtD)
│   ├── queries.py          ← cópia adaptada de dashboard/queries.py
│   └── render.py           ← transformações JSON-safe
├── run_local.py            ← servidor HTTP local (porta 8000)
├── smoke_test.py           ← valida a coleta sem subir servidor
├── requirements.txt
├── README.md
└── .env                    ← (copiado de dashboard/.env)
```

## Como rodar

```powershell
cd dashboard-pessoal
uv run --python 3.12 --with "psycopg[binary]" python run_local.py
```

Abre [http://127.0.0.1:8000](http://127.0.0.1:8000) no browser.

> O `.env` já está copiado do dashboard oficial (mesmo banco, mesmo `looker_readonly`).

## Validar antes de rodar o servidor

```powershell
uv run --python 3.12 --with "psycopg[binary]" python smoke_test.py
```

Faz uma coleta completa (todos os blocos) e imprime os KPIs no terminal. Útil pra confirmar que o banco está respondendo antes de abrir o browser.

## Manutenção

Quando o filtro CM oficial mudar (em `dashboard/queries.py`), replicar mudanças aqui em `lib/queries.py`. Não tem import compartilhado entre as pastas — as duas versões são independentes propositalmente.

## Diferenças vs dashboard oficial

| Aspecto | Oficial (Vercel) | Pessoal (local) |
|---|---|---|
| Período "atual" | Semana sáb→sex fixa | Seletor dinâmico (default 7d) |
| Geração | HTML estático buildado | API local + JS dinâmico no browser |
| Acesso | Público | Só você (rodando local) |
| Filtro CM | idêntico | idêntico |
| Tabelas | Brasil | Brasil |
| Gráficos 12m | Pré-renderizados | Sempre fresh ao abrir |

## Atalho recomendado

Crie um shortcut no Windows pra subir o servidor com 1 clique:

1. Clique direito em algum lugar → Novo → Atalho
2. Em "Localização":
   ```
   powershell.exe -Command "cd 'C:\Users\titof\Downloads\Claude\Agente Inhouse\dashboard-pessoal'; uv run --python 3.12 --with 'psycopg[binary]' python run_local.py"
   ```
3. Nome: "Dashboard CM Victor"

E adicione um atalho no browser pra `http://127.0.0.1:8000`.
