# buzz-digital-experience-br · Museu das Conversas Perdidas

Versão **PT-BR** da LP `buzz-digital-experience` (que é ES-LATAM). Mesmo desenho, mesma mecânica,
mesmo cenário (o México): só o idioma muda.

Domínio: `content.buzzmonitor.com/buzz-digital-experience-br` (guarda-chuva migrado ao CI).
GTM: `GTM-WFJVK858` (container Brasil). `hreflang` cruzado com a versão ES; `x-default` aponta para a ES.

## Preview local

```bash
python3 -m http.server 8123 --bind 127.0.0.1
```

E abrir `http://127.0.0.1:8123/landing-pages/buzzmonitor/buzz-digital-experience-br/` da raiz do repo.

## O que precisa andar junto com a versão ES

As duas LPs são arquivos independentes (mesmo padrão de `mcp` / `mcp-es` / `mcp-pt`). Toda mudança
de mecânica ou de layout precisa ser aplicada **nas duas**. Os comentários do código seguem em
espanhol nesta cópia, de propósito: são os mesmos da versão original, para o diff entre elas
continuar legível.

## Detecção de país por IP

Desligada, igual à versão ES (`CONFIG.geo = false`). Ligar exige o flag mais os dois hosts no CSP
do domínio — esse segundo passo é mecânica e passa por revisão.

## Formulário

Mock. Integrar o embed real via `/lp-integrar-form` quando o layout estiver fechado.
