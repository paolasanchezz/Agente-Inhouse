# LP Buzzmonitor — consumidor-sintetico

**Gerado em:** 2026-11-09
**Copy-fonte:** `copy.txt` (output de /lp-preparar) · Notion: https://app.notion.com/p/4133934026fd81f99666ed0d343d4ce2
**Região:** brasil (pt-BR) · GTM `GTM-WFJVK858`
**Funil:** MoFu/BoFu (agendar demonstração). Form na última seção + CTA do hero/header rolando até `#demo`.

## Estrutura (v2.2, ajustes de 2026-11-10)

**Hero (versão A, escolhida pela Thamires em 2026-11-10):** texto à esquerda + mosaico orgânico de 9 retratos à direita; um retrato por vez ganha destaque (cor, zoom, borda laranja e rótulo demográfico), a cada 2,3 s. No celular o rótulo aparece como legenda abaixo do mosaico. A versão B (retratos correndo por trás do texto) foi descartada e apagada.

1. Nav: pílula escura flutuante com logo + CTA
2. Hero: H1 com "Consumidor Sintético:" grande + "saiba o que seu consumidor pensa em minutos", subtítulo, 2 CTAs, mosaico de 9 retratos, faixa com 3 diferenciais
3. Ticker: 10 itens testáveis
4. Solução: chapéu "O que são Consumidores Sintéticos?" + card escuro dividido + retrato com 3 cards de dado (1.000, IBGE, REDES SOCIAIS)
5. Como funciona: 3 cards com mini-telas (`#como-funciona`)
6. Diferencial: comparativo em 3 colunas
7. Pausa: "1.000" gigante + avatares
8. Módulos: grade de 6 cards
9. Resultados: grade com 6 ✓
10. Para quem: 5 cards numerados
11. Prova: case Maracugina (logo pendente, aguardando arquivo oficial)
12. Plataforma: chapéu "Uma plataforma completa" + faixa escura com 5 itens + faixa do MCP (movida para depois do case)
13. CTA final: bloco escuro + form mock (`#demo`)
14. Footer

Removidos nos ajustes: seção Problema, FAQ, overline do hero, aviso "Exemplo ilustrativo", carrossel 3D.

## Referências visuais

Pinterest (aprovadas pela Thamires): `1089941547344244124` (cards de foto arredondados), `1017672847073561362` (carrossel 3D de retratos + grade de cards), `1085297210228504613` (títulos em duas cores, card escuro dividido + cards de dado sobre retrato, navbar escura).

## Decisões de design (desvios conscientes das GUIDELINES)

- **Hero centralizado** (§3 pede texto à esquerda): segue a referência do carrossel de retratos.
- **Fundo creme `#F6F2EB`** com cards brancos, areia e lilás (§1 pede branco ↔ neutral-100): paleta contida das referências. Cor forte só no laranja (acento/CTA) e no roxo-escuro (`#1C0F25`, blocos escuros).
- **Texto do CTA laranja em quase-preto** (o brand pede branco): branco sobre `#EB7C2E` dá cerca de 2,9:1 e reprova AA.
- **Cinza dos títulos em duas cores `#837B87`**: cerca de 3,4:1 sobre o creme, aprovado para texto grande (só usado em títulos ≥ 30px).
- **Tipografia:** League Spartan em peso 600 (títulos), Instrument Serif itálica para um trecho de destaque por título, Hanken Grotesk no corpo (substitui Lato e HK Grotesk para um visual mais atual).
- **Fotos reais de banco gratuito** como retratos dos consumidores sintéticos (aviso "Exemplo ilustrativo" removido a pedido da Thamires).
- **H1 em benefício, sem seção de problema** (§3 pede dor no H1): decisão da Thamires em 2026-11-10.

## Créditos das fotos (Unsplash, licença gratuita; atribuição não obrigatória)

Arquivos em `assets/`, recortados e comprimidos para web (~970 KB no total). IDs de origem (`https://unsplash.com/photos/{id}` via `images.unsplash.com/photo-{id}`):

| Arquivo | Photo ID |
|---|---|
| p-02.jpg | 1580489944761-15a19d654956 |
| p-03.jpg | 1611695434369-a8f5d76ceb7b |
| p-04.jpg | 1662850886700-4ec19bd30d11 |
| p-05.jpg | 1573515159471-0eb7ec72912c |
| p-06.jpg | 1749189516333-168cfd97de0b |
| p-07.jpg | 1759765468070-120cdc180be8 |
| p-08.jpg | 1604261605115-4b34b646a05c |
| p-10.jpg | 1588676478223-cea188261d35 |
| p-11.jpg | 1507003211169-0a1dd7228f2d |
| p-12.jpg | 1583264277168-58ceba4b84e7 |
| p-13.jpg | 1600603406200-5b2a104684ac |
| p-17.jpg | 1779630986800-f0ed643f357b |

## Pendências

- Logo da Maracugina (arquivo oficial) para o case.
- 4 rótulos demográficos novos no hero (63 Florianópolis B1, 71 Fortaleza C2, 23 Salvador C1, 25 Curitiba B2): conferir se fazem sentido.

## Pendências de copy (marcadas `[VALIDAR]` no copy.txt)

- Se a demo roda teste com audiência do mercado do lead (BODY do CTA final).
- Número/depoimento autorizado do case Maracugina.

Resolvidos em 2026-11-10: nome "Hipóteses de Pesquisa" e descrições de Focus Group, UX e Gestão de Crises (texto da Thamires).

## Estado

- [x] HTML gerado (SEO completo, JSON-LD válido, GTM nos 2 blocos, em-dash 0, mobile 375px sem overflow, pisos §20 ok)
- [x] OG image 1200×630 → `assets/og-consumidor-sintetico.png`
- [x] Revisão (2026-11-10): 5 críticos aplicados, melhorias em `REVISAO.md`
- [x] Formulário integrado

**Form provider:** Jotform 252995108251662 (2026-11-10)
- [ ] Publicado — rodar `/lp-publicar buzzmonitor consumidor-sintetico [dominio]` (sugestão: `material.buzzmonitor.com`)

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon + faixa do MCP)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (nav escura e footer; raster, sem `<text>`)
- `./assets/p-*.jpg` (12 retratos, ver créditos acima)
