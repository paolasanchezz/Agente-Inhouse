# LP Buzzmonitor — obrigado-pt

Página de agradecimento geral dos eventos PT, em `content.buzzmonitor.com/obrigado-pt` (`noindex`).
Pedido do Ulises em 2026-10-22.

**Para que serve:** é a Thank You Page do Jotform "Webinars Portugal" (`261127236463050`). Esse
form é partilhado por várias LPs, e a Thank You Page do Jotform é uma só por formulário. Esta
página funciona como despachante: se a LP de captura deixou um destino, encaminha para lá; se não,
mostra o agradecimento genérico.

## Como funciona

1. A LP de captura grava o destino num cookie `bm_next` em `.buzzmonitor.com` (Max-Age 30 min).
   Cookie, e não `sessionStorage`, porque a captura vive em `webinar.buzzmonitor.com` e esta página
   em `content.buzzmonitor.com`: `sessionStorage` não atravessa subdomínio.
2. O Jotform redireciona a janela inteira para esta página.
3. O script no topo do `<head>` lê o cookie, apaga-o e faz `location.replace` para o destino.
   Só aceita `https` em `buzzmonitor.com` ou subdomínio (sem open redirect) e não redireciona para
   si mesma.
4. Sem cookie (LP que não registou destino, navegação privada, cookie bloqueado): fica aqui.

## LPs que registam destino

| LP de captura | Destino |
|---|---|
| `webinar.buzzmonitor.com/perpetuo-monitoramento-vsl-pt` | `/perpetuo-monitoramento-vsl-pt-confirmado` |

LPs que usam o form sem registar destino (caem no agradecimento genérico):
`territorios-marca-mundial-2026`, `webinar-territorios-marca-mundial-junho-2026`.

## Pendências

- **Configurar no Jotform (uma vez):** Thank You Page do `261127236463050` → redirecionar para
  `https://content.buzzmonitor.com/obrigado-pt`. Sem isso, nada passa por aqui.
- **Efeito nas outras LPs do form:** passam a ver este agradecimento genérico no lugar do atual.
- Quem abriu a `perpetuo-monitoramento-vsl-pt` e, em menos de 30 min, se inscreveu noutra LP do
  mesmo form na mesma sessão do browser cai no vídeo da VSL. Caso raro; aceite.
