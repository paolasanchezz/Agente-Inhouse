"""pocket_event_job.py — aplica no repo as solicitacoes de Pocket Event.

Recebe uma LISTA de solicitacoes (ja coletadas pelo workflow, seja do payload do
repository_dispatch ou da varredura da planilha) e, pra cada uma que passar na
validacao, cria `landing-pages/buzzmonitor/{slug}/` e inscreve o slug no
manifesto do guarda-chuva. Nada alem disso: quem abre PR, mergeia e deploya e o
CI que ja existe (lp-pr.yml -> lp-deploy.yml).

O que este script NUNCA faz, por desenho:
  - editar ou remover LP que ja existe (sobrescrever exigiria decisao humana);
  - tocar em qualquer manifesto que nao seja o configurado em config.json;
  - publicar mais que `limites.lps_por_execucao` de uma vez (planilha com defeito
    nao vira uma enxurrada de deploys);
  - deixar uma solicitacao ruim passar em silencio: ela entra em `recusadas`,
    com os motivos, e o workflow avisa o solicitante.

USO
---
    py pocket_event_job.py <solicitacoes.json> [--repo DIR] [--dry-run]

`solicitacoes.json` e uma lista de objetos (ou um objeto unico). Campos:
titulo, nicho, modulo, data, horario, speaker; opcionais: solicitante, linha.

Imprime em stdout o relatorio JSON {criadas, recusadas, ignoradas, ...}.
Exit 0 = rodou (o veredito esta no relatorio); 2 = erro de uso/interno.
"""
import argparse
import io
import json
import os
import sys

import render_pocket_event as rpe

AQUI = os.path.dirname(os.path.abspath(__file__))


def carregar_manifesto(repo, config):
    caminho = os.path.join(repo, config["manifesto"])
    return caminho, json.load(io.open(caminho, encoding="utf-8"))


def salvar_manifesto(caminho, manifesto):
    io.open(caminho, "w", encoding="utf-8", newline="\n").write(
        json.dumps(manifesto, ensure_ascii=False, indent=2) + "\n")


def ja_existe(repo, config, existentes, slug):
    destino = os.path.join(repo, config["destino_source"].replace("/", os.sep), slug)
    return slug in existentes or os.path.isdir(destino)


def publicada_antes(repo, config, pedido):
    """Slug de uma LP ja gerada com a MESMA data e o MESMO titulo, ou None.

    Rede de seguranca pro caso em que o slug nao da mais pra recalcular: o nicho
    da linha saiu da lista (a lista da diretoria trocou em 2026-09-14, e a LP
    pocket-alimentos-2026-09-22 foi gerada com um nicho que nao existe mais).
    Titulo + data identificam a edicao; o titulo sai do README gerado pelo
    proprio renderer, nunca de arquivo editado a mao.
    """
    data = str(pedido.get("data", "")).strip()[:10]
    titulo = " ".join(str(pedido.get("titulo", "")).split())
    if len(data) != 10 or not titulo:
        return None
    base = os.path.join(repo, config["destino_source"].replace("/", os.sep))
    if not os.path.isdir(base):
        return None
    alvo = "| Titulo | %s |" % titulo
    for nome in sorted(os.listdir(base)):
        if not (nome.startswith("pocket-") and nome.endswith("-" + data)):
            continue
        readme = os.path.join(base, nome, "README.md")
        if not os.path.isfile(readme):
            continue
        linhas = io.open(readme, encoding="utf-8").read().splitlines()
        if any(l.strip() == alvo for l in linhas):
            return nome
    return None


def ignorada(config, slug, linha):
    return {"slug": slug, "linha": linha,
            "url": "https://%s/%s" % (config["dominio"], slug),
            "motivo": "ja existe (no manifesto ou em disco)"}


