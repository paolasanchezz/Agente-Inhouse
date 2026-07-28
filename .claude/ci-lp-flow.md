<!-- title: CI/CD de LPs — conteúdo vs mecânica -->

# Fluxo de CI/CD — Landing Pages (guarda-chuva)

```mermaid
flowchart TD
    A[Push / PR pra main<br/>tocando landing-pages/** ou brand/**] --> B{lp-pr.yml<br/>Valida PR de LP}

    B --> C[Build de TODOS os guarda-chuvas<br/>build_umbrella.py]
    C --> D[pr_check.py classifica o diff]

    D --> E{Diff é 100% CONTEÚDO?<br/>landing-pages/marca/**<br/>manifestos · brand/*/assets/**}

    E -->|Sim: só conteúdo de LP| F[Auto-merge squash<br/>via GITHUB_TOKEN]
    F --> G[Dispara lp-deploy.yml<br/>workflow_dispatch por domínio]
    G --> H[deploy_ci.py:<br/>build determinístico + smoke test<br/>de todas URLs do manifesto]
    H -->|smoke OK| I[✅ No ar<br/>comentário automático no PR]
    H -->|smoke falha| J[🔁 Rollback automático<br/>pro deploy anterior]

    E -->|Não: toca skills/, build/,<br/>.github/, vercel.json,<br/>ou remove LP existente| K[🔒 Label<br/>precisa-revisao-victor]
    K --> L[Victor revisa e aprova<br/>merge manual]
    L --> M[push direto na main<br/>dispara lp-deploy.yml<br/>por push-event]
    M --> H

    style F fill:#1a7f37,color:#fff
    style K fill:#d93f0b,color:#fff
    style I fill:#1a7f37,color:#fff
    style J fill:#d93f0b,color:#fff
```

## Regra-chave

| Tipo de mudança | Caminho | Gate |
|---|---|---|
| **Conteúdo de LP** (copy, HTML, assets, manifesto) | Auto-merge → auto-deploy | Só precisa passar build+smoke |
| **Mecânica** (skills, `build/`, `.github/`, `vercel.json`) ou **despublicação** de LP | Bloqueado pra revisão humana | Precisa aprovação do Victor |

Isso significa: **alterar uma skill que mexe no pipeline de LP (`lp-preparar`, `lp-gerar`, `lp-publicar`, scripts em `landing-pages/build/`) nunca sobe sozinho** — mesmo que o PR também contenha uma LP nova, o diff inteiro cai em "precisa-revisao-victor" porque toca mecânica, não só conteúdo.

Também há o gate `check_gtm_region.py` (§5.4 do CONTEXT) dentro do `deploy_ci.py`/`pr_check.py`: bloqueia deploy/merge se o container GTM não bater com a região declarada da LP — independe de ser conteúdo ou mecânica.
