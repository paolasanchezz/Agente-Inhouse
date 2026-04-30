# Livraria · Agente Inhouse

Catálogo interno de animações e componentes CSS para uso em landing pages do grupo Elife.

**Live:** https://content.cxpress.io/livraria

## O que é

Página de referência com 59 espécimes prontos para colar em LPs — preview ao vivo + código limpo + zero dependências. Cobre tudo que aparece com frequência em LPs nossas: loaders, botões, cards, animações de texto, formulários, listas tipadas (problema-X / benefício-✓), métricas, pills/badges, formas decorativas Cxpress (pílulas + arcos do brandbook) e padrões compostos (accordion, tooltip, sticky CTA, scroll reveal, skeleton).

## Categorias (14 / 59 espécimes)

| # | Categoria | Espécimes |
|---|---|---|
| 01 | Loaders | 6 |
| 02 | Botões | 5 |
| 03 | Cards | 4 |
| 04 | Texto | 4 |
| 05 | Objetos | 6 |
| 06 | Fundos | 4 |
| 07 | Hover | 4 |
| 08 | Entradas | 4 |
| 09 | Formulários | 4 |
| 10 | Listas | 3 |
| 11 | Métricas | 3 |
| 12 | Pills & Badges | 4 |
| 13 | Decorativos Cxpress | 3 |
| 14 | Avançados | 5 |

## Por que está hospedada em `content.cxpress.io`?

Domínio guarda-chuva já existe (vide `landing-pages/CONTEXT.md` §4.2). É a única página do tipo "ferramenta interna" no domínio, mas a paleta foi rebrandada para tokens Cxpress (azul royal + laranja + amarelo, fontes Open Sans/Source Sans 3/Bitter), então não destoa.

## Branding aplicado

- **Tema:** dark (deep navy `#0d1124`) — apropriado pra catálogo de código
- **Acento primário:** `#EF863C` (laranja Cxpress)
- **Acento secundário:** `#F1A908` (amarelo Cxpress)
- **Fontes:** Bitter (display, italics editoriais), Source Sans 3 (body), JetBrains Mono (código), Open Sans (botões)
- **Brand mark:** quadrado laranja com spinner CSS (vide `.brand-mark`)

## Atualizar

Esta LP **não usa o pipeline lp-publicar** porque é página interna single-file (sem brand assets locais, sem GTM, sem form). Para atualizar:

1. Editar `landing-pages/cxpress/livraria/index.html` no repo
2. Copiar para sibling: `cp landing-pages/cxpress/livraria/index.html "C:/Users/titof/Downloads/Claude/cxpress-lp-playbook-whatsapp2026/livraria/index.html"`
3. Deploy: `cd "C:/Users/titof/Downloads/Claude/cxpress-lp-playbook-whatsapp2026" && npx vercel deploy --prod --yes`

Smoke test obrigatório pós-deploy (validar que a vizinha `playbook-whatsapp2026` não regrediu):

```bash
curl -sI -o /dev/null -w "livraria: %{http_code}\nplaybook: %{http_code}\n" "https://content.cxpress.io/livraria" "https://content.cxpress.io/playbook-whatsapp2026"
```

Os dois devem retornar 200.

## noindex

A página está marcada como `noindex` (mas `follow`) — é referência interna, não deve aparecer em busca pública.