def processar(repo, solicitacoes, config, speakers, dry_run=False,
              permitir_exemplo=False):
    caminho_manifesto, manifesto = carregar_manifesto(repo, config)
    existentes = {lp["slug"] for lp in manifesto["lps"]}
    teto = config["limites"]["lps_por_execucao"]

    relatorio = {"criadas": [], "recusadas": [], "ignoradas": [],
                 "manifesto_alterado": False, "teto": teto}

    for pedido in solicitacoes:
        linha = pedido.get("linha")
        solicitante = pedido.get("solicitante", "")

        if len(relatorio["criadas"]) >= teto:
            relatorio["recusadas"].append({
                "linha": linha, "solicitante": solicitante,
                "motivos": ["teto de %d LPs por execucao atingido; esta solicitacao "
                            "fica pra proxima rodada" % teto]})
            continue

        # Idempotencia: reprocessar a mesma linha (retry do webhook, varredura
        # diaria depois do webhook) nao pode recriar nem sobrescrever nada. Checa
        # ANTES de validar: uma LP ja no ar pode ter ficado invalida depois (data
        # que passou, modulo que sumiu num religamento do formulario, 2026-09-23)
        # e recusa-la derrubaria o job por uma linha que ja esta resolvida.
        previsto = rpe.slug_previsto(pedido, config)
        if not (previsto and ja_existe(repo, config, existentes, previsto)):
            previsto = publicada_antes(repo, config, pedido)
        if previsto:
            relatorio["ignoradas"].append(ignorada(config, previsto, linha))
            continue

        try:
            slug, arquivos = rpe.render(pedido, config, speakers,
                                        permitir_exemplo=permitir_exemplo)
        except ValueError as e:
            relatorio["recusadas"].append({
                "linha": linha, "solicitante": solicitante,
                "titulo": pedido.get("titulo", ""),
                "motivos": str(e).splitlines()})
            continue

        destino_rel = "%s/%s" % (config["destino_source"], slug)
        destino_abs = os.path.join(repo, destino_rel.replace("/", os.sep))

        if ja_existe(repo, config, existentes, slug):
            relatorio["ignoradas"].append(ignorada(config, slug, linha))
            continue

        if not dry_run:
            os.makedirs(destino_abs, exist_ok=True)
            for nome, conteudo in arquivos.items():
                io.open(os.path.join(destino_abs, nome), "w", encoding="utf-8",
                        newline="\n").write(conteudo)
            manifesto["lps"].append({"slug": slug, "marca": config["marca"],
                                     "source": destino_rel})
            manifesto["lps"].sort(key=lambda lp: lp["slug"])
            relatorio["manifesto_alterado"] = True

        existentes.add(slug)
        relatorio["criadas"].append({
            "slug": slug, "linha": linha, "solicitante": solicitante,
            "titulo": pedido["titulo"], "dir": destino_rel,
            "url": "https://%s/%s" % (config["dominio"], slug)})

    if relatorio["manifesto_alterado"] and not dry_run:
        salvar_manifesto(caminho_manifesto, manifesto)

    return relatorio


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("solicitacoes", help="JSON: lista de solicitacoes (ou 1 objeto)")
    ap.add_argument("--repo", default=os.environ.get("REPO_ROOT") or
                    os.path.abspath(os.path.join(AQUI, "..", "..")))
    ap.add_argument("--dry-run", action="store_true",
                    help="valida e monta o relatorio sem escrever nada")
    ap.add_argument("--permitir-exemplo", action="store_true",
                    help="aceita o speaker de exemplo do cadastro (so pra ensaio; "
                         "o workflow nunca passa isso)")
    args = ap.parse_args()

    config, speakers = rpe.carregar("config.json"), rpe.carregar("speakers.json")
    if not config.get("form_endpoint"):
        sys.stderr.write("AVISO: config.form_endpoint vazio - as LPs vao ao ar com "
                         "formulario que valida mas nao grava na planilha.\n")

    dados = json.load(io.open(args.solicitacoes, encoding="utf-8"))
    if isinstance(dados, dict):
        dados = dados.get("solicitacoes", [dados])
    if not isinstance(dados, list):
        sys.stderr.write("esperava uma lista de solicitacoes\n")
        return 2

    relatorio = processar(args.repo, dados, config, speakers, args.dry_run,
                          args.permitir_exemplo)
    print(json.dumps(relatorio, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
