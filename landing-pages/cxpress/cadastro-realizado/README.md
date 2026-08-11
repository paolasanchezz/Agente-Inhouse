# LP Cxpress — cadastro-realizado

Thanks page de confirmação de cadastro. Recriação, dentro do nosso pipeline (`content.cxpress.io`),
da página `home.cxpress.io/obrigado` — hoje hospedada no site institucional em GreatPages, fora do
pipeline de LPs e sem acesso de edição direto por aqui.

**Gerado em:** 2026-08-11
**Copy-fonte:** transcrição literal de `home.cxpress.io/obrigado`, ver `copy.txt`.

## Origem e diferença deliberada da fonte

A pedido do usuário, dois elementos da página original foram **removidos**, não apenas adaptados:

1. O botão "Falar no WhatsApp" (link `https://api.whatsapp.com/send?phone=551150395028&...`).
2. O texto de apoio "Caso prefira, clique no botão abaixo do Whatsapp e já seja atendido. (Nossa
   equipe atende de segunda a sexta das 9h às 18h.)" — removido junto com o botão, seguindo o
   precedente de `video-atendimento-obrigado` (2026-08-03): sem o botão, o texto prometia um
   contato sem caminho.

O menu de Soluções e o rodapé extenso (Termos, Documentações, redes sociais) do site institucional
**não foram replicados** — decisão explícita do usuário de seguir o padrão simples já usado nas
thanks pages do nosso pipeline (logo no header + rodapé mínimo), em vez de reproduzir o site
completo.

## Estrutura

- CONFIRMAÇÃO (ícone de check + H1 "Cadastro realizado com sucesso." + subtítulo)
- FOOTER (mínimo)

## Estado

- [x] HTML gerado
- [x] Revisão — ver `REVISAO.md` (1 crítico aplicado: logo faltando no footer)
- [ ] Publicado

## Exceções deliberadas às GUIDELINES (precedente: video-atendimento-obrigado / conheca-a-cxpress-confirmado)

- **`noindex, follow`**: página pós-ação; o Lighthouse SEO do lp-publicar vai apontar "is-crawlable"
  como falha — esperado, não "consertar".
- **Sem OG image, sem OG/Twitter/JSON-LD e sem placeholders `{{DOMAIN}}`**: ninguém compartilha esta
  URL.
- **Sem estrutura mínima de LP** (§6): não há form nem captação aqui, é só confirmação.

## Notas

- GTM injetado: `GTM-T4XDWHL3` (região brasil, mesmo container das demais LPs Cxpress BR).
- Ainda não se sabe qual formulário do site institucional redireciona para esta página — a URL de
  destino real (`content.cxpress.io/cadastro-realizado`) precisa ser configurada onde quer que o
  form aponte hoje para `home.cxpress.io/obrigado`, se a intenção for substituir o destino em produção.

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
