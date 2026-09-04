# Guia — um Jotform servindo N webinars perpétuos ("LP Aula")

**Quando usar:** LP de webinar **sem sala e sem data** — a pessoa preenche e assiste na hora, com o
vídeo já gravado na tks. É a "LP Aula" / webinar perpétuo. LP de webinar **com** sessão (ao vivo ou
série recorrente) não entra aqui: essa usa form próprio no `/api/clickmeeting-register`. Árvore de
decisão em [`CONTEXT.md` §2.7](CONTEXT.md).

**O problema:** a Thank You Page do Jotform é configuração **do formulário**, não da LP. Um form =
uma página de agradecimento. Como o plano tem um número limitado de formulários, cada webinar
perpétuo novo queimava um form só pra poder ter o próprio destino pós-envio.

**A solução:** cada LP de captura grava em `sessionStorage` pra onde ela quer levar a pessoa. A
página fixa onde o Jotform aterrissa lê esse valor e encaminha. O formulário fica igual pra todos;
o destino passa a ser decisão da LP.

Criado em 2026-08-26. Em uso no `webinar.buzzmonitor.com` com o form `261904654263661`
(**BR | MKT | Webinar Perpétuo**).

---

## 1. O que foi testado (2026-08-26)

Vale registrar, porque duas hipóteses "óbvias" caíram na verificação:

| Hipótese | Resultado |
|---|---|
| Montar um form nativo na LP e postar direto em `submit.jotform.com/submit/{id}` | ❌ **Não funciona.** O Jotform devolve `Please Complete` com desafio de **CAPTCHA** pra POST que não vem de uma sessão dele. Testado com e sem os campos de anti-bot (`jsExecutionTracker`, `submitSource`, `submitDate`, `buildDate`). Submissão barrada por captcha **não** grava nada. |
| Escutar `submission-completed` / `submission-started` via `postMessage` do iframe | ❌ **Não chega.** O `submission-completed` não existe no JS do formulário (só no script do parent, para o "inline embed"). O `submission-started` existe, mas é chamado como `window.parent.postMessage({...})` **sem `targetOrigin`** — o padrão nesse overload é `"/"` (mesma origem), então a mensagem é descartada num parent cross-origin. |
| O redirect do Jotform consegue sair do iframe | ✅ **Sim.** A documentação genérica deles diz que não, mas o embed atual navega a **janela de topo**. Verificado: envio feito num harness em `127.0.0.1` levou a aba inteira pra `https://webinar.buzzmonitor.com/perpetuo-social-listening-confirmado`, em tela cheia. |

A terceira linha é o que sustenta o desenho: o redirect funciona bem, o único defeito é o destino
ser fixo por formulário. Daí a ideia de deixar o Jotform redirecionar pra uma página só e
encaminhar de lá.

## 2. As duas peças

### 2.1 Na LP de captura — registrar o destino

O embed ganha um `data-perpetuo-next` com o caminho da tks **desta** LP:

```html
<div class="jotform-embed" data-perpetuo-next="/{slug}-confirmado">
  <script type="text/javascript" src="https://form.jotform.com/jsform/261904654263661"></script>
</div>
```

E, dentro do IIFE do `<script>` no fim do `<body>`:

```js
var slot = document.querySelector('[data-perpetuo-next]');
if (slot) {
  try {
    sessionStorage.setItem('bmPerpetuoNext', JSON.stringify({
      to: slot.getAttribute('data-perpetuo-next'),
      at: Date.now()
    }));
  } catch (e) { /* sessionStorage bloqueado: cai no destino padrao do Jotform */ }
}
```

Grava no **carregamento** da página, não no envio — não há como detectar o envio de dentro de um
iframe cross-origin (§1). Isso é correto porque **a última LP carregada ganha**, e a última LP
carregada é sempre aquela de onde a pessoa enviou o formulário. Quem abre a LP A, navega pra B na
mesma aba e envia em B, sai com o destino de B.

### 2.2 Na página onde o Jotform aterrissa — encaminhar

Bloco no **início do `<head>`**, antes de qualquer render, pra não piscar o vídeo errado:

