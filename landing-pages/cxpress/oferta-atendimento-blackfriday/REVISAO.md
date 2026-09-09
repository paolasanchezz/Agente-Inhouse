# Revisao LP — cxpress/oferta-atendimento-blackfriday

**Data:** 2026-09-09
**Auditores:** design review (GUIDELINES.md, 10 seções) + Web Interface Guidelines (Vercel Labs) + auditorias determinísticas (GTM, SEO, fidelidade de copy)

## Aplicado automaticamente (3 críticos)

- [x] **A11y — foco removido em campos de formulário.** `.field input:focus { outline: none; }` desativava o indicador de foco visível do teclado nos 4 campos do form, contrariando o padrão `:focus-visible` (3px accent) usado no resto da página. Removido o `outline: none`; o campo agora recebe a borda azul (mouse/touch) **e** o outline global de `:focus-visible` (teclado).
- [x] **Tipografia mobile — `.cnpj-card h3` 1px abaixo do piso.** GUIDELINES §20 pede mínimo 22px pra título de card; estava fixo em 21px. Ajustado para 22px.
- [x] **OG image ausente.** Gerada via template (`assets/og-template.html`) + Chrome headless, 1200×630px, salva em `assets/og-oferta-atendimento-blackfriday.png` (nome canônico, sem duplicata `og-image.png`).

## Auditorias determinísticas — todas OK

- **GTM:** container `GTM-T4XDWHL3` (região brasil) confere com `tracking.json`. Selo `.tracking.lock` gravado.
- **SEO:** description (1), robots (1), canonical (1), Open Graph (10, mínimo 8), Twitter (4, mínimo 4), JSON-LD (1, parseia válido).
- **Fidelidade de copy:** texto visível do HTML confere 1:1 com `copy.txt`. Única adição fora da copy: labels de formulário (Nome, E-mail de trabalho, Telefone, Nome da empresa) e skip-link — ambos whitelist.
- **Em-dash:** 0 ocorrências.
- **Logos:** `logo-primary.svg` e `logo-reversed.svg` sem `<text>` vivo (não serifam).
- **Header/footer:** logo aponta pra `home.cxpress.io` com `target="_blank" rel="noopener"`, não para `/`.

## Melhorias opcionais (3)

Para o usuário decidir. Não aplicadas.

- [ ] **CTA final sem destaque visual.** GUIDELINES §8 sugere fundo destacado pra seção de CTA final; hoje "Depois da virada" usa o mesmo fundo branco das seções anteriores. Poderia ganhar um tom de fundo (`primaryLighter` ou `primary`) pra fechar a página com mais impacto.
- [ ] **`spellcheck="false"` no campo de e-mail.** Detalhe de polish das Web Interface Guidelines — evita que o navegador sugira correção ortográfica no endereço de e-mail.
- [ ] **Logo do footer sem `loading="lazy"`.** Está abaixo da dobra; lazy-load é opcional aqui dado o tamanho pequeno do arquivo.

## Nice-to-haves (1)

- [ ] `text-wrap: balance` no H1/H2 pra evitar quebras de linha desequilibradas em telas largas.

## Próximos passos

- Formulário: integrar o Jotform da página de referência (`https://form.jotform.com/jsform/261045149477663`) via `/lp-integrar-form`
- Publicar: `/lp-publicar cxpress oferta-atendimento-blackfriday content.cxpress.io`
