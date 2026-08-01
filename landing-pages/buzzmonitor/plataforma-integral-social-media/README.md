# LP Buzzmonitor — plataforma-integral-social-media

**Substituída em:** 2026-07-31 (a pedido explícito do usuário, via chat)
**Origem:** HTML trazido pelo usuário no chat, fora do pipeline padrão `/lp-preparar` → `/lp-gerar`. Não existe `copy.txt` fonte original — `copy.txt` deste commit é uma transcrição de auditoria feita a partir do HTML final.
**Região:** LATAM (ES) — `es-419`, GTM `GTM-MKQBX2MG` (mesmo container já validado nesta LP), Meta Pixel `935436740448328`.

Esta versão **substitui inteiramente** o design anterior ("Varias herramientas, cero eficiencia" — ver histórico git para a versão anterior). Slug e domínio (`content.buzzmonitor.com/plataforma-integral-social-media`) permanecem os mesmos; só o conteúdo/design mudou.

## Estrutura

1. HERO — "Toda tu operación de Social Media en una sola plataforma" + 6 tiles flutuantes dos módulos
2. Fila de logos de agências/marcas parceiras (Kaleidoscopio, McCann, Agencia Lead, Sube, Eureka&Co, Havas, TBWA)
3. DESAFIOS — 4 pain points
4. FEATURES — 6 módulos do produto
5. AUDIÊNCIAS — tabs (Agencias / Marcas regionales / Gobierno e instituciones)
6. BENEFÍCIOS — 4 cards
7. TESTIMONIOS — 6 quotes reais de clientes/agências
8. COMPARATIVA — Buzzmonitor vs. Sprinklr/Meltwater/Onclusive
9. CTA-FINAL — form Jotform
10. CLIENTS-PROOF — contadores animados + carrossel infinito de 30 logos de clientes
11. FOOTER

## Estado

- [x] HTML substituído (fluxo ad-hoc — ver "Notas de escopo" abaixo)
- [x] Logos reais de agências e clientes aplicados — baixados de `contenido.getbuzzmonitor.com/agencias` (autorização explícita do usuário) + brand assets locais
- [x] Interatividade: scroll-reveal, contadores animados, tiles flutuantes no hero, carrossel de logos auto-scroll (pausa no hover), tabs acessíveis (ARIA) na seção de audiências
- [x] Formulário integrado — Jotform, form id `241825239057661` (mesmo form já usado nesta LP antes da substituição)
- [x] Meta Pixel `935436740448328` adicionado (não existia na versão anterior desta LP)
- [x] OG image gerada (`assets/og-plataforma-integral-social-media.png`, 1200×630) via template + Chrome headless
- [ ] Auditoria formal `frontend-design` + `web-design-guidelines` (não rodada nesta sessão — ver nota abaixo)

## Notas de escopo (decisões tomadas nesta substituição)

- **Não passou pelo `/lp-revisar` formal.** O design foi construído e iterado diretamente no chat (fora do pipeline), com verificação manual de: contraste/legibilidade visual, estados de hover, acessibilidade dos tabs (roles ARIA, `aria-selected`, `hidden`), `prefers-reduced-motion` (kill-switch já presente cobre as novas animações), e paths de asset (convenção `../../brand/{marca}/assets/...` pra brand assets, `./assets/...` pra assets LP-local, per `landing-pages/CONTEXT.md` §3.2). Recomendado rodar `/lp-revisar` numa próxima iteração pra auditoria formal.
- **Paleta**: laranja `#ff6b16` + rosa `#ec174c` (gradiente), tom mais vibrante que o `--gradient-safe` usado na versão anterior desta LP — decisão do design trazido pelo usuário, não recalibrado pro token `--orange-ink` de contraste AA usado alhures no repo.
- **Duplicata conhecida**: existe uma LP quase idêntica em `landing-pages/buzzmonitor/plataforma-completa-social-media-latam/` (mergeada em main via PR #150/#151, no mesmo dia), criada por outra sessão em paralelo a partir do mesmo HTML de origem. Ela está **desatualizada** em relação a esta versão (não tem a troca de IPG Mediabrands → Agencia Lead, os fixes de hover de Havas/Eureka&Co, nem a interatividade) e **não está atribuída a nenhum domínio**. Ficou como está — o usuário decidiu não mexer nela nesta rodada; considerar remover ou consolidar numa limpeza futura.
- **Testimonios**: 6 quotes reais de clientes/agências (McCann, Kaleidoscopio, Publicis, Eureka&Co, SA365, Sube Agencia) — mesma fonte usada no README da LP duplicada acima (`contenido.getbuzzmonitor.com/agencias`).

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header + footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon + marca decorativa do hero)
- `./assets/og-plataforma-integral-social-media.png` (OG image, LP-local)
- `./assets/logos-agencias/*` (8 imagens — Kaleidoscopio, McCann, Agencia Lead em 2 partes LEAD/DIGITAL, Sube, Eureka&Co, Havas, TBWA)
- `./assets/logos-clientes/*` (30 imagens — Coca-Cola, Sephora, Samsung, IKEA, Amazon, Uber, etc.)
