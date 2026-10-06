# Revisao LP — buzzmonitor/gerenciar-redes-sociais

**Data:** 2026-10-06
**Hospedagem:** Leadpages (org Tami Buzzmonitor), slug `gerenciar-redes-sociais`, pageId `yu7ci3s9bjxxp9ywz532m0xp`
**Auditores:** ui-craft design-reviewer + a11y-auditor (adaptacao do /lp-revisar para LP fora do pipeline Vercel/CI: sem GTM, hreflang ou logo regional; head e tracking sao da Leadpages)
**Fidelidade da copy:** 0 em-dash. Textos fora do `copy.txt` sao so whitelist (menu, aria, rodape da irma) ou os sinalizados abaixo.

## Aplicado automaticamente (criticos)

- [x] Foco invisivel no botao Fechar do pop-up (roxo sobre roxo): anel branco com apoio escuro
- [x] Esteira com ~60 paradas de Tab: so a linha 1, 1a passada, 18 chips focaveis; duplicados e linhas 2-3 ocultos para tecnologia assistiva; chip focado centraliza e para a esteira; clique num duplicado devolve o foco ao chip real
- [x] Foco laranja sobre fundo branco no hub: anel roxo `#390155` e borda solida no chip
- [x] Foco do poster do video cortado: anel interno
- [x] Preco animado de 0 a 1.790 removido (valor fixo, com `aria-label`); preco com quebra permitida, cabe em 375px
- [x] CTA fixo mobile focavel fora da tela: `visibility:hidden` + `aria-hidden` quando inativo
- [x] Depoimentos so em imagem: `alt` real com texto e autoria; `role=img` trocado por `group`
- [x] Reduced-motion: palavras do H1/sub/CTA nao ficam invisiveis por `animation-delay`
- [x] Extras baratos: `<h3>` de comparacao (era h2), preco em `<p>`, `scroll-padding`, `forced-colors` no texto em degrade, rotulo da lista de selos, barra de progresso `aria-hidden`, foco vai ao iframe apos clicar no video

## Pendencias de copy/oferta (decisao sua, nao aplicadas)

- [ ] **Promessa inconsistente:** "Comece grátis" (menu/hero) x "Experimente grátis por 14 dias" x "Agendar demonstração grátis" levam ao mesmo form. Definir uma oferta so (trial ou demo) e repetir. Hoje o preco aparece sem dizer o que acontece apos os 14 dias.
- [ ] **Titulo da secao de redes** ("Descubra os interesses do seu público...") nao descreve a secao; veio da LP `ia-para-gerenciar-redes-sociais`. Sugestao: titulo que nomeie cobertura de redes e canais.
- [ ] Hero: H1 de 13 palavras abre por superlativo e o lead tem 45 palavras e 3 exclamacoes (mantidas por decisao anterior); CTA pode ficar abaixo da dobra em 375x667
- [ ] Numeros 500+ / 1.000+ aparecem no hero e na prova social

## Melhorias opcionais (nao aplicadas)

- [ ] Gradiente do H1 por palavra e stagger de ~2,3 s (LCP); usar um unico `<em>` ou cor solida
- [ ] Selos flutuantes do hero sem rotulo visivel (estrela, envelope, celular) e duplicam o hub
- [ ] Pop-up: `100vh` -> altura dinamica; anunciar troca de rede (`aria-live`); titulo como h2; lista como `dl`; foco no corpo rolavel
- [ ] Textos < 14px no pop-up (rotulos 11,5px, nota 12,5px)
- [ ] Espacamento de secao abaixo do minimo do GUIDELINES §2 (hub, mod, video); video sem titulo
- [ ] Motion ambiente acima do §4 (10 efeitos); botao "Pausar animacoes" empilha com o CTA fixo no mobile
- [ ] `text-wrap:balance` so no H1 (GUIDELINES §21): estender a H2/subtitulos
- [ ] Teste do form com validacao ativa em 375px (plano B do Jotform)
- [ ] ~50% do CSS herdado da LP irma e morto (`.bz-trust`, `.bz-pt*`, `.bz-ui*`...)
- [ ] `target=_blank` sem aviso; logos de clientes sem nomes; contraste do degrade do H1 (~3:1, texto grande)
- [ ] Depoimentos/logos dependem de assets de outras paginas Leadpages (`escolha-a-buzzmonitor`, `XPHHtX4wus`, `plataforma-de-atendimento-ao-cliente`): se essas paginas forem apagadas, quebram

## Antes de divulgar

- [ ] Enviar um lead de teste na URL publicada (form srcdoc + reCAPTCHA) e conferir UTM no Jotform/CRM
- [ ] Conectar dominio proprio (a URL `lpcontent.net` sai com noindex e barra de Preview)
