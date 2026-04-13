# Meta Ads — Setup do colaborador

Guia para configurar o modulo `meta-ads/` na sua maquina. Cada pessoa do time precisa fazer isso uma vez.

> **Prefere conduzido?** Rode `/setup-agencia` no Claude Code — ele faz pergunta a pergunta e valida cada passo.

---

## Pre-requisitos

- **Python 3.10+** instalado
- **Acesso ao Business Manager do Grupo Elife** com permissao `ads_read` nas 6 contas (peca ao admin para te adicionar como Funcionario)
- Repositorio clonado e voce esta na pasta raiz

---

## Passo 1 — Gerar seu token Meta (individual)

> Cada pessoa tem o proprio token. Nao compartilhamos um unico por seguranca / auditoria.

1. Acesse https://business.facebook.com → entre com sua conta.
2. Clique no seu perfil (canto inferior esquerdo) → **Configuracoes de negocios**.
3. No menu lateral: **Usuarios → Tokens de acesso → Gerar token**.
4. Selecione a App do Grupo Elife (peca ao admin se nao souber qual).
5. **Permissoes:** marque **APENAS `ads_read`**. Nao marque nada de escrita.
6. Clique em **Gerar token** e copie o texto longo que aparece (comeca com `EAA...`).
7. Anote a data de hoje no formato `YYYY-MM-DD` (ex.: `2026-04-13`).

> O token expira em ~60 dias. O sistema avisa 10 dias antes — anote na agenda para renovar.

---

## Passo 2 — Criar e preencher o `.env`

```bash
cd meta-ads
cp .env.example .env       # Windows: copy .env.example .env
```

Abra `meta-ads/.env` no editor de texto e preencha **2 linhas**:

```
META_ACCESS_TOKEN=EAA...                  # cole o token do Passo 1
META_TOKEN_CREATED_AT=2026-04-13          # data de hoje
```

> **IDs das 6 contas ja vem no codigo** (`scripts/cache_manager.py`). Voce nao precisa configurar nada alem de token + data.

---

## Passo 3 — Instalar dependencias Python

```bash
cd meta-ads
python -m pip install -r requirements.txt    # Mac/Linux: python3
```

---

## Passo 4 — Validar setup

```bash
cd meta-ads
python scripts/check_setup.py
```

Saida esperada:
```
[OK] META_ACCESS_TOKEN presente (XXX caracteres).
[OK] META_TOKEN_CREATED_AT = 2026-04-13
[OK] Token dentro da validade.
[OK] buzzmonitor_brl   Buzzmonitor Brasil (BRL) (ativa)
... (mais 5 contas)
[OK] Tudo configurado! Voce esta pronto para usar /meta-ads e /anuncios.
```

Se aparecer `[ERRO]` em alguma linha, veja **Troubleshooting** abaixo.

---

## Renovacao do token (a cada ~60 dias)

Quando voce rodar `/meta-ads` e ver:
```
[AVISO] ATENCAO: Token Meta Ads expira em N dia(s) (YYYY-MM-DD). Renove em breve.
```

Repita o **Passo 1** (gerar novo token), depois atualize **as duas linhas** no `meta-ads/.env`:
- `META_ACCESS_TOKEN=` (novo token)
- `META_TOKEN_CREATED_AT=` (data de hoje)

Rode `python scripts/check_setup.py` para confirmar.

---

## Troubleshooting

**`META_ACCESS_TOKEN nao definido`**
Voce nao copiou o `.env.example` para `.env` ou nao salvou. Repita o Passo 2.

**`Token invalido ou expirado` (erro #190 da Meta)**
Causas comuns:
1. Voce copiou apenas parte do token (eles sao longos — 200+ caracteres)
2. O token foi revogado ou expirou
3. Voce gerou na conta Facebook errada

Solucao: gere um novo token (Passo 1) e cole no `.env`.

**`sem permissao` (erro #100)**
O admin nao te deu acesso `ads_read` em alguma das 6 contas. Peca para te adicionar com essa permissao em todas. Voce pode usar as contas que **estao** acessiveis enquanto isso.

**`facebook-business nao instalado`**
Pule o Passo 3. Se ja rodou e mesmo assim falha, tente:
```bash
python -m pip install --user -r requirements.txt
```

**`pip install` falha com erro de rede**
Causas: sem internet, firewall corporativo, ou Python instalado em local protegido. Tente o `--user` acima ou peca ao admin.
