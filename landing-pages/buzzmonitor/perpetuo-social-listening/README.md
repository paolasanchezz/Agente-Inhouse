# LP · perpetuo-social-listening (par captura + tks)

Par de páginas no modelo da CX `content.cxpress.io/video-atendimento`: uma página de captura leva à thank-you page onde o vídeo do webinar fica embedado. **Webinar perpétuo** (a pessoa assiste assim que se inscreve).

| Página | Slug | Papel | robots |
|---|---|---|---|
| Captura | `perpetuo-social-listening` | hero (gancho WhatsApp/40%) + form "preencha e assista" + teaser "o que você vai ver" + autoridade | index |
| Thank-you | `perpetuo-social-listening-confirmado` | vídeo embedado + prova + CTA "fale com especialista" | noindex |

**Fluxo:** captura (Jotform `261904654263661`) → submit redireciona pra `/perpetuo-social-listening-confirmado` → assiste ao vídeo → CTA de WhatsApp.

> ⚠️ **O redirect pra tks agora depende do Jotform, não do código.** O antigo JS (`window.location.href = '/perpetuo-social-listening-confirmado'`) foi removido junto com o form mock. Configure no painel do Jotform → **Settings → Thank You Page → Redirect to an external link** com a URL final `https://webinar.buzzmonitor.com/perpetuo-social-listening-confirmado` (ajustar ao domínio real de publicação). Sem isso, o usuário vê a tela de "obrigado" padrão do Jotform e não cai na tks com o vídeo.

**Vídeo:** `https://youtu.be/fflNMhqjr48` (embed `youtube.com/embed/fflNMhqjr48`).

## Fonte da copy (2026-08-12)

Baseada **só no briefing da Catharina** (título + promessa + Bloco A do vídeo). O roteiro de 22/06 foi **descartado** (não ficou idêntico ao vídeo). Por isso a copy é **teaser**: não detalha feature por feature (decisão "opção A"). O que sobrou é 100% ancorado nos 3 bullets do "o que você sai sabendo".

## Pendências antes de publicar

- **Link do WhatsApp:** os CTAs da tks estão com placeholder `WHATSAPP_LINK_PENDENTE` (2 ocorrências: header e cta-final). Catharina envia o link; trocar as 2.
- [x] **Form integrado:** Jotform `261904654263661` (2026-08-17). **Form provider:** Jotform. Falta configurar o redirect da tks no painel do Jotform (ver aviso no topo).
- **Dados de autoridade (Victor):** confirmar números (1.000+/300+/500+/10mil) e uso das marcas Youse/Turbi/Brisanet como clientes. Não vieram do briefing; é prova de marca pré-existente.
- **OG image:** hoje reusa `og-primeiro-listening-5-passos.png`. Trocar por uma dedicada se quiser.
- **Domínio:** decisão do Victor. Migrado (CI) → publicar via `/lp-publicar` (manifesto + PR; deploy manual bloqueado por hook). Candidatos: `webinar.buzzmonitor.com`, `content.buzzmonitor.com`, `material.buzzmonitor.com`.
- **Revisão formal:** rodar `/lp-revisar buzzmonitor/perpetuo-social-listening` (design + a11y) antes do publish.

## Construção

Estrutura e tokens espelhados das LPs de webinar da Buzzmonitor. Captura **dark premium**; tks **clara** (fundo branco, sancionado pela Catharina em 2026-08-12). Anti-IA aplicado (0 em-dash, grafias oficiais, "a Buzzmonitor" feminino).
