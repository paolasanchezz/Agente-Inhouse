"""Confere a conexao do Claude com o Supabase (SUPABASE_PG_URL) sem mostrar a senha.

Usado pelo Passo 5 do /setup-agencia. O servidor `supabase` do `.mcp.json` le a
URL do banco da variavel SUPABASE_PG_URL do ambiente do Claude (nao do
dashboard/.env). Este script le de onde o setup grava: no Windows, das variaveis
de usuario (registro); no Mac/Linux, do `env` de ~/.claude/settings.json (o app
do Mac ignora variaveis exportadas no ~/.zshrc). Os dois valem sem reiniciar o
terminal. Por ultimo, o ambiente do proprio processo.

Uso (rodar da raiz do repo):
    uv run --no-project --python 3.12 --with "psycopg[binary]" python .claude/skills/setup-agencia/checar_supabase.py
    uv run --no-project --python 3.12 --with "psycopg[binary]" python .claude/skills/setup-agencia/checar_supabase.py --gravar-env

--gravar-env: depois de conectar, grava a mesma URL em dashboard/.env (cria a
linha se faltar, troca se for diferente). Usado por /auditar-deals-cm e /seo-report.

Saida, pro agente interpretar (nunca contem a senha):
    [OK] ...                 conexao feita
    ERRO=<codigo>            ver a tabela no SKILL.md (Passo 5.4)
    ENV_ARQUIVO=<estado>     ausente | igual | diferente | gravado
Exit 0 = conectou; 1 = falhou.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

POOLER_HOST = "aws-1-sa-east-1.pooler.supabase.com"
SUFIXO_PROJETO = ".vymnlivcgokmyonqlkah"
ENV_PATH = Path(__file__).resolve().parents[3] / "dashboard" / ".env"


def ler_variavel() -> str | None:
    if sys.platform == "win32":
        import winreg

        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as chave:
                return winreg.QueryValueEx(chave, "SUPABASE_PG_URL")[0].strip()
        except OSError:
            pass
    try:
        settings = json.loads((Path.home() / ".claude" / "settings.json").read_text(encoding="utf-8"))
        valor = (settings.get("env") or {}).get("SUPABASE_PG_URL")
    except (OSError, ValueError, AttributeError):
        valor = None
    if valor:
        return valor.strip()
    valor = os.environ.get("SUPABASE_PG_URL", "").strip()
    return valor or None


def erro(codigo: str, detalhe: str = "") -> None:
    print(f"ERRO={codigo}" + (f" ({detalhe})" if detalhe else ""))
    sys.exit(1)


def checar_formato(url: str) -> None:
    if "#" in url:
        erro("CARACTERE_CRU", "a senha tem # sem codificar; a URL e cortada nesse ponto")
    try:
        partes = urlsplit(url)
        porta = partes.port
    except ValueError:
        erro("FORMATO_INVALIDO")
    if partes.scheme not in ("postgresql", "postgres") or not partes.hostname:
        erro("FORMATO_INVALIDO")
    if partes.hostname.startswith("db.") and partes.hostname.endswith(".supabase.co"):
        erro("HOST_DIRETO")
    if partes.hostname != POOLER_HOST or porta != 5432:
        erro("HOST_DESCONHECIDO", f"{partes.hostname}:{porta}")
    if not (partes.username or "").endswith(SUFIXO_PROJETO):
        erro("USUARIO_SEM_SUFIXO", partes.username or "vazio")
    if not partes.password:
        erro("SENHA_VAZIA")


def ocultar(msg: str, url: str) -> str:
    senha = urlsplit(url).password or ""
    for segredo in (url, senha, unquote(senha)):
        if segredo:
            msg = msg.replace(segredo, "***")
    return msg.strip().splitlines()[0] if msg.strip() else ""


def conectar(url: str) -> None:
    import psycopg

    try:
        with psycopg.connect(url, connect_timeout=15, autocommit=True) as conn:
            usuario = conn.execute("select current_user").fetchone()[0]
            n_deals = conn.execute(
                "select count(*) from information_schema.tables"
                " where position('deal' in table_name) > 0"
            ).fetchone()[0]
    except psycopg.Error as e:
        msg = str(e)
        if "password authentication failed" in msg:
            erro("SENHA_ERRADA")
        if "Tenant or user not found" in msg:
            erro("USUARIO_ERRADO")
        if any(t in msg for t in ("translate host name", "getaddrinfo", "timeout expired",
                                  "Connection refused", "Network is unreachable")):
            erro("REDE", ocultar(msg, url))
        erro("OUTRO", ocultar(msg, url))
    print(f"[OK] Conectado no Supabase como {usuario} (so leitura). Tabelas de deals visiveis: {n_deals}")


def estado_env(url: str) -> str:
    if not ENV_PATH.exists():
        return "ausente"
    for raw in ENV_PATH.read_text(encoding="utf-8").splitlines():
        linha = raw.strip()
        if linha.startswith("SUPABASE_PG_URL="):
            atual = linha.split("=", 1)[1].strip().strip('"').strip("'")
            return "igual" if atual == url else "diferente"
    return "ausente"


def gravar_env(url: str) -> None:
    linhas = ENV_PATH.read_text(encoding="utf-8").splitlines() if ENV_PATH.exists() else []
    nova = f"SUPABASE_PG_URL={url}"
    trocou = False
    for i, raw in enumerate(linhas):
        if raw.strip().startswith("SUPABASE_PG_URL="):
            linhas[i] = nova
            trocou = True
    if not trocou:
        linhas.append(nova)
    ENV_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENV_PATH.write_text("\n".join(linhas) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gravar-env", action="store_true",
                        help="grava a URL em dashboard/.env depois de conectar")
    args = parser.parse_args()

    url = ler_variavel()
    if not url:
        erro("VAR_AUSENTE")
    checar_formato(url)
    conectar(url)

    estado = estado_env(url)
    if args.gravar_env and estado != "igual":
        gravar_env(url)
        estado = "gravado"
    print(f"ENV_ARQUIVO={estado}")


if __name__ == "__main__":
    main()
