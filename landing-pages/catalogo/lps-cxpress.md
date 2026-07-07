# Catálogo de LPs — Cxpress

> Usado pela skill `/blog-diario` pra escolher a LP de destino dos CTAs (MoFu/BoFu).
> A skill casa **dor/tema ↔ cluster** + **estágio de funil ↔ intenção do post**. Sem match → CTA suave + flag.
>
> **Status de confiança:** URLs `content.cxpress.io/{slug}` confirmadas via README das LPs no repo.
> `home.cxpress.io/atendimento-omnicanal-whatsapp` confirmada via post de referência ("Banimento no WhatsApp").
> Demais `home.cxpress.io` marcadas **(confirmar)**. **Victor:** revise dor/estágio/URL e o token `utm_campaign` de cada linha.
>
> **UTM:** `{URL}?utm_source=blog&utm_campaign={campaign}&utm_content={slug-do-post}` (utm_source=blog padrão de todas as marcas desde 2026-07-07; marca vem do domínio de destino).

---

## LPs evergreen (preferir para CTA de blog)

> **Confirmado pelo Victor (2026-06-30):** `atendimento-digital`, `coex-whatsapp`, `banimento-whatsapp` e `atendimento-clinicas` são os destinos das campanhas ativas de remarketing/MoFu (Cxpress BR), verificado via MCP Meta. São os alvos prioritários de CTA. `atendimento-digital` = **default de conversão** (campanhas smb/gatilhos e público-frio apontam pra ele).

| LP / slug | URL | Dor / tema alvo | Funil | utm_campaign | Status |
|---|---|---|---|---|---|
| Página de produto — atendimento omnicanal WhatsApp | https://home.cxpress.io/atendimento-omnicanal-whatsapp | API oficial, centralização, migração de WhatsApp | MoFu/BoFu | (por tema do post) | live (ref.) |
| Home / produto | https://home.cxpress.io/ | visão geral da plataforma | ToFu/MoFu | home-cxpress | live |
| conheca-a-cxpress | https://content.cxpress.io/conheca-a-cxpress | conhecer a plataforma (webinar institucional) | ToFu/MoFu | conheca-cxpress | live |
| atendimento-digital | https://content.cxpress.io/atendimento-digital | atendimento digital multicanal | MoFu | atendimento-digital | live |
| atendimento-clinicas | https://content.cxpress.io/atendimento-clinicas | atendimento p/ clínicas (vertical saúde) | MoFu | atendimento-clinicas | live |
| banimento-whatsapp | https://content.cxpress.io/banimento-whatsapp | banimento WhatsApp / risco de ferramenta não-oficial | MoFu/BoFu | banimento-whatsapp | live |
| coex-whatsapp | https://content.cxpress.io/coex-whatsapp | experiência/atendimento via WhatsApp (confirmar foco) | MoFu | coex-whatsapp | live |
| gestao-canais-ia-2026 | https://content.cxpress.io/gestao-canais-ia-2026 | gestão de canais com IA | MoFu | gestao-canais-ia-2026 | live (OG pendente) |
| playbook-whatsapp2026 | https://content.cxpress.io/playbook-whatsapp2026 | material/ebook WhatsApp 2026 | ToFu/MoFu | playbook-whatsapp2026 | live |

## Materiais / eventos LATAM (ES) — usar só em posts ES-LATAM

| LP / slug | URL | Tema | Funil | utm_campaign | Status |
|---|---|---|---|---|---|
| ebook-marketing-conversacion-latam | https://content.cxpress.io/ebook-marketing-conversacion-latam | ebook marketing conversacional (ES) | ToFu | ebook-conversacion-latam | live |
| latam-webinar-atencionalcliente | https://content.cxpress.io/latam-webinar-atencionalcliente | webinar atención al cliente (ES) | ToFu | latam-atencion-cliente | sazonal/datado |

## Webinars / ofertas datadas (baixa prioridade p/ blog evergreen)

| LP / slug | URL | Observação |
|---|---|---|
| webinar-tecnologia-maio2026 (+ -oferta, -oferta-latam) | https://content.cxpress.io/webinar-tecnologia-maio2026 | datado (maio/2026) — não usar em post evergreen |
| webinar-tecnologia-pt (+ -oferta-pt) | https://content.cxpress.io/webinar-tecnologia-pt | webinar PT-PT, datado |
| consumidores-sinteticos-evento | https://content.cxpress.io/consumidores-sinteticos-evento | evento datado |
| conheca-a-cxpress-confirmado | https://content.cxpress.io/conheca-a-cxpress-confirmado | página de confirmação (noindex) — **nunca** é destino de CTA |
| livraria | (interna) | biblioteca de componentes — **não é LP de captação** |

---

## Regra de seleção (resumo)

1. Filtrar por idioma da região (LATAM → só LPs ES; Brasil → PT-BR).
2. Casar dor/tema do post (do cluster) com a coluna "Dor / tema alvo".
3. Desempate por estágio: preferir a LP cujo funil = intenção do post.
4. Excluir datadas/internas (confirmação, livraria, webinars passados).
5. Nenhuma compatível → sem CTA duro: CTA suave (link interno / "conheça a Cxpress") + flag no relatório.
