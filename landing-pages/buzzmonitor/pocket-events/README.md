# Pocket Events — LP modelo

LP modelo para o formato **Pocket Event** da Buzzmonitor: mini-encontro online com **10 vagas**, 1 BD apresentando.

## Status

**Modelo / preview.** Esta pasta serve como base reutilizável para futuras edições de Pocket Event. Cada nova edição pode ser duplicada a partir daqui ou esta mesma pasta pode ser editada e republicada (decisão tomada após validação do diretor).

## Metadata

| Campo | Valor |
|---|---|
| Marca | Buzzmonitor |
| Slug | `pocket-events` |
| Idioma | PT-BR |
| Formato | Pocket Event (10 vagas, 1 speaker BD Buzzmonitor) |
| Domínio futuro | `pocket.buzzmonitor.com` (modo guarda-chuva — várias edições no mesmo projeto Vercel) |
| GTM | **Não** — esta LP não roda em anúncio |
| Form | Mock (`action="#"`) — trocar por embed Jotform via `/lp-integrar-form` antes de cada edição real |
| Favicon | `assets/logos/logo-icon.png` (cópia local do brand) |

## Placeholders a substituir por edição

Antes de cada Pocket Event, substituir no `index.html`:

- `{{ TÍTULO DO ENCONTRO }}` — título do encontro
- `{{ NICHO }}` — nicho/segmento abordado (ex: varejo, financeiro)
- `{{ MÓDULO BUZZMONITOR }}` — módulo principal apresentado (ex: monitoramento, IA, dashboard)
- `{{ DATA }}` — data por extenso (ex: 5 de Junho)
- `{{ HORÁRIO }}` — horário com fuso (ex: 11h, horário de Brasília)
- `{{ NOME DO SPEAKER }}` — nome completo do BD
- `{{ CARGO }}` — cargo do BD na Buzzmonitor
- `{{ BREVE BIO — 1 a 2 linhas }}` — mini-bio
- `{{ DD }}` e `{{ MÊS }}` — dia (2 dígitos) e mês curto no ticket-card
- `{{ TEMA DO ENCONTRO }}` — uma linha de teaser no ticket
- Foto do speaker: substituir `[FOTO DO SPEAKER]` no avatar pela `<img>` real

## Estrutura

```
pocket-events/
├── index.html              # LP completa, single-file, CSS inline
├── copy.txt                # Copy estruturada em blocos rotulados
├── README.md               # Este arquivo
└── assets/
    └── logos/
        ├── logo-icon.png   # Favicon
        ├── mural-1.jpeg    # Mural de clientes — parte 1
        └── mural-2.jpeg    # Mural de clientes — parte 2
```

## Como rodar preview local / público

**Preview local** (servidor estático):
```powershell
python -m http.server 8000 --directory .
```
Abrir `http://localhost:8000` no navegador.

**Preview público temporário** (Vercel `.vercel.app`):
```powershell
vercel
```
Rodar dentro desta pasta. Vai pedir login na 1ª vez. Retorna URL pública temporária. Sem domínio custom anexado.

## Publicação real (futuro)

Quando o diretor aprovar e a 1ª edição real for ao ar:

1. Substituir todos os placeholders por valores reais
2. Trocar form mock por embed Jotform: `/lp-integrar-form buzzmonitor/pocket-events "{snippet}"`
3. Anexar domínio `pocket.buzzmonitor.com` no Vercel (modo guarda-chuva)
4. Rodar `/lp-publicar buzzmonitor pocket-events pocket.buzzmonitor.com`

Se cada edição virar uma subrota (`pocket.buzzmonitor.com/{edicao}`), duplicar esta pasta antes para `landing-pages/buzzmonitor/pocket-event-{slug}/` e ajustar a estrutura sibling.

## Decisões de design

- 2 cores ativas: roxo primary `#390155` + laranja secondary `#EB7C2E` (§1 GUIDELINES)
- Hero clean fundo branco + ticket-card direita (§3 GUIDELINES)
- Form ao lado do speaker na 2ª dobra — lead frio + oferta gratuita (§10 GUIDELINES)
- Sem seção "Problema" nem "Para quem" — formato exclusivo já filtra público (§9 GUIDELINES)
