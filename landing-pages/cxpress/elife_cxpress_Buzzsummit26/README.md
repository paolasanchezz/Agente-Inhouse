# elife_cxpress_Buzzsummit26

LP de captura do Buzz Summit 2026 no guarda-chuva **content.cxpress.io**.
URL final: `https://content.cxpress.io/elife_cxpress_Buzzsummit26` (o slug mantém a caixa exata, Vercel distingue maiúsculas).

- **Estrutura:** header preto com o SVG do lockup Elife | Cxpress | Buzz Summit 2026 (o SVG traz o próprio fundo preto), uma única seção com o formulário e rodapé idêntico ao de `/institucional`.
- **lang:** `pt-BR` · **GTM:** `GTM-T4XDWHL3` (brasil).
- **Formulário:** Jotform `261027611029650`, embed de **HTML completo** (não o iframe/`jsform`), colado na íntegra de `message (6).txt`. Os campos ocultos de UTM, gclid e `url` são preenchidos pelo próprio Jotform a partir da URL da página (validado: `?utm_source=...` chega em `input_11`, e o widget Get Page URL preenche `input_18`).
- **Ajustes de estilo** sobre o tema do Jotform ficam no bloco `.form-card .form-*` do `<style>` (largura 100%, fontes 16px, botão azul da LP).
- **CSP:** o HTML completo carrega CSS/fontes de `cdn.jotfor.ms` e o widget de `widgets.jotform.io`. Por isso o `vercel.json` do domínio ganhou `https://*.jotfor.ms` em `style-src`/`font-src` e `https://*.jotform.io` em `script-src`. Sem isso o form fica sem estilo e o campo `url` não é preenchido.
- **Assets:** `assets/logo-elife-cxpress-buzzsummit26.svg` e `assets/og-elife_cxpress_Buzzsummit26.png` (1200x630, logo sobre preto).
- **Rodapé:** o título "Termos e Políticas" tem 12px, igual ao de `/institucional` (é o único texto abaixo de 14px no mobile).
