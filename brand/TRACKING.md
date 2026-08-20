# Tracking: containers GTM por marca e regiao

Fonte de verdade: **`brand/{marca}/tracking.json`**. Este documento explica o modelo, registra o estado real conferido em producao e lista as divergencias conhecidas. Ao criar LP, ler o `tracking.json` da marca, nunca copiar ID de outra pagina nem deste texto.

Ultima conferencia contra repo + producao: **2026-08-19**.

---

## Modelo

Cada marca tem um container por regiao. O `default` e o fallback quando a regiao nao resolve.

```json
{
  "$schema": "tracking/v1",
  "gtm": {
    "default": "GTM-XXXX",
    "regions": { "brasil": "GTM-XXXX", "latam": "GTM-YYYY", "portugal": "GTM-ZZZZ" }
  }
}
```

**A regiao e deduzida do `<html lang>`**, nao da pasta nem do dominio (`landing-pages/build/check_gtm_region.py`):

| `<html lang>` | regiao |
|---|---|
| `es-419`, `es`, `es-MX` | latam |
| `pt-PT` | portugal |
| resto (`pt-BR`) | brasil |

Consequencia pratica: trocar o `lang` de uma pagina muda o container esperado. Clonar LP entre marcas ou regioes exige trocar o GTM junto, senao o gate barra o deploy.

---

## Estado atual

| Marca | brasil | latam | portugal |
|---|---|---|---|
| **buzzmonitor** | `GTM-WFJVK858` | `GTM-MKQBX2MG` | `GTM-NCFT22CW` |
| **cxpress** | `GTM-T4XDWHL3` | `GTM-WRQ47B9R` | `GTM-NW6V5KBM` |
| **buzzcreators** | *null* (ver divergencia 2) | *null* | *null* |
| **elife** | *null* | *null* | *null* |

Uso real nas LPs do repo, para dar lastro a tabela:

| Marca | Regiao | Container | LPs |
|---|---|---|---|
| buzzmonitor | brasil | `GTM-WFJVK858` | 38 |
| buzzmonitor | latam | `GTM-MKQBX2MG` | 19 |
| buzzmonitor | latam | `GTM-PC4TJ6H` | 2 (divergencia 1) |
| buzzmonitor | portugal | `GTM-NCFT22CW` | 4 |
| cxpress | brasil | `GTM-T4XDWHL3` | 25 |
| cxpress | latam | `GTM-WRQ47B9R` | 16 |
| cxpress | portugal | `GTM-NW6V5KBM` | 7 |
| buzzcreators | brasil | `GTM-WFJVK858` | 3 (divergencia 2) |
| buzzcreators | brasil | sem GTM | 5 |
| elife | brasil | sem GTM | 1 |

Marca com `tracking.json` null nao recebe injecao de GTM pela `lp-gerar`, e o gate nao bloqueia (nao ha valor esperado para comparar).

---

## Divergencias conhecidas

### 1. Buzzmonitor LATAM: `GTM-PC4TJ6H` em 2 LPs

`la-mejor-plataforma-social-listening-es` e `ia-para-social-listening-es` usam o container do time ES, confirmado em producao. Ambas tem `.tracking.lock` com `grandfathered: true`, entao passam no gate.

Vale so para essas duas. **Todo o resto do LATAM Buzzmonitor usa `GTM-MKQBX2MG`**, incluindo as LPs de webinar (`que-es-mcp`, `atencion-al-cliente-es`, `webinar-atencion-multicanal-latam`, `primer-listening-5-pasos`, `caso-smartfit`, `gestion-crisis`). Decisao pendente: alinhar o `tracking.json` ou migrar as duas para MKQBX2MG.

> Correcao de registro: circulou internamente que esse container seria `GTM-5PNK2VZ`. **Esse ID nao existe em nenhuma LP do repo nem em producao.** O valor certo e `GTM-PC4TJ6H`.

### 2. Buzzcreators sem container proprio

Tres LPs da marca (`vendendo-com-creators`, `oferta-webinar-influencia`, `oferta-crescer-marca-influenciadores-setembro-2026`) carregam `GTM-WFJVK858`, que e o container **Brasil do Buzzmonitor**. As outras cinco nao tem GTM nenhum.

Ou seja: o trafego dessas LPs cai no container da Buzzmonitor. O `tracking.json` da Buzzcreators segue null, entao o gate nao acusa. Definir se a marca ganha container proprio ou se adota WFJVK858 oficialmente (e ai preencher o `tracking.json`).

### 3. Elife sem container

Uma LP, sem GTM. Mesmo caso da Buzzcreators, em escala menor.

---

## Gate no deploy

`landing-pages/build/deploy_ci.py` roda `check_gtm_region.py` **antes** de publicar. Se alguma LP do manifesto tiver container diferente do esperado para a regiao, o deploy do guarda-chuva inteiro para (`GATE GTM BLOQUEOU`), sem publicar nada e sem rollback, porque nada chegou a subir. Os outros guarda-chuvas do mesmo push seguem normalmente, entao o estado pode ficar parcial.

Status possiveis (`check_gtm_region.py`): `ok` · `wrong` (bloqueia, salvo grandfather) · `absent` (aviso, LP sem GTM) · `no_expected` (aviso, marca sem ID para a regiao) · `no_tracking` (marca sem `tracking.json`, caso da Buzzcreators e da Elife).

O selo `.tracking.lock` cobre **estado pre-existente**, casando por fingerprint do conteudo da LP. Se a pagina muda, o fingerprint muda e o lock para de valer. Nao serve para liberar divergencia em pagina nova.

**Conferir antes de commitar**, sem publicar nada:

```bash
VERCEL_TOKEN=... REPO_ROOT=$PWD py landing-pages/build/deploy_ci.py landing-pages/dominios/{dominio}/manifest.json --dry-run
```

No dry-run o smoke compara o build com o live atual, entao LP alterada acusa "conteudo live != build" e LP nova acusa 404. Isso e esperado. O que importa e nao aparecer `GATE GTM BLOQUEOU`.

---

## Ao criar ou clonar LP

1. Definir a regiao pelo `<html lang>` e pegar o container no `tracking.json` da marca.
2. Clonou de outra pagina? Conferir GTM, `lang` e favicon, que sao os tres que viajam junto sem avisar.
3. Rodar o dry-run acima antes do commit.
4. Marca com `tracking.json` null: nao inventar container. Perguntar antes.

Historico e contexto de incidentes ficam em `landing-pages/CONTEXT.md`.
