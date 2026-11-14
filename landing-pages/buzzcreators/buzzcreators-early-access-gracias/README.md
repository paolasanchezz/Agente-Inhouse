# LP Buzzcreators — buzzcreators-early-access-gracias

**Gerado em:** 2026-11-13 (a pedido do Ulises)
**Tipo:** pagina de agradecimento (tks) da lista de espera `/buzzcreators-early-access`, ES-LATAM
**URL:** `https://content.buzzmonitor.com/buzzcreators-early-access-gracias`

## Estrutura

1. Confirmacao: H1 "Ya estás en la lista." + o que acontece agora + nota de spam, com um "passe" de acesso antecipado animado (entra girando, recebe o selo "Confirmado" + confete)
2. Lo que viene: 2 cards
3. Compartilhar: botao que abre o menu nativo no celular (Web Share) e copia o link da LP de captura no desktop
4. Footer

Mesmo sistema visual da LP de captura (degradê preto -> Rich Purple, laranja Sundown so como acento). `noindex, follow`, sem OG/JSON-LD (precedente `buzzmonitor/inscripcion-confirmada`: ninguem compartilha a tks). Sem GTM (`brand/buzzcreators/tracking.json` null). Conversao medida pelo pageview desta URL (Vercel Web Analytics do guarda-chuva).

## Como a pessoa chega aqui (pendente)

O form da LP de captura e o Jotform **compartilhado** `241825239057661` (usado por ~15 LPs Buzzmonitor LATAM), entao a Thank You Page dele NAO pode apontar pra ca sem afetar as outras. Caminhos:

- **Form proprio:** clonar o form no Jotform pra Buzzcreators e apontar a Thank You Page do clone pra esta URL (e trocar o ID no embed da LP de captura).
- **Despachante (GUIA-webinar-perpetuo-destino.md):** a LP de captura ja grava `data-perpetuo-next="/buzzcreators-early-access-gracias"` no `sessionStorage`; falta o bloco §2.2 na pagina onde o form `241825239057661` aterrissa hoje (destino configurado so no painel do Jotform).

## Estado

- [x] HTML gerado, em-dash 0, sem overflow em 390px, sem erro de JS
- [ ] Conectado ao form (ver acima)
