# REVISAO — cxpress / atendimento-domingo

LP de agendamento de demonstração (BoFu). Refação da LP "Domingo às 22h" (artefato externo)
na identidade visual da Cxpress, com o Samir e revisão anti-IA da copy.

## Origem

Artefato Claude compartilhado pela Marielle em 2026-09-02. A narrativa, a ordem das seções e
a maior parte da copy vêm de lá; o visual e as correções abaixo são desta refação.

## O que mudou no visual

| Item | Antes (artefato) | Agora |
|---|---|---|
| Tipografia | Sora / Work Sans / IBM Plex Mono | Open Sans / Source Sans 3 / Bitter (tokens da marca) |
| Navy do hero | `#0E1230` (genérico) | `#232960` (`primary-dark` da Cxpress) |
| CTA | Âmbar arredondado em pílula | Verde `#21CC78`, raio 9px (padrão banimento-whatsapp / app-whatsapp) |
| Ícones dos cards | Emoji (🤖 ✅ 💬 📊 🎧 🔌 💸 🇧🇷 ⚡ 🧠) | `card__pill` nas cores da marca, alternando primary / accent / warning |
| Seção de dor | Grid de cards | Lista vertical com X vermelho (GUIDELINES §8) |
| Mascote | Não existia | Samir com headset no hero e Samir joinha no fecho, os dois com flutuação em CSS |
| Logos de clientes | 26 data-URIs embutidos | Os 42 PNGs do repo, em marquee (mesmo padrão da banimento-de-whatsapp) |

O fundo azul foi mantido porque a Marielle pediu: hero e fecho são as duas bandas escuras,
funcionando como bookend. Todas as seções de conteúdo entre elas alternam branco e neutral-100.

## O que mudou na copy (anti-IA e precisão)

| Onde | Problema | Correção |
|---|---|---|
| Tabela comparativa | Em-dash (`—`) na célula de implantação | "Não se aplica" |
| Seção Solução | Subtítulo dizia "Quatro coisas" com **seis** cards abaixo | "Seis coisas, e elas aparecem já no primeiro mês." |
| Title vs H1 vs mockup | `<title>` "Domingo às 22h", H1 "10h de domingo", chat "dom 22:14" | Tudo em 22h de domingo |
| Seção Desafios | "Você se identifica com algum destes?" (abertura genérica de LP gerada) | "O que trava o atendimento hoje" |
| Por que trocam | "IA que entende, não robô de menu" (antítese-por-negação) | "Entende a pergunta fora do script" |
| Case, stat row | "Escala no pico", "Custo menor", "Tom preservado" eram rótulos, não números | 8h para 26 min · 34% · Zero contratações (mesmos da vsl-atendimento-ia) |
| Solução, card de áudio | "Ninguém do time para para ouvir" | "Ninguém do time precisa parar para ouvir" |
| Todos os cards | 10 emojis como ícone | Zero emoji na página |

Contagens finais: em-dash 0 · `&mdash;` 0 · antítese-por-negação 0 · filler 0 · emoji 0 ·
exclamações 2 (as duas dentro do mockup de conversa, que é diálogo).

## Pendências

- **Formulário é mock** (GUIDELINES §11). Integrar o Jotform real via `/lp-integrar-form`
  quando o layout estiver aprovado. Os campos já batem com o do Jotform em uso
  (e-mail de trabalho, empresa, faixa de investimento, tamanho do time).
- **Preço divergente entre LPs.** Esta LP diz **R$ 1.750**, que é o que as outras 10 LPs
  da Cxpress em produção dizem. A `vsl-atendimento-ia`, publicada em 2026-09-02, diz
  **R$ 1.290**, valor que a Marielle informou como mínimo de contrato novo. Uma das duas
  está errada e as duas estão no ar. Decisão pendente.

## Correções de layout durante a revisão

- `.hero__inner` no mobile usava `grid-template-columns:1fr`, e o `min-content` do eyebrow
  (com `white-space:nowrap`) estourava a coluna para 396px num viewport de 375. Trocado por
  `minmax(0,1fr)` + `white-space:normal` no eyebrow do hero abaixo de 640px. Mesma troca
  aplicada preventivamente em `.case__cols`, `.trocas`, `.agendar__grid` e `.grid-3`.
- Pisos de tipografia mobile aplicados com `bump_mobile_type.py` (GUIDELINES §20).
- Único overflow horizontal remanescente no mobile é o marquee de logos e a tabela
  comparativa, os dois dentro de container com `overflow` próprio. `scrollWidth` do
  documento fica em 375.
