# Catálogo de LPs — Buzzmonitor

> Usado pela skill `/blog-diario` pra escolher a LP de destino dos CTAs (MoFu/BoFu).
> Casa **dor/tema ↔ cluster** + **estágio ↔ intenção**. Sem match → CTA suave + flag.
>
> **Confirmado pelo Victor (2026-06-30):** as 4 LPs abaixo são os destinos das campanhas ativas de
> remarketing/MoFu da conta Buzzmonitor BR (verificado via MCP Meta — campanhas `[BR][CONVERSÃO][Remarketing-IA]`,
> `[...][Agências]` etc.). São, portanto, os alvos prioritários de CTA de conversão.
>
> **UTM:** `{URL}?utm_source=blog&utm_campaign={campaign}&utm_content={slug-do-post}` (utm_source=blog padrão de todas as marcas desde 2026-07-07; marca vem do domínio de destino).

---

## LPs de conversão (destino das campanhas ativas)

| LP / slug | URL | Dor / tema alvo | Funil | utm_campaign | Status |
|---|---|---|---|---|---|
| plataforma-completa | https://conteudo.buzzmonitor.com.br/plataforma-completa | plataforma de inteligência digital completa (geral) — **default de conversão** | MoFu/BoFu | plataforma-completa | live · destino de ads |
| plataforma-completa-listening | https://conteudo.buzzmonitor.com.br/plataforma-completa-listening | social listening / monitoramento de marca | MoFu/BoFu | plataforma-completa-listening | live · destino de ads |
| plataforma-completa-agencias | https://conteudo.buzzmonitor.com.br/plataforma-completa-agencias | agências (gestão de várias marcas/clientes) | MoFu/BoFu | plataforma-completa-agencias | live · destino de ads |
| material-mcp | https://material.buzzmonitor.com/mcp | MCP / IA / integração de dados (material rico) | ToFu/MoFu | mcp | live · material |

---

## Mapa cluster → LP (default por tema)

| Cluster (clusters-brasil.md) | LP sugerida |
|---|---|
| Social Listening | plataforma-completa-listening |
| Métricas & Analytics (ROI) | plataforma-completa |
| Atendimento ao Cliente (SLA) | plataforma-completa |
| IA | material-mcp (se tema for MCP/IA) · senão plataforma-completa |
| Estratégia Social Media | plataforma-completa |
| Conteúdo voltado a **agências** | plataforma-completa-agencias |

Regra de seleção: 1) idioma da região; 2) casar tema do post com a coluna "Dor / tema alvo"; 3) desempate por estágio; 4) sem match claro → `plataforma-completa` (default) ou CTA suave. As 4 são PT-BR (Brasil).
