# LP Cxpress — help-desk-meta

**Espelho de Meta Ads da `help-desk`.** Mesma copy, mesmo layout, mesmos assets.
Criada em 2026-09-30 para a campanha de Help Desk no Meta.

## Por que existe

As LPs do reposicionamento (`help-desk` e irmãs) nasceram com a stack de **Google Ads**:
container `GTM-KN8BPFG` e Jotform `261034073026647`. A conversão personalizada
**Novo Lead (`1068177019134546`)**, que é de onde sai o CPL de todos os relatórios de Meta,
dispara no `/cadastro-realizado` do Jotform de Meta (`261045149477663`).

Apontar Meta para a versão de Google produz o padrão da `whatsapp-business-smb` em agosto:
cliques e visitas registrados, zero lead atribuído. Sem CPL por criativo não há como decidir
verba.

A reunião de 25/09 decidiu usar **a mesma página** para Google e Meta, e a recomendação técnica
era colocar os dois containers na mesma LP. A Marielle optou por duplicar em 30/09, o que mantém
a atribuição de cada canal isolada e não mexe nas páginas de SEO do Bruno.

## O que difere da `help-desk`

| | `help-desk` | `help-desk-meta` |
|---|---|---|
| GTM | `GTM-KN8BPFG` (Google Ads) | `GTM-T4XDWHL3` (Brasil/Meta) |
| Jotform | `261034073026647` | `261045149477663` |
| `robots` | `index, follow` | **`noindex, follow`** |
| `canonical` | ela mesma | aponta para **`/help-desk`** |
| `og:url` e JSON-LD | `/help-desk` | `/help-desk-meta` |
| Como o form renderiza | `assets/form-cxpress.js` (source do Jotform de Google hospedado em `srcdoc`) | `jsform` padrão do Jotform de Meta |

**O texto visível é byte a byte igual ao da original** (verificado na criação). A única diferença
de mecânica é a última linha da tabela, e ela era inevitável: o `form-cxpress.js` da versão de
busca embute o HTML do formulário **261034073026647** dentro do próprio arquivo, em `srcdoc`. Trocar
só o `data-jotform` não trocaria o formulário renderizado, apenas o da contingência, e a página
passaria a dizer um ID e servir outro. Aqui o carregador sob demanda foi apontado para o `jsform`
do formulário de Meta, que é o mesmo mecanismo da `banimento-whatsapp` e da `atendimento-digital`.
O `form-cxpress.js` foi removido desta pasta.

Consequência prática: o formulário desta página tem os **campos do formulário de Meta** (que inclui
faixa de investimento e tamanho do time) e o visual padrão do Jotform, não o visual customizado que
o Bruno aprovou para a versão de busca. Os dois formulários sempre tiveram campos diferentes, então
não havia como manter os dois idênticos.

O `noindex` e o `canonical` cruzado existem para a página de Meta não competir no Google com a de
SEO. Duas páginas com a mesma copy disputando a mesma busca cancelariam o trabalho que a `help-desk`
existe para fazer.

## ⚠️ Regra de sincronia

Esta página é cópia. **Toda alteração de copy ou layout feita na `help-desk` precisa ser repetida
aqui**, e o contrário também. Se as duas divergirem sem querer, o teste de canal deixa de comparar
canal e passa a comparar página.

Para conferir se dessincronizou, comparar o texto visível das duas. Diferença esperada: zero.

## Estado

- [x] Espelho criado e tracking trocado
- [x] No manifesto de `content.cxpress.io`
- [ ] Campanha Meta no ar (roteiros e legendas em `conhecimento/copywriting/criacao/cxpress/2026-09-30/campanha-help-desk-meta.md`)

## Pendência aberta

O formulário fica na última seção, como na original. Para tráfego de Meta isso é o padrão que
mediu pior nesta conta: a `tempo-de-resposta` convertia 3,2% com o form a 7,9 telas de scroll no
celular, contra 20,0% da `banimento-whatsapp` com o form a 1,9 tela e o mesmo Jotform. Subir o
form aqui é uma decisão em aberto, e seria a primeira divergência consciente em relação à versão
de busca.
