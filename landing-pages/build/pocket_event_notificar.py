"""pocket_event_notificar.py — manda por e-mail o resumo de uma rodada do
automatismo de Pocket Events.

Le o relatorio do pocket_event_job.py no stdin e envia UM e-mail com o que foi
criado, o que foi recusado (com os motivos, pra quem preencheu poder corrigir) e
o que ja existia. Silencioso quando a rodada nao fez nada: varredura diaria sem
solicitacao nova nao gera e-mail.

Mesma mecanica do notify.py do lp-health-check (Resend via HTTP, stdlib).

Variaveis de ambiente:
  RESEND_API_KEY            — obrigatoria pra enviar de fato
  POCKET_EMAIL_TO           — destinatario (default: victor.lopes@buzzmonitor.com.br)
  POCKET_EMAIL_FROM         — remetente (default: sandbox do Resend)
  POCKET_EMAIL_COPIA_SOLICITANTE — "1" inclui os solicitantes em copia. So
      funciona com dominio proprio verificado no Resend: o remetente sandbox
      (onboarding@resend.dev) so entrega pro dono da conta.

Uso:
    py pocket_event_job.py lote.json | py pocket_event_notificar.py [--dry-run]

Exit 0 = enviou ou nao havia o que enviar; 1 = falhou o envio.
"""
import json
import os
import sys
import urllib.error
import urllib.request

PADRAO_TO = "victor.lopes@buzzmonitor.com.br"
PADRAO_FROM = "Pocket Events <onboarding@resend.dev>"


def assunto(rel):
    n_ok, n_nao = len(rel["criadas"]), len(rel["recusadas"])
    if n_nao and n_ok:
        return "Pocket Events: %d LP(s) criada(s), %d solicitacao(oes) recusada(s)" % (n_ok, n_nao)
    if n_nao:
        return "Pocket Events: %d solicitacao(oes) recusada(s)" % n_nao
    return "Pocket Events: %d LP(s) criada(s)" % n_ok


def corpo(rel):
    linhas = []
    if rel["criadas"]:
        linhas.append("CRIADAS (entram no ar assim que o deploy do CI terminar)")
        for c in rel["criadas"]:
            linhas.append("  - %s" % c["titulo"])
            linhas.append("    %s" % c["url"])
            if c.get("solicitante"):
                linhas.append("    pedido por: %s (linha %s)" % (c["solicitante"], c.get("linha")))
        linhas.append("")

    if rel["recusadas"]:
        linhas.append("RECUSADAS (nada foi publicado; corrigir a linha e reenviar)")
        for r in rel["recusadas"]:
            linhas.append("  - linha %s | %s | %s"
                          % (r.get("linha"), r.get("solicitante", "?"), r.get("titulo", "")))
            for m in r["motivos"]:
                linhas.append("      %s" % m)
        linhas.append("")

    if rel["ignoradas"]:
        linhas.append("JA EXISTIAM (nada mudou)")
        for i in rel["ignoradas"]:
            linhas.append("  - %s (linha %s)" % (i["slug"], i.get("linha")))
        linhas.append("")

    linhas.append("Automatismo: .github/workflows/pocket-event-novo.yml")
    linhas.append("Regras e limites: landing-pages/build/templates/pocket-event/config.json")
    return "\n".join(linhas)


def destinatarios(rel):
    to = [os.environ.get("POCKET_EMAIL_TO") or PADRAO_TO]
    if os.environ.get("POCKET_EMAIL_COPIA_SOLICITANTE") == "1":
        for grupo in (rel["criadas"], rel["recusadas"]):
            for item in grupo:
                email = (item.get("solicitante") or "").strip()
                if email and "@" in email and email not in to:
                    to.append(email)
    return to


def enviar(api_key, de, para, titulo, texto):
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps({"from": de, "to": para, "subject": titulo,
                         "text": texto}).encode("utf-8"),
        headers={"Authorization": "Bearer %s" % api_key,
                 "Content-Type": "application/json",
                 # Resend fica atras de Cloudflare, que bloqueia o UA padrao do
                 # urllib ("Python-urllib/3.x") com 403 code 1010. Mesmo ajuste ja
                 # feito no notify.py do lp-health-check.
                 "User-Agent": "pocket-event/1.0",
                 "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return True, json.load(r).get("id", "")
    except urllib.error.HTTPError as e:
        return False, "HTTP %s: %s" % (e.code, e.read().decode("utf-8", "replace")[:400])
    except Exception as e:  # rede, DNS, timeout
        return False, str(e)


def main():
    rel = json.load(sys.stdin)
    if not (rel.get("criadas") or rel.get("recusadas")):
        print("nada a notificar (nenhuma criacao nem recusa nesta rodada)")
        return 0

    titulo, texto = assunto(rel), corpo(rel)
    para = destinatarios(rel)

    if "--dry-run" in sys.argv:
        print("PARA: %s\nASSUNTO: %s\n\n%s" % (", ".join(para), titulo, texto))
        return 0

    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        sys.stderr.write("RESEND_API_KEY ausente - resumo abaixo, sem envio:\n\n%s\n" % texto)
        return 0

    de = os.environ.get("POCKET_EMAIL_FROM") or PADRAO_FROM
    ok, info = enviar(api_key, de, para, titulo, texto)
    print(("enviado (%s)" if ok else "FALHOU: %s") % info)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
