# Design · Post 1 · Dia dos Namorados · 12/06/2026

> **Status**: design preenchido via API, **revisão visual necessária no Canva**
> **Tipo de teste**: validação end-to-end da skill /social-canva sem dataset autofill (modo direto via editing operations)

## Link

- **Editar no Canva**: https://www.canva.com/d/nxA7iZJr6snI7mW
- **Design ID**: DAHMXdOQiVU
- **Template base**: EAHMXaCZdd4 (Aplicar Kit de Marca Buzzmonitor)

## Mapeamento copy → páginas

Post 1 da [copies-junho.md](../copies/copies-junho.md) tinha 7 slides. O template tem 5 layouts de carrossel (1080×1350) + 1 página de referência do Canva (1350×1350, ignorada). Condensei pra 5 slides mantendo a narrativa:

| Página do template | Layout original | Slide do Post 1 | Texto preenchido |
|---|---|---|---|
| 1 | Cover "Um lembrete" | **Cover** | "A flor virou clichê. O jantar virou status. E a marca campeã do Dia dos Namorados nem fala de amor." |
| 2 | Stat "73%" | Setup + descoberta (slides 2+3 condensados) | "**3.118**" + "conversas em 8 dias revelaram um padrão claro: as flores estão saindo de moda." + "A geração Z já chama de clichê." |
| 3 | Quote | Slide 4 (jantar > flores) | "Prefiro um momento a um buquê. No lugar das flores: jantar, viagem, experiência." |
| 4 | "Dica rápida" | Slide 6 (Apple, punchline) | "A GRANDE SURPRESA: A marca campeã nem fala de romance. Foi a Apple. 20,5% dos posts. 100% positivos." |
| 5 | Manifesto | CTA (slide 7) | "Aspiração não saiu de moda. Só mudou de embalagem." + "Quer ler o consumidor antes da próxima data? Link na bio." |
| 6 | Página de referência Canva | — | (ignorada — não exportar) |

**Nota:** slide 5 da copy original (Shopee/ML 78%) foi cortado pra caber em 5 páginas. Quando o template tiver layout adicional pra mais dados, esse insight pode entrar.

## Iterações do teste

**v1 (primeira rodada)**: texto vazou do container em 2 lugares (página 1: overline "Buzz Pills · Dia dos Namorados 2026" + título longo, e página 4: overline "A GRANDE SURPRESA:" muito grande). Layout visual ficou bagunçado.

**v2 (corrigido)**: 3 textos encurtados pra respeitar tamanho dos containers originais. Regra incorporada à skill `/social-canva` (Passo 4.3.5): texto novo deve ficar dentro de ±20% do tamanho original.

- Página 1 overline: "Buzz Pills · Dia dos Namorados 2026" (35 chars) → **"BUZZ PILLS"** (10 chars)
- Página 1 título: longo → **"A marca campeã do Dia dos Namorados não fala de amor."** (53 chars)
- Página 4 overline: "A GRANDE SURPRESA:" (18 chars) → **"A SURPRESA:"** (11 chars)

## Limitações conhecidas

1. **Página 6 (referência do Canva) precisa ser excluída** antes de exportar o carrossel.
2. **Sem dataset fields** — esse teste foi feito via edição direta de elementos por ID, abordagem mais frágil que autofill com dataset. Quando os campos forem configurados, a skill fica mais robusta.

## Próximos passos

1. Abrir [o design no Canva](https://www.canva.com/d/nxA7iZJr6snI7mW) e revisar visualmente página por página
2. Ajustar tamanho de fonte / posição de caixa onde houver overlap
3. Excluir página 6 (referência)
4. Exportar como PNG/JPG em ordem
5. Programar no Meta Business Suite com a caption do feed (na [copies-junho.md](../copies/copies-junho.md))

## Caption do feed (cola direto no Instagram)

```
Enquanto você decidia o presente, a gente decidiu ouvir.

Em 8 dias monitorando Dia dos Namorados nas redes, descobrimos que a flor não é mais o presente clássico. E que quem dominou a conversa nem entra na maioria das listas de "ideias românticas".

Deslize. No fim, o nome surpreende.

🔗 Análise completa: link na bio.
```
