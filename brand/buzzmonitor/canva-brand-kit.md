# Brand Kit do Canva — Buzzmonitor

> Configuração passo a passo do **Brand Kit** da Buzzmonitor no Canva, baseado em `brand/buzzmonitor/tokens.json` (fonte da verdade) e nos logos em `brand/buzzmonitor/assets/logos/`.
> Quando concluir esse setup, partir pro [canva-brand-templates.md](canva-brand-templates.md) (os 3 templates).

## Como criar/editar Brand Kit no Canva

1. Acessa **canva.com** logada como admin da equipe Buzzmonitor
2. Menu lateral esquerda → **"Brand"** (ícone de paleta) → **"Brand Kit"**
3. Se já existe brand kit sem nome (vi 2 brand kits na sua conta): renomear pra **"Buzzmonitor"** e configurar.
4. Se preferir do zero: **"Create new brand kit"** → nomeia "Buzzmonitor"

Configura cada seção na ordem abaixo.

---

## 1. Logos (faz upload de 3 arquivos)

Sobe esses 3 arquivos como logos do brand kit. Os PNG estão em `brand/buzzmonitor/assets/logos/`:

| Nome no Canva | Arquivo do repo | Quando usar |
|---|---|---|
| **Buzzmonitor — Primary** | `logo-primary.svg` (ou .png) | Logo padrão (uso em fundos claros) |
| **Buzzmonitor — Reversed** | `logo-reversed.svg` (ou .png) | Logo branco/claro (uso em fundos escuros) |
| **Buzzmonitor — Icon** | `logo-icon.svg` (ou .png) | Só o ícone (favicons, marca d'água, espaços pequenos) |

**Dica**: o SVG vetoriza perfeito em qualquer tamanho. Se o Canva não aceitar SVG no upload de logo, sobe o PNG.

---

## 2. Cores (10 cores + neutros)

No Canva, vai em **Brand Kit → Brand Colors → Add color** e cria os grupos abaixo. **Cola o hex exato** que está aqui.

### Cores principais

| Nome | Hex | Uso |
|---|---|---|
| **Roxo Buzzmonitor** | `#390155` | Cor principal — fundos escuros, destaques |
| **Lilás claro** | `#F2D8FF` | Variante suave do roxo — fundos e hovers |
| **Laranja vibrante** | `#EB7C2E` | CTAs, acentos, elementos de destaque |
| **Pêssego claro** | `#FFD5C3` | Variante suave do laranja |

### Cores complementares

| Nome | Hex | Uso |
|---|---|---|
| **Teal** | `#0E9D9B` | Elementos complementares, ícones, badges |
| **Ciano claro** | `#CDFDFC` | Variante suave do teal |
| **Amarelo dourado** | `#FCBD4F` | Alertas positivos, destaques secundários |
| **Amarelo claro** | `#FFE1AD` | Variante suave |
| **Rosa/magenta** | `#DE2451` | Alertas, CTAs alternativos |
| **Rosa claro** | `#FFD7E0` | Variante suave |

### Neutros

| Nome | Hex | Uso |
|---|---|---|
| **Preto suave** | `#1A1A1A` | Texto principal |
| **Cinza escuro** | `#4A4A4A` | Texto secundário |
| **Cinza claro** | `#D1D1D1` | Bordas, divisores |
| **Fundo claro** | `#F5F5F5` | Fundo de seção clara |
| **Branco** | `#FFFFFF` | Fundo branco |

### Gradientes (criar como "background" no design)

Canva não tem campo de gradientes no brand kit. Documenta esses 4 como **decisões de design** pra reuso nos templates:

| Nome | Composição |
|---|---|
| **Roxo → Laranja** | `linear-gradient(135deg, #390155 → #EB7C2E)` — gradiente principal da marca |
| **Amarelo → Teal** | `linear-gradient(135deg, #FCBD4F → #0E9D9B)` — fundo vibrante |
| **Rosa → Laranja** | `linear-gradient(135deg, #DE2451 → #EB7C2E)` — CTAs quentes |
| **Teal → Roxo** | `linear-gradient(135deg, #0E9D9B → #390155)` — fundo frio |

---

## 3. Fontes (3 famílias)

No Canva, vai em **Brand Kit → Brand Fonts → Add font** e configura os 3 papéis.

| Papel no Canva | Fonte | Peso | Uso |
|---|---|---|---|
| **Heading font** | League Spartan | Bold (700) ou Black (900) | Títulos, manchetes, frases impactantes |
| **Subheading font** | HK Grotesk | Light (300) | Subtítulos, segunda linha de hierarquia |
| **Body font** | Lato | Regular (400) | Texto corrido, legendas, descrições |

### Notas sobre as fontes

- **League Spartan**: já está disponível na biblioteca padrão do Canva. É só selecionar.
- **HK Grotesk**: **não está na biblioteca do Canva**. Você precisa fazer upload (precisa de Canva Pro/Teams pra subir fonte custom).
  - Se não tiver acesso, **alternativa**: usa **Inter** (peso 300) — visualmente muito próxima do HK Grotesk Light. Free no Canva.
- **Lato**: já está disponível na biblioteca padrão do Canva.

### Como subir HK Grotesk (se for Canva Teams)

1. Brand Kit → Brand Fonts → **Upload font**
2. Sobe os arquivos `.ttf` ou `.otf` (você precisa ter os arquivos da fonte — se não tiver, [HK Grotesk é gratuita aqui](https://hanken.co/products/hk-grotesk))
3. Configura como "Subheading font"

---

## 4. Tom de voz (opcional mas útil)

Canva tem campo "Tone of voice" no brand kit. Cola isso:

> **Personalidade**: analítica · inovadora · confiável · acessível · vibrante
>
> **Não somos**: hypezeira, vendedora de promessa, agressiva, "disruptiva", "revolucionária"
>
> **Voz**: direta, conversacional, brasileira natural. "A Buzzmonitor" (feminino). Frases curtas. Dado quente abre, contexto humano fecha. Confiante na IA sem se vender como mágica.

---

## 5. Validação final

Quando terminar, confirma que aparece tudo:

- [ ] 3 logos (Primary, Reversed, Icon)
- [ ] 14 cores nomeadas com hex correto
- [ ] 3 fontes configuradas com papel certo (Heading, Subheading, Body)
- [ ] Tom de voz preenchido (opcional)

Se sim, partir pra criar os 3 brand templates conforme [canva-brand-templates.md](canva-brand-templates.md).

---

## Em paralelo: ainda preciso saber

Pra a `/social-canva` funcionar, a conta Canva precisa ser **Pro ou Teams** — Brand Templates é recurso pago. Conferir antes de criar os templates.

Se for free, dá pra:
- Criar o brand kit (esse doc aqui) — funciona no free também
- **Mas os 3 templates não viram "Brand Templates"** — viram só designs salvos. Skill `/social-canva` não conseguiria autofill.

Nesse cenário (free), o `/social-canva` viraria modo "geração de prompt" — gera um documento de instruções e você preenche manualmente. Funciona, é mais trabalho.
