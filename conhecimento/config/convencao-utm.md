# Convencao de UTM — Fonte Unica de Verdade

> Este arquivo e o unico lugar onde a regra de nomenclatura de UTM fica definida.
> Qualquer skill ou pessoa que monte link de conversao (LP, newsletter, e-mail, blog,
> criativo, assinatura) le a regra daqui. Se a convencao mudar, atualizar SO este arquivo.

Vale para **todo link nosso que aponta para uma pagina de captacao** (LP de proposta,
LP de material, LP de evento). Link de navegacao interna (logo -> home, ancora na propria
pagina) nao leva UTM.

---

## 1. Os dois parametros obrigatorios

| Parametro | O que responde | Regra |
|---|---|---|
| `utm_source` | **De onde veio o lead** — a fonte | Vocabulario fechado da §2 |
| `utm_content` | **Qual conteudo e qual tipo de pagina** geraram o lead | `{tipo-de-pagina}-{conteudo}` (§3) |

Todo link de conversao carrega esses dois. Sem `utm_source` **e** sem `url_conversao` o lead
desaparece do filtro das dashboards de CM (`landing-pages/CONTEXT.md` §2.7).

`utm_medium` e `utm_campaign` sao **opcionais** — use quando houver mais de um veiculo ou mais
de uma campanha dentro da mesma fonte e voce precisar separa-los no relatorio. Nunca use
`medium`/`campaign` como substituto de `source`/`content`.

## 2. Vocabulario de `utm_source`

A fonte e o **canal que entregou o lead**, nao o formato nem a marca (a marca sai do dominio
de destino).

| Valor | Quando |
|---|---|
| `webinar` | Webinar ao vivo ou perpetuo (LP de inscricao, LP de agradecimento, sala) |
| `email` | Disparo pontual de e-mail (nutricao, remarketing, convite) |
| `newsletter` | Newsletter recorrente |
| `blog` | Post de blog — vale para TODAS as marcas |
| `material` | Material rico (guia, estudo, playbook, planilha) |
| `evento` | Evento presencial ou hibrido |
| `social` | Post organico em rede social |
| `assinatura` | Assinatura de e-mail do time |
| `lp` | Uma LP nossa linkando outra LP fora dos casos acima |

Fonte nova entra nesta tabela **antes** de aparecer num link.

## 3. Como montar o `utm_content`

`utm_content` = **tipo de pagina + conteudo especifico**, nessa ordem, em kebab-case.

| Tipo de pagina | Token |
|---|---|
| Pagina de agradecimento / confirmacao | `agradecimento` |
| LP de captacao (inscricao, download) | `captacao` |
| Pagina de oferta pos-webinar | `oferta` |
| Resultado de quiz / teste | `resultado` |
| Post de blog | o proprio `{slug-do-post}` (o tipo ja vem do `utm_source=blog`) |

Exemplos:

```
# thank-you de webinar perpetuo (no ar em perpetuo-monitoramento-concorrentes-confirmado)
?utm_source=webinar&utm_content=agradecimento-perpetuo-monitoramento

# thank-you de material rico
?utm_source=material&utm_content=agradecimento-social-listening-guia

# post de blog -> LP comercial (aplicado pela /blog-diario)
?utm_source=blog&utm_campaign=banimento-whatsapp&utm_content={slug-do-post}
```

## 4. Formato (nao negociavel)

- Minusculas, kebab-case, sem acento e sem espaco: `agradecimento-perpetuo-monitoramento`.
- Sem underscore (`thank_you_page` e legado, nao replicar).
- Sem o nome da marca — a marca sai do dominio de destino (`content.buzzmonitor.com`,
  `content.cxpress.io`).
- Valor estavel: UTM ja publicada nao se renomeia sem motivo, senao a serie historica
  do relatorio quebra em duas.

## 5. Divergencias conhecidas (nao replicar)

- **6 paginas de agradecimento de perpetuo usam `utm_source=perpetuo`** no lugar de `webinar`
  (`perpetuo` e formato, nao fonte): `buzzmonitor/atencion-al-cliente-es-confirmado`,
  `buzzmonitor/caso-smartfit-confirmado`, `buzzmonitor/primer-listening-5-pasos-confirmado`,
  `buzzmonitor/que-es-mcp-confirmado`, `cxpress/webinar-bloqueo-whatsapp-confirmado`,
  `cxpress/webinar-whatsapp-pt-confirmado`. Unificar exige tocar as 6 em producao —
  decisao pendente do Victor.
- `utm_medium=thank_you_page` + `utm_content=cta-comercial` em
  `buzzmonitor/social-listening-guia-es-confirmado`: snake_case legado, e o `content` diz o
  lugar do botao em vez do conteudo que gerou o lead.
- LPs de resultado do teste de maturidade usam `utm_source=buzzmonitor` (marca como fonte).

---

## Referencias cruzadas

- `landing-pages/CONTEXT.md` §5.5 — aplicacao em CTA de LP
- `.claude/skills/blog-diario/CONTEXT.md` §Convencao UTM — aplicacao em CTA de blog
