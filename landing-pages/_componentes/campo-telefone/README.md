# campo-telefone

Campo de telefone com seletor de país por bandeira, usado no formulário das LPs de webinar
perpétuo (ClickMeeting). Entrou em 2026-09-23, obrigatório nas 9 LPs de séries ativas.

- O visitante escolhe o país na bandeira; o `+DDI` aparece na frente do número.
- No envio, `CampoTelefone.ler(form)` devolve o número **só com dígitos, DDI + número, sem `+`**
  (`5511987654321`), que é o formato gravado no ClickMeeting (campo 11).
- Aceita o que a pessoa costuma digitar: `(11) 98765-4321`, `011 98765-4321`, o DDI repetido
  (`55 11 9...`) e colar `+52 55 1234 5678` ou `00351 912...` (troca o país sozinho).
- Valida a quantidade de dígitos por país (faixa larga: pega erro de digitação, não valida
  operadora). "Outro país" aceita código + número, de 8 a 15 dígitos.
- País inicial = `data-pais` da LP. Nas LPs em espanhol, um navegador `es-CO`/`es-AR`/... troca
  pro país dele; nas LPs em português, não (navegador pt-BR não quer dizer número brasileiro).
- Bandeiras em SVG embutido: o Windows não desenha emoji de bandeira, e o CSP dos
  guarda-chuvas aceita `img-src data:`.

## Arquivos

| Arquivo | O que é |
|---|---|
| `campo-telefone.js` | Componente (bandeiras, países, validação, `window.CampoTelefone`) |
| `campo-telefone.css` | Prefixo por cima do input + lista de países. O input herda o estilo do form da LP |
| `sincronizar.py` | Copia CSS e JS pra dentro das LPs, entre marcadores `campo-telefone:inicio/fim` |

As LPs são HTML autocontido, então o componente vive **embutido** em cada uma. **Não edite a
cópia dentro da LP**: edite aqui e rode

```bash
py landing-pages/_componentes/campo-telefone/sincronizar.py
```

`--check` só confere (sai com 1 se alguma LP estiver defasada). O CSS entra no fim do último
`<style>` do `<head>` (o primeiro costuma ser o `<noscript><style>` do `.reveal`, que só vale
sem JS); o JS entra antes do `</body>`.

## Ligar o telefone numa LP nova

1. Markup, depois do campo Empresa (mesma classe de campo da LP: `cm-field` ou `field`):

   ```html
   <div class="cm-field" data-campo-telefone data-pais="BR">
     <label class="cm-label" for="cmPhone">Telefone</label>
     <div class="pf-box">
       <input id="cmPhone" type="tel" name="phone" required autocomplete="tel-national" inputmode="tel" maxlength="20">
     </div>
   </div>
   ```

   Use `div`, não `label`, no invólucro: dentro de um `<label>`, clicar no rótulo abriria a
   lista de países em vez de focar o número. `data-pais`: `BR` (PT-BR), `PT` (PT-PT), `MX` (ES).
   Rótulo: Telefone (PT-BR e PT-PT) / Teléfono (ES).

2. No submit, depois de montar o `payload`:

   ```js
   var telefone = window.CampoTelefone ? CampoTelefone.ler(form) : { ok: false, empty: true, message: '' };
   if (/* campos obrigatórios vazios */ || telefone.empty) { setFeedback('...e telefone.', null); return; }
   if (!telefone.ok) { setFeedback(telefone.message, null); return; }
   payload.phone = telefone.value;
   ```

3. Acrescentar a LP na lista `LPS` do `sincronizar.py` e rodá-lo.

A function `clickmeeting-register.js` exige `phone` e manda em `registration[11]` (campos e
regras no README de `_clickmeeting-api/`). A sala nova do ClickMeeting precisa ter o campo
Telefone no formulário de inscrição.
