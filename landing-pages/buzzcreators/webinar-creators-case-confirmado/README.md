# Tks Buzzcreators — webinar-creators-case-confirmado

**Gerado em:** 2026-11-11
**Tipo:** pagina do video da LP Aula [`../webinar-creators-case/`](../webinar-creators-case/). `noindex`.

## O que tem (v5, 2026-11-11: so titulo + video + CTA, a pedido do time)

1. Selo pequeno "Pronto! Seu acesso foi liberado" + H1 com o titulo da aula: "Webinar Employee advocacy: rede de moda vendeu 3x mais que a mídia paga" (v6, pedido do time em 2026-11-11). Com o Jotform nao ha nome personalizado.
2. Video do YouTube (`kR0Iq1bFWLc`) com **autoplay no mudo a partir de 3:00**, tocando dentro da pagina
   - Botao roxo "O video ja comecou. Clique para ouvir" cobre o player: ativa o som e volta para 3:00
   - Trava: se o navegador comecar fora de 3:00, volta uma vez para 3:00
   - Tela final propria no lugar das sugestoes do YouTube ("Assistir de novo" + "Conhecer o Buzzcreators")
   - Se a IFrame API nao carregar em 8s, cai num iframe simples com autoplay no mudo
   - Constantes `VIDEO_ID` e `VIDEO_START` no topo do `<script>`
3. Botao "Conhecer o Buzzcreators" abaixo do video (pagina comercial com UTM)
4. Rodape com redes sociais e politica de privacidade

Sairam na v5: selo "Assista agora · 12 min", subtitulo, roteiro "Neste video", resumo (governanca + 4 pilares), faixa de numeros, pergunta de fechamento e o card do Buzzmonitor.

Paleta: so roxo e branco, sem laranja.

## Tracking

- `dataLayer`: `lead_webinar_perpetuo_01` no load e `webinar_perpetuo_01_som_ativado` no clique do som. Conversao do lead = pageview desta pagina (o envio do Jotform nao gera evento, ver GUIA §5).
- GTM nao injetado (container `null` em `brand/buzzcreators/tracking.json`).
- CTA segue `conhecimento/config/convencao-utm.md`: `utm_source=webinar&utm_content=agradecimento-perpetuo-creators-case` (a marca sai do dominio). Desde a v5 so existe o CTA do Buzzcreators. Mesma aba, UTMs fixas, nao repassa as UTMs da URL.

## Limites conhecidos

- O YouTube nao deixa esconder o logo nem o "Assistir no YouTube" com o video pausado.
- No mudo o YouTube pode mostrar legenda automatica.
- Testado so no Chrome. Safari/iOS e celular em economia de bateria nao verificados.

## Estado

- [x] HTML gerado e testado (form mock → tks, nome, autoplay em 3:00, som, tela final, 375px sem scroll lateral)
- [x] Link da politica de privacidade: `https://buzzmonitor.com.br/privacidade`
- [x] v3 (2026-11-11): laranja trocado por roxo (botao de som, ponto do selo, chips, numeros). Video conferido: `kR0Iq1bFWLc`, autoplay no mudo a partir de 3:00
- [x] Revisao (2026-11-11): 3 criticos aplicados. Melhorias em [`REVISAO.md`](REVISAO.md)
- [ ] Testar no Safari/iOS e no celular (autoplay no mudo + botao de som)
- [ ] Publicado junto com a LP de captura
