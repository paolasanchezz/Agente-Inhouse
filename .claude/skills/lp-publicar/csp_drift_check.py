#!/usr/bin/env python3
"""csp_drift_check.py — compara CSP do sibling/vercel.json com o template.

Uso (env vars):
    SIBLING_VERCEL_JSON   caminho do vercel.json do sibling (guarda-chuva)
    TEMPLATE_VERCEL_JSON  caminho do .claude/skills/lp-publicar/vercel.template.json

Exit:
    0  OK — sibling cobre todos os dominios do template (pode ter extras)
    1  DRIFT — template tem dominio que sibling nao tem
    2  ERRO de leitura, parsing ou env var faltando

Stdout (em caso de drift):
    JSON com {status: "DRIFT", missing_in_sibling: {...}, extra_in_sibling: {...}}.
    `missing_in_sibling` agrupa por directive os dominios novos no template
    que o sibling nao tem (drift que precisa de patch).
    `extra_in_sibling` agrupa os dominios do sibling que NAO estao no template
    (customizacoes a preservar quando o operador escolher patch automatico).

Por que existe (motivacao 2026-05-08):
    Apos v3.2.0 atualizar o template para liberar Meta Pixel (Facebook), apenas
    o sibling guarda-chuva redeployado em seguida (cxpress-lp-playbook-whatsapp2026)
    recebeu o patch. Os 3 guarda-chuvas Buzzmonitor continuaram servindo CSP antigo
    por dias — Meta Pixel era bloqueado em runtime mas a skill nao detectava porque
    o `diff` generico do Passo 1.6 era ignoravel (CR/LF + multiplas linhas).
    Esse helper substitui o diff generico por comparacao programatica de conjuntos
    de dominios por directive, com saida acionavel.

Testar isolado:
    SIBLING_VERCEL_JSON=path/to/sibling/vercel.json \\
    TEMPLATE_VERCEL_JSON=.claude/skills/lp-publicar/vercel.template.json \\
    python csp_drift_check.py
"""
import json
import os
import re
import sys


def get_csp(vercel_json_path):
    with open(vercel_json_path, encoding='utf-8') as f:
        d = json.load(f)
    for hdr_block in d.get('headers', []):
        for h in hdr_block.get('headers', []):
            if h.get('key', '').lower() == 'content-security-policy':
                return h.get('value', '')
    return ''


def parse_csp(csp):
    """Retorna dict[directive] -> set(domains)."""
    out = {}
    for chunk in csp.split(';'):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts = chunk.split()
        if not parts:
            continue
        directive = parts[0]
        out[directive] = set(parts[1:])
    return out


def main():
    sibling_path = os.environ.get('SIBLING_VERCEL_JSON', '')
    template_path = os.environ.get('TEMPLATE_VERCEL_JSON', '')

    # Defesa em profundidade: normaliza path estilo MSYS (/c/Users/...) -> Windows (C:/Users/...).
    # O caller (lp-publicar Passo 1.6) ja normaliza via `cygpath -m`, mas se este script for
    # chamado standalone com a forma MSYS, o Python do Windows daria FileNotFoundError (exit 2,
    # abortando o deploy). Idempotente para paths ja Windows-style e no-op em Unix/relativos.
    sibling_path = re.sub(r'^/([a-zA-Z])/', r'\1:/', sibling_path)
    template_path = re.sub(r'^/([a-zA-Z])/', r'\1:/', template_path)

    if not sibling_path or not template_path:
        print(json.dumps({
            "status": "ERROR",
            "message": "SIBLING_VERCEL_JSON e TEMPLATE_VERCEL_JSON sao obrigatorios"
        }), file=sys.stderr)
        sys.exit(2)

    try:
        sibling_csp = get_csp(sibling_path)
        template_csp = get_csp(template_path)
    except FileNotFoundError as e:
        print(json.dumps({"status": "ERROR", "message": f"arquivo nao encontrado: {e}"}), file=sys.stderr)
        sys.exit(2)
    except (json.JSONDecodeError, OSError) as e:
        print(json.dumps({"status": "ERROR", "message": f"falha ao ler/parsear: {e}"}), file=sys.stderr)
        sys.exit(2)

    if not sibling_csp:
        print(json.dumps({"status": "ERROR", "message": "sibling nao tem header Content-Security-Policy"}), file=sys.stderr)
        sys.exit(2)
    if not template_csp:
        print(json.dumps({"status": "ERROR", "message": "template nao tem header Content-Security-Policy"}), file=sys.stderr)
        sys.exit(2)

    sibling_dir = parse_csp(sibling_csp)
    template_dir = parse_csp(template_csp)

    missing_in_sibling = {}
    extra_in_sibling = {}

    for directive, domains in template_dir.items():
        diff = domains - sibling_dir.get(directive, set())
        if diff:
            missing_in_sibling[directive] = sorted(diff)

    for directive, domains in sibling_dir.items():
        diff = domains - template_dir.get(directive, set())
        if diff:
            extra_in_sibling[directive] = sorted(diff)

    if not missing_in_sibling:
        print(json.dumps({"status": "OK"}))
        sys.exit(0)

    print(json.dumps({
        "status": "DRIFT",
        "missing_in_sibling": missing_in_sibling,
        "extra_in_sibling": extra_in_sibling,
    }, indent=2, sort_keys=True))
    sys.exit(1)


if __name__ == "__main__":
    main()
