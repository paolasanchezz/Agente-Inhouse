# LP Buzzmonitor · mcp-claude-latam

**Version viva:** v3 (`index.html`) · historico em [VERSIONS.md](VERSIONS.md)
**Gerado em:** 2026-09-10
**Copy-fonte:** `copy.txt` (copy do brief do Ulises + ajustes da v3)
**Regiao:** latam (`es-419`) · **GTM:** GTM-MKQBX2MG
**Objetivo:** funil MCP, valor, prova e intencao comercial (agendar demo)

## Direcao visual (v2)

Fundo escuro (`#0A0507`) com degradados ambar, laranja e vermelho, tipografia display enorme e muito respiro.
Referencias pedidas: nickho-motorsports.nl (jerarquia e grid), crency.agency (motion), filmbot.com (bloco `spotlight` com MacBook).

Paleta: laranja `#EB7C2E` + vermelho `#DE2451` + ambar `#FCBD4F` sobre preto quente. Uma unica familia de degradado
(`--grad-display`) em titulares display, bordas e brilhos. Os botoes usam `--grad-cta` (ambar para laranja) com texto
quase preto, porque branco sobre laranja reprova AA.

## Estrutura

1. HERO: eyebrow, H1 display, H2 em degradado, intro, **MacBook com spotlight e a gravacao real da conexao**, 3 passos, caixa da URL com botao de copiar e **card do Paso 0** com o CTA "Crear cuenta gratis"
2. TICKER: 8 capacidades do MCP em marquee
3. PRUEBA: oferta 50% OFF com contador
4. VALOR: H2 display + lista editorial 01 a 06
5. CONVERSACION: 4 prompts
6. EQUIPOS: argumento + 4 checks + form mock (posicao MoFu/BoFu, GUIDELINES §10)
7. CIERRE: display gigante em degradado + 3 CTAs
8. FOOTER

## Estado

- [x] HTML gerado (v2)
- [x] Revisao tecnica (GUIDELINES §4, §7, §9, §10, §12, §14, §15, §17, §19, §20)
- [ ] OG image 1200x630 em `assets/og-mcp-claude-latam.png` (arquivo unico, nunca `og-image.png`)
- [x] Formulario integrado (Jotform `241825239057661`, 2026-09-10)
- [ ] Publicado: `/lp-publicar buzzmonitor mcp-claude-latam [dominio]`

## Pendencias que precisam de decisao humana

1. **URL de "Probar gratis" e "Crear cuenta gratis".** Apontam para `https://getbuzzmonitor.com/es/?utm_source=lp&utm_content=lp-mcp-claude-latam`. Trocar pela URL canonica de signup/trial se existir.
2. **Dominio.** `content.buzzmonitor.com` (conteudo ES-LATAM) ou `material.buzzmonitor.com` (onde vivem `mcp`, `mcp-es`, `mcp-pt`).
3. **OG image** ainda nao gerada.
4. **Ticker do MCP.** As 8 capacidades sao copy nova (nao vinham do brief). Nao inclui "crea dashboards a medida en segundos" do exemplo do Ulises: a copy desta LP nao afirma que o MCP gera dashboards e nao consegui confirmar contra o produto. Se gerar, e so uma linha a mais.

**Form provider:** Jotform (`241825239057661`), integrado em 2026-09-10 via `/lp-integrar-form`. O iframe e cross-origin: o interior do formulario **nao** se estiliza daqui. O card em volta virou claro para que o branco do provedor pareca intencional.

## Video do hero

`assets/conectar-mcp-claude.mp4` (217 KB, H.264, 1024x640, 13,7 s, sem audio) + poster JPG.

Derivado da gravacao de tela do Ulises (`conectar mcp buzzmonitor.mp4`, 1920x1080 HEVC, 3,7 MB). O que foi feito:

- **Cortada a barra lateral do Claude**, que mostrava titulos de conversas pessoais ("Mejores formas de acceder a Claude", "Dashboard de analisis de datos inbound", "Optimiza mi landing page") e o rodape "Ulises · Free". Isso nao pode ir para uma pagina publica.
- Cortados os primeiros 2,8 s ("Buenas tardes, Ulises"), que tambem traziam o nome do usuario.
- Recorte final de 1172x733 do painel de conteudo, reescalado para 1024x640 (16:10 do MacBook), reencodado para H.264 sem audio, com `+faststart`.

O video comeca em Personalizar e termina com o conector verificado. **Se a gravacao for refeita, repetir o mesmo recorte** ou revisar quadro a quadro que nao sobre nenhum dado pessoal.

## Animacoes

Revelacao palavra a palavra nos titulares display, reveal por IntersectionObserver com stagger `--d`, abertura da tampa
do MacBook ligada ao scroll (rotateX 15deg para 0 mais escala), tilt por mouse, cursor com halo ambar, botoes magneticos,
ticker da URL, contador do 50%, desenho dos checks, hover com degradado nas filas 01 a 06 e nav que vira pilula.

Fallbacks (GUIDELINES §4): classe `.js` no `<html>` (sem JS nada fica escondido), `<noscript><style>`, failsafe de
3,5 s e bloco `prefers-reduced-motion` que zera transform e opacity **e pausa o video**. Validado nos dois modos.

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.png` (header e footer, recortado por `.logo-clip`)
- `./assets/conectar-mcp-claude.mp4` e `./assets/conectar-mcp-claude-poster.jpg`
