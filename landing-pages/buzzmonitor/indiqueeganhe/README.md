# LP Buzzmonitor — indiqueeganhe

**Gerado em:** 2026-07-01
**Copy-fonte:** `copy.txt` (output de /lp-preparar, a partir da copy revisada em `conhecimento/copywriting/revisoes/lp-indique-e-ganhe-buzzmonitor-revisado-2026-07-01.md`)

## Estrutura

- Hero (H1 + sub + CTA "Indicar agora" + link "Entenda como funciona" + vídeo embed YouTube Shorts)
- Quem pode indicar (grid 4 personas: cliente ativo, ex-cliente, colaborador, aluno)
- Como funciona (stepper 4 passos)
- Recompensas (seção escura, 2 colunas: para você / para o seu indicado)
- Quem vale a pena indicar (4 desafios de ICP + imagem `assets/quem-vale-a-pena.png` + 4 segmentos-alvo em caixinhas lilás, numa fileira centralizada abaixo)
- CTA final + formulário (Jotform embed)
- Regulamento (6 itens + contato)
- Footer

## Estado

- [x] HTML gerado
- [x] Revisão (frontend-design review + web-design-guidelines) — última rodada 2026-08-14, ver `REVISAO.md` (3 bugs e 4 pontos de design corrigidos; 5 melhorias e 3 nice-to-haves antigos fechados)
- [x] Formulário integrado
- [x] Publicado — `https://content.buzzmonitor.com/indiqueeganhe` (guarda-chuva `content.buzzmonitor.com`, deploy pelo CI a partir da main; entrada no manifesto desde o PR #209).
- [ ] **Deploy solo antigo ainda no ar:** `https://buzzmonitor-lp-indiqueeganhe.vercel.app/indiqueeganhe` responde 200, indexável e com canonical próprio, competindo com a URL do guarda-chuva. Retirar do ar ou marcar `noindex` (decisão pendente do Victor).
- [ ] **Jotform pendente de ajuste** (botão verde, label-por-placeholder, "REQUIRED" em inglês, link de privacidade com URL antiga) — ver `REVISAO.md`, seção "Aberto — depende de decisão". Nada foi alterado no form: são 188 submissões em produção.

**Form provider:** Jotform (form id `242464989976077`), integrado em 2026-07-02.
**Vídeo do hero:** YouTube Shorts embed (`https://www.youtube.com/embed/BZ2oA2FWvGU`), integrado em 2026-07-02.
**Imagem "quem vale a pena":** `assets/quem-vale-a-pena.png` (1672×941), enviada pelo Victor via Drive, integrada em 2026-08-05.

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `./assets/quem-vale-a-pena.png` (imagem LP-local, seção "Quem vale a pena indicar")

## Pendências conhecidas

- **OG image:** gerada em 2026-07-02 (`assets/og-image.png`, 1200×630, via `assets/og-template-indiqueeganhe.html` + Chrome headless).
- **GTM:** injetado com `GTM-WFJVK858` (região brasil, resolvido de `brand/buzzmonitor/tracking.json`). Stamp gravado.
- **Domínio:** ainda não definido — placeholders `{{DOMAIN}}` e `{{OG_IMAGE_PATH}}` no HTML serão substituídos pelo `/lp-publicar`.
- **Notion:** a copy não foi publicada no Notion (sem MCP conectado na sessão em que rodou `/lp-preparar`). Um MCP Notion está disponível agora — pode publicar retroativamente se quiser.
