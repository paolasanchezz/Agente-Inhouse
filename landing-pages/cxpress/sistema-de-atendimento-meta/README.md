# LP Cxpress — sistema-de-atendimento-meta

**Espelho de Meta Ads da `sistema-de-atendimento`.** Mesma copy, mesmo layout, mesmos assets.
Criada em 2026-09-30 para a campanha de Sistema de Atendimento ao Cliente no Meta.

## Por que existe

As LPs do reposicionamento (`sistema-de-atendimento` e irmãs) nasceram com a stack de **Google Ads**:
container `GTM-KN8BPFG` e Jotform `261034073026647`. A conversão personalizada
**Novo Lead (`1068177019134546`)**, que é de onde sai o CPL de todos os relatórios de Meta,
dispara no `/cadastro-realizado` do Jotform de Meta (`261045149477663`).

Apontar Meta para a versão de Google produz o padrão da `whatsapp-business-smb` em agosto:
cliques e visitas registrados, zero lead atribuído. Sem CPL por criativo não há como decidir
verba.

A reunião de 25/09 decidiu usar **a mesma página** para Google e Meta, e a recomendação técnica
era colocar os dois containers na mesma LP. A Marielle optou por duplicar em 30/09, o que mantém
a atribuição de cada canal isolada e não mexe nas páginas de SEO do Bruno.

## O que difere da `sistema-de-atendimento`

| | `sistema-de-atendimento` | `sistema-de-atendimento-meta` |
|---|---|---|
| GTM | `GTM-KN8BPFG` (Google Ads) | `GTM-T4XDWHL3` (Brasil/Meta) |
| Jotform | `261034073026647` | `261045149477663` |
| `robots` | `index, follow` | **`noindex, follow`** |
| `canonical` | ela mesma | aponta para **`/sistema-de-atendimento`** |
| `og:url` e JSON-LD | `/sistema-de-atendimento` | `/sistema-de-atendimento-meta` |
| Como o form renderiza | `assets/form-cxpress.js` (source do Jotform de Google hospedado em `srcdoc`) | `jsform` padrão do Jotform de Meta |
| Posição do formulário | última seção | **logo após a esteira de clientes** |

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
SEO. Duas páginas com a mesma copy disputando a mesma busca cancelariam o trabalho que a `sistema-de-atendimento`
existe para fazer.

## ⚠️ Regra de sincronia

Esta página é cópia. **Toda alteração de copy ou layout feita na `sistema-de-atendimento` precisa ser repetida
aqui**, e o contrário também. Se as duas divergirem sem querer, o teste de canal deixa de comparar
canal e passa a comparar página.

Para conferir se dessincronizou, comparar o texto visível das duas. Diferença esperada: zero.

## Estado

- [x] Espelho criado e tracking trocado
- [x] No manifesto de `content.cxpress.io`
- [ ] Campanha Meta no ar (roteiros e legendas em `conhecimento/copywriting/criacao/cxpress/2026-09-30/campanha-help-desk-meta.md`)

## Formulário no topo (aplicado em 30/09)

O bloco `.cta#contato` saiu da última seção e entrou logo depois da esteira de clientes. Todo o
argumento continua abaixo dele, que é o padrão da `banimento-whatsapp`.

Motivo: nesta conta, form fundo de página mediu 3,2% de conversão (`tempo-de-resposta`, form a 7,9
telas de scroll no celular) contra 20,0% (`banimento-whatsapp`, form a 1,9 tela), com o mesmo
Jotform e os mesmos campos. A GUIDELINES §10 manda form na 4ª ou última seção para BoFu, como
filtro de intenção; o dado desta conta aponta o contrário para tráfego de Meta. Desvio consciente,
e só no espelho: a versão de busca não foi tocada.

**Nenhum texto mudou.** A seção foi movida inteira, com o H2 e a lead que já tinha.

Efeito colateral: a página agora termina no FAQ, sem seção de fechamento. Os 3 a 5 CTAs internos
continuam apontando para `#contato` (agora rolando para cima) e o botão flutuante de WhatsApp
segue fixo na tela. Criar um fechamento novo exigiria escrever copy que não existe no original,
o que quebraria a paridade entre as duas versões.
