# conheca-a-cxpress-confirmado

Página de confirmação pós-inscrição da LP `conheca-a-cxpress`. Não é uma LP de captação: é a etapa intermediária entre o form custom ClickMeeting e a sala do webinar, criada para deixar claro que o inscrito entrou num webinar com sessão em horário marcado (antes, o redirect ia direto pro lobby do ClickMeeting, sem contexto).

URL em produção: `https://content.cxpress.io/conheca-a-cxpress-confirmado`

## Fluxo

1. O form da LP `conheca-a-cxpress` registra o lead via `POST /api/clickmeeting-register` (serverless na sibling, intocada).
2. No sucesso, o JS da LP grava em `sessionStorage` a chave `cx_webinar_confirmation` e redireciona pra cá.
3. Esta página lê a chave e mostra o **estado A** (confirmação + data/hora da sessão + countdown + CTA pra sala). Quando o countdown zera, entra na sala automaticamente após aviso de 10s (cancelável).
4. Sem a chave (visita direta, outro dispositivo, storage bloqueado, sem JS), mostra o **estado B**: "seu link está no email" + próxima sessão via `GET /api/next-webinar`.

## Shape do sessionStorage (`cx_webinar_confirmation`)

```json
{
  "v": 1,
  "join_url": "https://....clickmeeting.com/.../?r=...",
  "email": "pessoa@empresa.com",
  "first_name": "Pessoa",
  "starts_at": "2026-06-10T11:05:00-03:00",
  "formatted_full_pt": "Quarta-feira, 10 de junho · 11h05 (horário de Brasília)",
  "saved_at": "ISO de quando foi salvo"
}
```

Gravado pelo submit handler da LP mãe (`landing-pages/cxpress/conheca-a-cxpress/index.html`). Se o storage falhar lá, a LP degrada pro comportamento antigo (redirect direto pra sala) e esta página nunca é visitada. A chave não é removida na leitura: refresh e voltar-da-sala mantêm o estado A.

## Exceções deliberadas às GUIDELINES

- **`noindex, follow`** (exceção ao §15): página pós-ação, depende de sessionStorage; visitante orgânico cairia no estado B sem contexto. Precedente: `livraria`. O Lighthouse SEO do lp-publicar vai apontar "is-crawlable" como falha: esperado, não "consertar" removendo o noindex.
- **Sem OG image** e sem placeholders `{{DOMAIN}}`: ninguém compartilha esta URL; a validação do lp-publicar é condicional e passa limpo.
- **Sem estrutura mínima de LP** (§6): não há form nem captação aqui.

## Eventos GTM (container GTM-T4XDWHL3)

- `webinar_confirmation_view` (`has_join_url: true|false`) no load.
- `webinar_room_enter` (`method: 'click'|'auto'`) ao entrar na sala.
- O push sozinho não reporta nada: triggers/tags precisam ser criados no container.

## Publicação

Sempre em batch com a LP mãe (deploy atômico, evita janela em que o form redireciona pra 404):

```
/lp-publicar cxpress "conheca-a-cxpress,conheca-a-cxpress-confirmado" content.cxpress.io
```
