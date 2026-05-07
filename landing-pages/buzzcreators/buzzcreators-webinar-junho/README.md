# LP Buzzcreators — Webinar Junho

Webinar gratuito Vendendo com Creators (Buzzcreators) — versao com slug `buzzcreators-webinar-junho` no guarda-chuva `webinar.buzzmonitor.com`.

## Origem

LP **recuperada do live** em 2026-05-07. Foi publicada de outra maquina (deploy `dpl_AVT1U37u4ZDMQpyTLQVTsxTrK9pv`) **sem passar pelo pipeline padrao** (`/lp-preparar` -> `/lp-gerar` -> `/lp-revisar`) e **sem commit** no repo. Reconstituida a partir do download do deploy production via Vercel API e revertendo paths absolutos (`/assets/buzzcreators/...`) para padrao source (`../../brand/buzzcreators/assets/...`).

## URL ao vivo

`https://webinar.buzzmonitor.com/buzzcreators-webinar-junho` (modo guarda-chuva — projeto `buzzmonitor-lp-monitoramento-concorrentes`)

## Assets

| Asset | Path source | Origem |
|---|---|---|
| `favicon.png` | `../../brand/buzzcreators/assets/logos/favicon.png` | Brand existente — match MD5 com o live |
| `logo-color.png` | `../../brand/buzzcreators/assets/logos/logo-color.png` | **Promovido para o brand** nesta sessao (PNG do logo Buzzcreators que so existia no deploy) |
| `bruno-filho.png` | `https://evento.buzzmonitor.com/assets/buzzcreators/bruno-filho.png` | Cross-domain — referencia LP `vendendo-com-creators` no `evento.buzzmonitor.com` |

## Debito tecnico

- **Sem `copy.txt`** — texto editavel da LP nao foi extraido do HTML; pode ser feito por reverse engineering se vier proxima iteracao.
- **Sem `REVISAO.md`** — nao passou por `/lp-revisar` (faltam auditorias de GTM, a11y, anti-IA, etc).
- **Cross-domain dependency**: `bruno-filho.png` vem do `evento.buzzmonitor.com`. Funciona enquanto a LP `vendendo-com-creators` daquele projeto estiver no ar; quebra se ela sair. Idealmente mover para `landing-pages/buzzcreators/buzzcreators-webinar-junho/assets/` ou `brand/buzzcreators/assets/people/`.

## Atualizar

```
/lp-publicar buzzcreators buzzcreators-webinar-junho webinar.buzzmonitor.com
```

A fonte vive aqui. Editar `index.html`, rodar o comando.
