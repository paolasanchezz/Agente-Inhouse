# LP Buzzcreators — encontrar-creators

**Gerado em:** 2026-09-11
**Copy-fonte:** `copy.txt` (output de `/lp-preparar`)
**Briefing-fonte:** PDF "Buzzcreators | Briefing e prompt da LP, Creators para sua marca" (9 páginas, CMO)
**Região:** brasil (PT-BR) · **Domínio previsto:** `content.buzzmonitor.com/encontrar-creators` (guarda-chuva migrado pro CI)

## Modo de entrega: PRÉ-LANÇAMENTO

O briefing descreve uma ferramenta conectada ao Buzz Trends. Esse serviço ainda não existe para a LP consumir, e o próprio briefing define o que fazer nesse caso: mostrar o aviso de lançamento e captar apenas essa intenção, nunca publicar busca simulada como funcional.

Toda a experiência conectada está codada e desligada por uma única flag no topo do `<script>` do `index.html`:

```js
var LP_CONFIG = {
  modo: 'pre-lancamento',   // 'conectado' quando o serviço existir
  endpointBusca: null,      // POST JSON; trava de segurança: modo conectado não liga sem ele
  endpointCaptura: null,    // registra a solicitação no CRM
  urlDemo: 'https://buzzcreators.com.br/?utm_source=lp&utm_content=lp-encontrar-creators'
};
```

O que muda sozinho ao virar `conectado`: o aviso "A busca ainda não está aberta ao público" some, o CTA de envio vira "Consultar creators", e os estados de resultado (carregando, múltiplos perfis, um perfil, nenhum perfil, falha técnica) entram em operação. Nenhum outro ponto do HTML precisa mudar.

### Contrato esperado do serviço de busca

`POST {endpointBusca}` recebe `{marca, tema, site, objetivo, nome, email, vinculo, agencia, optin, origem}` e deve responder:

```json
{
  "consulta_id": "...",
  "marca": "Marca pesquisada",
  "tema": "Tema informado",
  "filtros": ["Instagram", "TikTok"],
  "periodo": "jan a set 2026",
  "perfis": [
    {
      "nome": "", "usuario": "@", "rede": "", "url_perfil": "https://",
      "motivo": "relação observada entre o conteúdo e o tema",
      "evidencia_titulo": "", "evidencia_url": "https://", "evidencia_data": ""
    }
  ]
}
```

`perfis: []` renderiza o estado "nenhum perfil"; 1 item renderiza o card mais o aviso de sugestão única; erro HTTP renderiza o estado de falha técnica. O front nunca completa a lista nem inventa pontuação de afinidade, conforme o briefing.

## Estrutura

1. Hero (§1) — branco, texto à esquerda, mock da interface de busca à direita com o rótulo "Exemplo de interface" (exigido pelo briefing) e sem nenhum dado de creator
2. Decisão (§2) — faixa off-white sem CTA, recorte Challenger pedido pelo briefing. É a seção de pausa da GUIDELINES §2
3. O que a consulta entrega (§3) — grid de 3 cards
4. Como funciona (§4) — 3 passos + CTA
5. Formulário (§5) — aviso de pré-lançamento + 2 etapas (contexto → identificação)
6. Resultado da busca — só existe no modo conectado, 5 estados
7. Orientação de seleção (§6) — texto + 3 perguntas de apoio
8. Conexão com o Buzzcreators (§7) — única seção escura, 3 benefícios + CTA comercial
9. Confiança + FAQ (§8) — assinatura institucional + 6 perguntas
10. Encerramento (§9) — CTA final
11. Footer

## Instrumentação (dataLayer)

Eventos empurrados pro GTM, no recorte honesto de cada modo:

| Evento | Quando |
|---|---|
| `lp_view` | carregamento (carrega o modo ativo) |
| `search_start` | primeira digitação no formulário |
| `prelaunch_notify_submit` | envio válido em pré-lançamento, **só depois** de a captura ser salva |
| `search_submit` | envio válido em modo conectado |
| `search_success` | retorno real com 1 ou mais perfis |
| `search_no_results` | retorno real com 0 perfis |
| `search_error` | falha HTTP ou de rede |
| `creator_profile_click` | clique em "Ver perfil" ou "Ver conteúdo" |
| `demo_requested` | clique em "Quero organizar minha campanha" |

`search_success` nunca dispara sem retorno real e `demo_requested` só em clique efetivo, como o briefing exige. Nenhum evento carrega email, telefone ou conteúdo pessoal.

## Estado

- [x] HTML gerado
- [x] OG image 1200×630 → `assets/og-encontrar-creators.png` (template reproduzível em `og-template-encontrar-creators.html`)
- [x] Revisão (design + web-design-guidelines) — ver `REVISAO.md`
- [ ] Formulário integrado — rodar `/lp-integrar-form buzzcreators/encontrar-creators "<snippet>"`
- [ ] Publicado — entrar no `manifest.json` de `content.buzzmonitor.com` e abrir PR (domínio migrado pro CI)

## Assets referenciados

| Path no source | Origem |
|---|---|
| `../../brand/buzzcreators/assets/logos/logo-icon.png` | brand (favicon) |
| `../../brand/buzzcreators/assets/logos/logo-color.png` | brand (header e bloco de confiança) |
| `../../brand/buzzcreators/assets/logos/logo-branca-2.svg` | brand (footer escuro; `<text>` vivo = 0, não serifa) |
| `./assets/og-encontrar-creators.png` | LP-local (OG image) |

Build do guarda-chuva simulado com `build_umbrella.transform_html`: zero path relativo sobrando, zero placeholder não resolvido, 4/4 assets resolvem.

## Pendências que dependem de outras áreas

**Produto / Tecnologia**
- Endereço do serviço que consulta o Trends, autenticação, cobertura por rede, campos disponíveis, janela de dados e tempo de resposta.
- Amostras reais autorizadas nos 4 cenários (vários perfis, um perfil, nenhum perfil, falha) para homologar antes de ligar o modo conectado.
- Confirmar se existe filtro por região. Enquanto não houver, o campo "Região de interesse" fica fora da LP, porque o briefing proíbe exibir filtro que a fonte não cumpre.

**CRM / Operações**
- Endpoint de captura, mapeamento de campos, deduplicação e identificador da consulta.
- A LP preserva a URL de conversão em `origem`. UTMs precisam continuar sendo lidas no destino, sem sobrescrever Google ou Meta por lead magnet.

**Marketing / Comercial**
- Destino real do "Quero organizar minha campanha". Hoje aponta pro site institucional com `utm_source=lp&utm_content=lp-encontrar-creators`.
- Link da Política de Privacidade: está usando `buzzmonitor.com/politica-de-privacidade/` (do grupo). Confirmar se existe uma do Buzzcreators.
- Captura atual do produto ou vídeo aprovado para a seção escura. Sem material, ela usa composição gráfica neutra.
- Prova social (depoimento, case ou logo) com indicação do produto. Sem material, fica só a assinatura institucional.
- Selo "Descoberta inicial gratuita": não aplicado. Entra quando gratuidade, limite e custo por consulta forem confirmados.

**Tracking**
- `brand/buzzcreators/tracking.json` segue `null` nas 3 regiões. A LP usa `GTM-WFJVK858`, que é o container aprovado para `content.buzzmonitor.com` e o mesmo que a LP irmã `oferta-crescer-marca-influenciadores-setembro-2026` já usa no domínio. O gate de CI aceita (aviso, não bloqueio). Quando o Buzzcreators ganhar container próprio, preencher o `tracking.json` e rodar `/lp-revisar`.
