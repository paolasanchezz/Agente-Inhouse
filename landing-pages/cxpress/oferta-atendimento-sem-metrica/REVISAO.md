# Revisao LP — cxpress/oferta-atendimento-sem-metrica

**Data:** 2026-07-31
**Auditores:** frontend-design (review mode) + web-design-guidelines + auditorias deterministicas (GTM, copy fidelity, SEO)

## Aplicado automaticamente (3 criticos)

- [x] Aspas retas em copy renderizada (`"atender bem"`, linha 402 do index.html, secao Regra) — GUIDELINES §5 exige aspas curvas. Trocado para `&ldquo;atender bem&rdquo;` no HTML e no copy.txt.
- [x] COPY-VAZAMENTO (punchline de marketing nao aprovada): `form-note` continha "Vagas limitadas por turma de onboarding" — padrao explicitamente listado como CRITICO na auditoria de fidelidade (nao estava em copy.txt). Substituido por disclaimer de consentimento generico ("Ao enviar, você concorda em ser contatado pela Cxpress sobre esta oferta."), categoria whitelist (compliance/form). copy.txt atualizado para refletir.
- [x] GTM stamp desatualizado (`stamp_match=false` na 1a checagem) — rodado `check_gtm_region.py --write-stamp`. Status final: `ok`, GTM-T4XDWHL3 (regiao brasil), 0 bloqueios.

## Melhorias opcionais (3)

- [ ] Input WhatsApp sem `inputmode="tel"` — melhora teclado numerico em mobile. Nao bloqueante (form e mock, sera substituido em `/lp-integrar-form`).
- [ ] Input E-mail sem `spellcheck="false"` — evita sublinhado vermelho do corretor em e-mails. Mesma ressalva (form mock).
- [ ] Stat da secao Impacto (Instituto Hibou, 2020) e a fonte mais proxima e citavel encontrada para o tema "empresas sem metrica de atendimento", mas tem 6 anos. Se surgir pesquisa brasileira mais recente e especifica sobre visibilidade/indicadores de atendimento, trocar.

## Nice-to-haves (0)

Nenhum achado estilistico alem do que ja e padrao herdado da LP-referencia (`oferta-whatsapp-comercial-bloqueado`), ja validada em producao.

## Notas de escopo

- Estrutura clonada 1:1 da LP `oferta-whatsapp-comercial-bloqueado` (mesmo CSS, mesma ordem de secoes) a pedido explicito do usuario — nao passou por `/lp-gerar` (frontend-design generativo), e sim clone + adaptacao de copy, mesmo padrao ja usado em `whatsapp-business-smb-pt`.
- Build do guarda-chuva `content.cxpress.io` validado limpo (37 LPs, sem avisos novos) e gate GTM×regiao em `0 bloqueios`.
- Notion nao conectado nesta sessao — copy nao foi publicada la, apenas local.

## Proximos passos

- Design aprovado? -> `/lp-integrar-form cxpress/oferta-atendimento-sem-metrica "<snippet>"` (quando houver Jotform/RD/HubSpot real)
- Publicar (form mock aceito por ora, ou apos integrar): `/lp-publicar cxpress oferta-atendimento-sem-metrica content.cxpress.io`
