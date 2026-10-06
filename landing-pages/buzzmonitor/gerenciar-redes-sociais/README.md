# LP Buzzmonitor — gerenciar-redes-sociais

**Gerado em:** 2026-10-06
**Copy-fonte:** `copy.txt` (Notion: Copy LP · Buzzmonitor · gerenciar-redes-sociais · 2026-10-05)
**Hospedagem:** Leadpages (org Tami Buzzmonitor), slug `gerenciar-redes-sociais`, pageId `yu7ci3s9bjxxp9ywz532m0xp`. **Rascunho (não publicada).**
**Base:** LP irmã `plataforma-de-atendimento-ao-cliente` (tema, form Jotform em srcdoc, esteiras, rodapé).

## Estrutura

Menu, Hero (H1 + stats), Solução completa (+ form), **Hub de redes (esteira de chips + pop-up)**, Monitoramento, Relacionamento Multicanal, Análises (+ comparativo), Vídeo (facade YouTube `42tvEPRKQAo`), Planos, Prova social (números + esteira de depoimentos), Empresas (esteira de logos), Rodapé.

## Hub de redes (ref. Pluga)

3 linhas × 40 chips (20 + cópia p/ loop), linha 2 em sentido contrário, 100 s linear, pausa no hover/foco. Clique no chip pausa a esteira e abre `<dialog>` com os dados da rede (`build/src/redes.json`, vindos da LP `ia-para-gerenciar-redes-sociais`); fechar retoma. 18 redes, ícones em `build/src/icons.json`. Chips e modal são montados por `page.js` a partir de `nets.js`; sem JS / no editor da Leadpages aparece só a lista de nomes.

## Build

`node build/_build.js` regenera `build/nets.js`, `build/styles.css` (= `styles.base.css` + `src/extra.css`), `build/leadpages.html` e `index.html` (dev). IDs dos assets enviados à Leadpages em `build/assets.json`. Para nova versão: subir `styles-vN.css`/`page-vN.js`/`nets-vN.js` e trocar os links por `update_page`.

## Texto fora do `copy.txt` (confirmar)

- Seção do hub: título "Descubra os interesses do seu público e destaque sua marca" (sem "!") e dica "Clique numa rede e veja como funciona", reaproveitados da LP `ia-para-gerenciar-redes-sociais`. Conteúdo do pop-up idem.
- Rodapé da irmã (descrição, cidades) conforme pedido; `© Buzzmonitor 2025` e @handles do copy.txt não foram usados.
- Vídeo sem título visível (a copy não traz).

## Estado

- [x] HTML gerado e testado local (desktop + mobile 375, esteira, pop-up, form)
- [x] OG image 1200×630 → `assets/og-gerenciar-redes-sociais.png` (subida e aplicada via `update_page_seo`)
- [ ] Revisão (`/lp-revisar`)
- [ ] Teste de envio real do form (srcdoc + reCAPTCHA no domínio final)
- [ ] Publicar (`publish_page_draft`) e domínio próprio (preview `lpcontent.net` sai noindex)