```html
<script>
  (function () {
    try {
      var raw = sessionStorage.getItem('bmPerpetuoNext');
      if (!raw) return;
      sessionStorage.removeItem('bmPerpetuoNext');
      var d = JSON.parse(raw);
      if (!d || typeof d.to !== 'string') return;
      if (d.to.charAt(0) !== '/' || d.to.charAt(1) === '/') return;  // so caminho interno
      if (Date.now() - (d.at || 0) > 1800000) return;                // vale 30 min
      var norm = function (p) { return p.replace(/\/+$/, ''); };
      if (norm(d.to) === norm(location.pathname)) return;            // ja e aqui
      location.replace(d.to);
    } catch (e) { /* sem sessionStorage: segue nesta pagina */ }
  })();
</script>
```

Quatro travas, nessa ordem: **consome a chave antes de qualquer decisão** (nunca entra em loop),
aceita **só caminho interno** (`/algo`, nunca `//host` — não vira open redirect), **expira em
30 min** e **não redireciona pra si mesma**.

## 3. Estado atual e o passo que falta

Hoje a Thank You Page do form `261904654263661` aponta pra
`https://webinar.buzzmonitor.com/perpetuo-social-listening-confirmado`. Por isso o despachante do
§2.2 mora **nessa** página: é onde todo mundo cai. Funciona, e não exigiu nenhuma mudança no
Jotform.

**Limpeza recomendada (1 minuto, uma vez, no painel do Jotform):** criar uma LP mínima de despacho
(ex: slug `obrigado`, `noindex`, só com o bloco do §2.2) e apontar a Thank You Page do formulário
pra `https://webinar.buzzmonitor.com/obrigado`. Aí:

- a tks da `perpetuo-social-listening` volta a ser só uma tks (o bloco do §2.2 sai de lá);
- nenhuma tks de webinar fica servindo de corredor pras outras;
- quem chegar em `/obrigado` sem chave precisa de um destino padrão — definir qual.

Enquanto isso não for feito, o arranjo atual é o que está no ar e está correto.

## 4. Webinar perpétuo novo — checklist

1. Gerar o par de LPs (`{slug}` de captura + `{slug}-confirmado` com o vídeo).
2. Na LP de captura, usar o embed do §2.1 com `data-perpetuo-next="/{slug}-confirmado"` e o
   registrador no `<script>`.
3. Adicionar os 2 slugs ao manifesto do domínio e publicar via `/lp-publicar`
   (`webinar.buzzmonitor.com` é migrado pro CI — PR, nunca deploy manual).
4. Testar no ar: preencher, confirmar que caiu no **vídeo certo** e que o lead apareceu no Jotform.
5. **Nada a configurar no Jotform.** É esse o ganho.

## 5. Pegadinhas

- **Não existe evento de GTM no envio.** O form é um iframe cross-origin e o `submission-started`
  não atravessa (§1). Medir conversão pelo **pageview da tks** (`/{slug}-confirmado`), que é o
  padrão pra form embedado — não tentar instrumentar o submit.
- **`parentURL` continua sendo transmitido**, então o widget *Get Parent URL* segue alimentando o
  `url_conversao` no CRM e os leads não saem das dashboards de CM. Esse é um motivo forte pra
  manter o embed em vez de trocar por form nativo, além do captcha.
- **`sessionStorage` é por aba.** Abrir a tks numa aba nova, na mão, não tem chave — e por isso
  não redireciona, o que é o comportamento desejado.
- **Navegação privada ou storage bloqueado** cai no destino padrão do Jotform (hoje, a tks da
  social-listening). Degrada, não quebra: o lead é gravado do mesmo jeito.
- **Um form, uma lista de campos.** Se um webinar precisar de pergunta própria, aí sim precisa de
  formulário separado.
- **De onde veio o lead?** Pelo campo *Get Page URL* / `url` da submissão, que guarda a URL da LP.

## 6. Onde isso está em uso

| LP de captura | Form | Destino (`data-perpetuo-next`) |
|---|---|---|
| `buzzmonitor/perpetuo-social-listening` | `261904654263661` | `/perpetuo-social-listening-confirmado` |

Saiu em 2026-09-02: `buzzmonitor/perpetuo-monitoramento-concorrentes`. O par virou webinar **ao
vivo** (série ClickMeeting `18043`) e agora usa o form nativo + as serverless functions do
guarda-chuva, não o Jotform. Ver o README da LP.

Saiu em 2026-09-04: `buzzmonitor/perpetuo-monitoramento-concorrentes-pt`, pelo mesmo motivo (série
`18086`, Portugal). Esse par nunca chegou a usar o Jotform: tinha form **mock** que só redirecionava
para a tks com o vídeo.

Despachante (§2.2) hoje em: `buzzmonitor/perpetuo-social-listening-confirmado`.
