#!/usr/bin/env python3
"""notificar_falha.py — e-mail quando a atualizacao noturna das dashboards falha.

Silencioso no verde: so o workflow chama isto, e so em falha. O e-mail diz em que etapa parou,
traz o fim do log daquela etapa (o validar_contrato.py ja escreve o que consertar, inclusive o
provavel rename) e o comando para destravar quando for catraca.

O log vai bruto para o e-mail — sem a mascara de secrets que o GitHub aplica na tela do run.
Por isso todo valor de secret conhecido e apagado do texto antes de enviar.

Env:
    RESEND_API_KEY          sem ela, imprime o e-mail e sai 0 (nao derruba o job por causa do aviso)
    EMAIL_TO / EMAIL_FROM   destinatario / remetente
    RUN_URL                 link do run no GitHub
    LOG_DIR                 diretorio com etapa.txt (etapa que falhou) e log-<etapa>.txt
Uso: py dashboards-umbrella/notificar_falha.py [--dry-run]
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

SECRETS = ("SUPABASE_PG_URL", "DASHBOARD_BASIC_AUTH_PASS", "DASHBOARD_BASIC_AUTH_USER",
           "VERCEL_TOKEN", "RESEND_API_KEY")
LINHAS_LOG = 40

O_QUE_FAZER = {
    "conectividade": "O runner nao alcancou o Supabase (pooler fora, credencial revogada ou "
                     "permissao do looker_readonly mudou). Nada foi exportado; o painel segue "
                     "com os dados de ontem.",
    "filtro": "O filtro CM do buzz-br divergiu entre dashboard/queries.py (oficial) e "
              "dashboard-pessoal/lib/queries.py (o espelho que o exportador usa). Nada foi "
              "exportado. Replique a mudanca no espelho; o log lista o que difere.",
    "exportar": "Um exportador quebrou (query, statement_timeout, coluna renomeada no banco). "
                "Nada foi para o ar.",
    "validar": "O validador barrou os dados — nada foi para o ar, o painel segue com os de "
               "ontem. exit 2 = contrato (campo que o painel le sumiu/mudou; a mensagem aponta "
               "o provavel rename) · exit 4 = schema_version divergente · exit 3 = catraca "
               "(contagem caiu ou explodiu contra producao). Se for catraca e a queda for "
               "legitima, rode o workflow a mao com aceitar_catraca=<slug> e um motivo.",
    "deploy": "Build, deploy ou smoke falharam. Se o deploy chegou a subir e o smoke reprovou, "
              "o rollback ja devolveu a versao anterior — veja a ultima linha do log.",
}


def limpar(texto: str) -> str:
    for nome in SECRETS:
        v = os.environ.get(nome)
        if v and len(v) >= 4:
            texto = texto.replace(v, f"***{nome}***")
    # Senha embutida em qualquer URL de conexao que tenha escapado.
    return re.sub(r"(postgres(?:ql)?://[^:/\s]+:)[^@\s]+@", r"\1***@", texto)


def montar() -> tuple[str, str]:
    log_dir = Path(os.environ.get("LOG_DIR", "."))
    etapa = (log_dir / "etapa.txt").read_text(encoding="utf-8").strip() \
        if (log_dir / "etapa.txt").exists() else "desconhecida"
    arq = log_dir / f"log-{etapa}.txt"
    cauda = "\n".join(arq.read_text(encoding="utf-8", errors="replace").splitlines()[-LINHAS_LOG:]) \
        if arq.exists() else "(sem log capturado para esta etapa)"
    corpo = (
        f"A atualizacao noturna das dashboards CM falhou na etapa: {etapa}.\n\n"
        f"{O_QUE_FAZER.get(etapa, '')}\n\n"
        f"Run: {os.environ.get('RUN_URL', '(sem link)')}\n\n"
        f"--- ultimas {LINHAS_LOG} linhas do log de '{etapa}' ---\n{cauda}\n"
    )
    return f"[dashboards] atualizacao noturna falhou em: {etapa}", limpar(corpo)


def enviar(api_key: str, de: str, para: str, assunto: str, texto: str) -> tuple[bool, str]:
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps({"from": de, "to": [para], "subject": assunto, "text": texto}).encode(),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json",
                 # Resend fica atras de Cloudflare, que bloqueia 'Python-urllib/x' (erro 1010).
                 "User-Agent": "dashboards-noturno/1.0", "Accept": "application/json"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return True, json.loads(r.read() or b"{}").get("id", "")
    except Exception as e:
        return False, str(e)


def main() -> int:
    assunto, texto = montar()
    chave = os.environ.get("RESEND_API_KEY")
    if "--dry-run" in sys.argv or not chave:
        if not chave:
            print("aviso: RESEND_API_KEY ausente — e-mail nao enviado, so impresso", file=sys.stderr)
        print(f"Assunto: {assunto}\n\n{texto}")
        return 0
    ok, info = enviar(chave, os.environ.get("EMAIL_FROM", "Dashboards CM <onboarding@resend.dev>"),
                      os.environ.get("EMAIL_TO", "victor.lopes@buzzmonitor.com.br"), assunto, texto)
    print(f"e-mail {'enviado' if ok else 'FALHOU'}: {info}")
    return 0  # falha do aviso nao muda o resultado do run, que ja e vermelho


if __name__ == "__main__":
    sys.exit(main())
