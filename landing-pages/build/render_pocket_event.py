"""render_pocket_event.py — transforma 1 solicitacao de Pocket Event nos
arquivos da LP, de forma deterministica.

Nao ha interpretacao aqui: toda escolha de conteudo ou ja veio de uma lista
fechada do formulario (nicho, modulo, horario, speaker) ou e derivada por regra
fixa (slug, datas por extenso, meta tags). O unico texto livre e o titulo, e ele
passa por um validador estrito antes de encostar no HTML.

Fonte das opcoes e limites: templates/pocket-event/config.json
Cadastro de quem apresenta:  templates/pocket-event/speakers.json
Template da pagina:          templates/pocket-event/index.html.tmpl

USO
---
    py render_pocket_event.py <solicitacao.json> [--out DIR] [--permitir-exemplo]
    py render_pocket_event.py --form-spec            # opcoes p/ o Apps Script
    py render_pocket_event.py --autoteste            # fixture embutida

Exit 0 = renderizou (ou passou no autoteste); 1 = solicitacao invalida; 2 = erro
de uso/interno. Os erros de validacao saem em stderr, um por linha.
"""
import argparse
import datetime
import html
import io
import json
import os
import re
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(AQUI, "templates", "pocket-event")

MESES = ("janeiro", "fevereiro", "marco", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro")
DIAS_SEMANA = ("segunda-feira", "terca-feira", "quarta-feira", "quinta-feira",
               "sexta-feira", "sabado", "domingo")

CAMPOS = ("titulo", "nicho", "modulo", "data", "horario", "speaker")

# Caracteres que nunca entram num titulo de Pocket Event. Os tres primeiros
# grupos quebrariam o HTML ou a string JS; os travessoes e aspas curvas sao a
# regra anti-IA da casa (conhecimento/editorial/regras-anti-ia.md).
PROIBIDOS = {
    "<": "menor-que", ">": "maior-que", '"': "aspas retas", "'": "apostrofo",
    "\\": "barra invertida", "`": "crase", "{": "chave", "}": "chave",
    "—": "travessao (em-dash)", "–": "meia-risca (en-dash)",
    "“": "aspas curvas", "”": "aspas curvas",
    "‘": "aspas curvas", "’": "aspas curvas",
}


def carregar(nome):
    return json.load(io.open(os.path.join(TEMPLATE_DIR, nome), encoding="utf-8"))


def kebab(texto):
    """Minusculas, sem acento, so [a-z0-9-]. Deterministico."""
    sem_acento = "".join(c for c in unicodedata.normalize("NFD", texto)
                         if unicodedata.category(c) != "Mn")
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", sem_acento.lower())).strip("-")


def por_valor(lista, valor):
    for item in lista:
        if item["valor"] == valor:
            return item
    return None


def data_extenso(d, hoje):
    """'8 de outubro' — com o ano so quando o evento cai em outro ano."""
    base = "%d de %s" % (d.day, MESES[d.month - 1])
    return base if d.year == hoje.year else "%s de %d" % (base, d.year)


def validar(dados, config, speakers, hoje=None, permitir_exemplo=False):
    """Devolve (erros[], normalizado{}). Lista vazia de erros = pode renderizar."""
    hoje = hoje or datetime.date.today()
    erros = []
    norm = {}

    for campo in CAMPOS:
        if not str(dados.get(campo, "")).strip():
            erros.append("campo obrigatorio ausente ou vazio: %s" % campo)
    if erros:
        return erros, norm

    # --- titulo (unico texto livre do formulario) ---
    titulo = " ".join(str(dados["titulo"]).split())  # colapsa espacos e quebras
    lim = config["limites"]
    if len(titulo) < lim["titulo_min"]:
        erros.append("titulo curto demais (%d caracteres, minimo %d): %r"
                     % (len(titulo), lim["titulo_min"], titulo))
    if len(titulo) > lim["titulo_max"]:
        erros.append("titulo longo demais (%d caracteres, maximo %d): %r"
                     % (len(titulo), lim["titulo_max"], titulo))
    for char, nome in PROIBIDOS.items():
        if char in titulo:
            erros.append("titulo tem caractere proibido %s (%s): %r" % (char, nome, titulo))
    if titulo.endswith("."):
        erros.append("titulo nao termina em ponto final: %r" % titulo)
    norm["titulo"] = titulo

    # --- listas fechadas ---
    nicho = por_valor(config["nichos"], str(dados["nicho"]).strip())
    if nicho is None:
        erros.append("nicho fora da lista: %r (validos: %s)"
                     % (dados["nicho"], ", ".join(n["valor"] for n in config["nichos"])))
    norm["nicho"] = nicho

    # Modulo e multipla escolha: um encontro pode cobrir mais de um. O Google Forms
    # entrega as caixas marcadas como "A, B, C" numa celula so; aceitamos tambem
    # lista, pra quem chamar o job direto com JSON.
    pedidos = dados["modulo"]
    if not isinstance(pedidos, (list, tuple)):
        pedidos = [p.strip() for p in str(pedidos).split(",")]
    pedidos = [p for p in (str(p).strip() for p in pedidos) if p]
    if not pedidos:
        erros.append("nenhum modulo informado")
    modulos = []
    for p in pedidos:
        achado = por_valor(config["modulos"], p)
        if achado is None:
            erros.append("modulo fora da lista: %r (validos: %s)"
                         % (p, ", ".join(m["valor"] for m in config["modulos"])))
        elif achado not in modulos:  # marcar duas vezes nao duplica na frase
            modulos.append(achado)
    norm["modulos"] = modulos

    horario = str(dados["horario"]).strip()
    if horario not in config["horarios"]:
        erros.append("horario fora da lista: %r (validos: %s)"
                     % (horario, ", ".join(config["horarios"])))
    norm["horario"] = horario

    # --- speaker (bio, cargo e foto vem do cadastro, nunca do formulario) ---
    pedido = str(dados["speaker"]).strip()
    achado = None
    for s in speakers["speakers"]:
        if pedido in (s["id"], s["nome"]):
            achado = s
            break
    if achado is None:
        erros.append("speaker fora do cadastro: %r (cadastrados: %s)"
                     % (pedido, ", ".join(s["id"] for s in speakers["speakers"])))
    elif achado.get("exemplo") and not permitir_exemplo:
        erros.append("speaker %r e entrada de exemplo do cadastro, nao pode ir pro ar"
                     % achado["id"])
    norm["speaker"] = achado

    # --- data ---
    bruto = str(dados["data"]).strip()
    try:
        data = datetime.date.fromisoformat(bruto[:10])
    except ValueError:
        erros.append("data fora do formato AAAA-MM-DD: %r" % bruto)
        data = None
    if data is not None:
        dias = (data - hoje).days
        if dias < lim["dias_minimo"]:
            erros.append("data no passado ou perto demais: %s (faltam %d dias, minimo %d)"
                         % (data.isoformat(), dias, lim["dias_minimo"]))
        if dias > lim["dias_maximo"]:
            erros.append("data longe demais: %s (faltam %d dias, maximo %d)"
                         % (data.isoformat(), dias, lim["dias_maximo"]))
    norm["data"] = data

    return erros, norm


def montar_slug(norm):
    """pocket-{nicho}-{AAAA-MM-DD}. Sem titulo: titulo e texto livre e mudaria a
    URL a cada correcao de digitacao."""
    return "pocket-%s-%s" % (norm["nicho"]["slug"], norm["data"].isoformat())


def foto_html(speaker):
    """<img> quando ha foto cadastrada; iniciais com o degrade da marca quando nao.
    Nunca devolve placeholder — LP no ar nao exibe '[ FOTO DO SPEAKER ]'."""
    if speaker.get("foto"):
        rel = "../../" + speaker["foto"].lstrip("/")
        return ('<img src="%s" alt="%s" class="sp-img" width="168" height="168" />'
                % (html.escape(rel, quote=True), html.escape(speaker["nome"], quote=True)))
    iniciais = "".join(p[0] for p in speaker["nome"].split()[:2]).upper()
    return ('<span class="sp-initials" aria-hidden="true">%s</span>'
            % html.escape(iniciais))


def juntar(itens):
    """['A'] -> 'A' | ['A','B'] -> 'A e B' | ['A','B','C'] -> 'A, B e C'."""
    if len(itens) == 1:
        return itens[0]
    return "%s e %s" % (", ".join(itens[:-1]), itens[-1])


def bio_html(speaker):
    """Bio e opcional no cadastro. Sem bio, o paragrafo inteiro sai do HTML: card
    com nome e cargo e honesto, card com bio inventada nao."""
    bio = (speaker.get("bio") or "").strip()
    if not bio:
        return ""
    return '          <p class="sp-bio">%s</p>' % html.escape(bio)


def render(dados, config, speakers, hoje=None, permitir_exemplo=False):
    """Devolve (slug, {nome_do_arquivo: conteudo}). Levanta ValueError se invalido."""
    hoje = hoje or datetime.date.today()
    erros, norm = validar(dados, config, speakers, hoje, permitir_exemplo)
    if erros:
        raise ValueError("\n".join(erros))

    data, speaker = norm["data"], norm["speaker"]
    slug = montar_slug(norm)
    extenso = data_extenso(data, hoje)

    titulo_pagina = config["titulo_pagina"].format(titulo=norm["titulo"])
    meta = config["meta_description"].format(
        nicho=norm["nicho"]["frase"], data_extenso=extenso, horario=norm["horario"])

    valores = {
        "TITULO": html.escape(norm["titulo"]),
        "TITULO_TEXTO": norm["titulo"],
        "TITULO_PAGINA": html.escape(titulo_pagina, quote=True),
        "META_DESCRIPTION": html.escape(meta, quote=True),
        "NICHO": html.escape(norm["nicho"]["frase"]),
        "MODULO": html.escape(juntar([m["frase"] for m in norm["modulos"]])),
        "DATA_EXTENSO": html.escape(extenso),
        "DATA_ISO": data.isoformat(),
        "HORARIO": html.escape(norm["horario"]),
        "HORARIO_TEXTO": norm["horario"],
        "DD": "%02d" % data.day,
        "MM": "%02d" % data.month,
        "DIA_SEMANA": DIAS_SEMANA[data.weekday()],
        "SPEAKER_NOME": html.escape(speaker["nome"]),
        "SPEAKER_NOME_TEXTO": speaker["nome"],
        "SPEAKER_CARGO": html.escape(speaker["cargo"]),
        "SPEAKER_BIO_BLOCO": bio_html(speaker),
        "SPEAKER_FOTO": foto_html(speaker),
        "SLUG": slug,
        "ANO": str(data.year),
        "GTM_ID": config["gtm_id"],
        "FORM_ENDPOINT": config.get("form_endpoint", ""),
    }

    tmpl = io.open(os.path.join(TEMPLATE_DIR, "index.html.tmpl"), encoding="utf-8").read()
    for chave, valor in valores.items():
        tmpl = tmpl.replace("{{%s}}" % chave, valor)

    sobrou = re.findall(r"\{\{[A-Z_]+\}\}", tmpl)
    if sobrou:
        raise ValueError("token nao substituido no template: %s" % ", ".join(sorted(set(sobrou))))

    # Anti-IA de tolerancia zero (regras-anti-ia.md): em-dash nao passa, nem como
    # entidade HTML. Checar aqui e nao so no titulo protege tambem a copy fixa do
    # template, que ninguem re-audita a cada edicao.
    if "—" in tmpl or "&mdash;" in tmpl:
        raise ValueError("em-dash no HTML gerado (tolerancia zero): trocar por virgula, "
                         "ponto, dois-pontos ou parenteses no index.html.tmpl")

    return slug, {
        "index.html": tmpl,
        "copy.txt": _copy_txt(slug, norm, speaker, extenso, valores),
        "README.md": _readme(slug, norm, speaker, extenso, config),
    }


def _copy_txt(slug, norm, speaker, extenso, v):
    return """META
slug: %s
marca: buzzmonitor
regiao: brasil
idioma: pt-br
tipo: evento-fechado
formato: pocket-event (10 vagas, 1 especialista apresentando)
origem: gerado por render_pocket_event.py (nao editar a mao — ver README.md)

---

SECAO: HERO

LABEL: Pocket Event - Apenas 10 vagas
H1: %s
H2: Discussao pratica sobre %s com foco em %s.
INFO: %s - %s - Online ao vivo

TICKET_DATE: %s/%s
TICKET_SUB: %s - %s

---

SECAO: SPEAKER + FORM

SPEAKER_NOME: %s
SPEAKER_CARGO: %s - Buzzmonitor
SPEAKER_BIO: %s

FORM: nativo -> Apps Script -> planilha unica de inscricoes
FORM_CAMPOS: nome, email, empresa, cargo
FORM_OCULTOS: edicao, evento, data_evento, horario, speaker, url_conversao, utm_*

---

SECAO: EMPRESAS QUE CONFIAM / DEPOIMENTOS / URGENCIA / FOOTER

Fixas no template (iguais em toda edicao).
""" % (slug, norm["titulo"], norm["nicho"]["frase"],
       juntar([m["frase"] for m in norm["modulos"]]),
       extenso, norm["horario"], v["DD"], v["MM"], v["DIA_SEMANA"], norm["horario"],
       speaker["nome"], speaker["cargo"], speaker["bio"])


def _readme(slug, norm, speaker, extenso, config):
    return """# Pocket Event - %s

**Gerado automaticamente.** Nao editar este diretorio a mao: ele e recriado a
partir de `landing-pages/build/templates/pocket-event/` sempre que a solicitacao
for reprocessada, e qualquer edicao local se perde.

Pra mudar o texto de TODA edicao: `templates/pocket-event/index.html.tmpl`.
Pra mudar esta edicao: corrigir a linha na planilha e reprocessar.

| Campo | Valor |
|---|---|
| Slug | `%s` |
| URL | https://%s/%s |
| Titulo | %s |
| Nicho | %s |
| Modulo | %s |
| Data | %s (%s) |
| Speaker | %s - %s |
| Form | Apps Script (planilha unica de inscricoes) |
| GTM | %s |
""" % (norm["titulo"], slug, config["dominio"], slug, norm["titulo"],
       norm["nicho"]["valor"], ", ".join(m["valor"] for m in norm["modulos"]),
       extenso, norm["horario"],
       speaker["nome"], speaker["cargo"], config["gtm_id"])


def form_spec(config, speakers):
    """Opcoes exatas pro dropdown do formulario de solicitacao (Apps Script)."""
    return {
        "nichos": [n["valor"] for n in config["nichos"]],
        "modulos": [m["valor"] for m in config["modulos"]],
        "horarios": list(config["horarios"]),
        "speakers": [{"id": s["id"], "nome": s["nome"], "cargo": s["cargo"]}
                     for s in speakers["speakers"] if not s.get("exemplo")],
        "titulo_max": config["limites"]["titulo_max"],
        "dias_maximo": config["limites"]["dias_maximo"],
    }


def autoteste():
    """Fixture minima: prova que template + config + renderer batem entre si.

    O cadastro de speakers e sintetico, nao o speakers.json real: o teste nao pode
    quebrar (nem passar por acidente) por causa de quem entrou ou saiu do cadastro.
    """
    config = carregar("config.json")
    speakers = {"speakers": [
        {"id": "com-bio", "nome": "Fulana de Teste", "cargo": "Business Developer",
         "bio": "Duas linhas de bio que existem so pra este teste.", "foto": None},
        {"id": "sem-bio", "nome": "Beltrano de Teste", "cargo": "Business Developer",
         "bio": None, "foto": None},
        {"id": "com-foto", "nome": "Sicrana de Teste", "cargo": "Business Developer",
         "bio": None, "foto": "brand/buzzmonitor/assets/speakers/sicrana.jpg"},
        {"id": "so-exemplo", "nome": "Exemplo Exemplo", "cargo": "Business Developer",
         "bio": None, "foto": None, "exemplo": True},
    ]}
    hoje = datetime.date(2026, 9, 14)
    pedido = {"titulo": "Como o varejo escuta o cliente em tempo real",
              "nicho": "Alimentos (varejo)", "modulo": "Social Listening",
              "data": "2026-10-08", "horario": "11h", "speaker": "com-bio"}

    slug, arquivos = render(pedido, config, speakers, hoje)
    assert slug == "pocket-alimentos-varejo-2026-10-08", slug
    h = arquivos["index.html"]
    for esperado in ("Como o varejo escuta o cliente em tempo real",
                     "varejo de alimentos", "Social Listening", "8 de outubro",
                     "quinta-feira", "08<span", "pocket-alimentos-varejo-2026-10-08",
                     "GTM-WFJVK858", "Duas linhas de bio", 'class="sp-bio"'):
        assert esperado in h, "faltou no HTML: %s" % esperado
    assert "{{" not in h and "[ FOTO DO SPEAKER ]" not in h

    # multiplos modulos: a frase junta com virgula e "e"
    _, dois = render({**pedido, "modulo": "Social Listening, AI Insights"},
                     config, speakers, hoje)
    assert "Social Listening e AI Insights" in dois["index.html"]
    _, tres = render({**pedido, "modulo": ["Social Listening", "AI Insights", "Buzz GPT"]},
                     config, speakers, hoje)
    assert "Social Listening, AI Insights e Buzz GPT" in tres["index.html"]
    # marcar o mesmo modulo duas vezes nao duplica na frase
    _, rep = render({**pedido, "modulo": "AI Insights, AI Insights"}, config, speakers, hoje)
    assert rep["index.html"].count("AI Insights") >= 1
    assert "AI Insights e AI Insights" not in rep["index.html"]

    # sem bio: o paragrafo inteiro some, e nada e inventado no lugar
    _, sem = render({**pedido, "speaker": "sem-bio"}, config, speakers, hoje)
    assert 'class="sp-bio"' not in sem["index.html"]
    assert "Beltrano de Teste" in sem["index.html"]
    assert 'class="sp-initials"' in sem["index.html"]  # cai nas iniciais sem foto

    # com foto: <img> com min-height:0 garantido pelo CSS do template
    _, foto = render({**pedido, "speaker": "com-foto"}, config, speakers, hoje)
    assert 'class="sp-img"' in foto["index.html"]
    assert "sicrana.jpg" in foto["index.html"]

    casos_ruins = [
        ({**pedido, "titulo": "curto"}, "titulo curto"),
        ({**pedido, "titulo": "Titulo com travessao — proibido"}, "travessao"),
        ({**pedido, "titulo": "<script>alert(1)</script> no titulo"}, "caractere proibido"),
        ({**pedido, "nicho": "Pet shop"}, "nicho invalido"),
        ({**pedido, "modulo": "BuzzMonitor Listening"}, "modulo invalido"),
        ({**pedido, "modulo": "Social Listening, Nao Existe"}, "um modulo invalido na lista"),
        ({**pedido, "modulo": ""}, "nenhum modulo"),
        ({**pedido, "horario": "23h"}, "horario invalido"),
        ({**pedido, "data": "2026-09-01"}, "data no passado"),
        ({**pedido, "data": "2027-09-01"}, "data longe demais"),
        ({**pedido, "data": "08/10/2026"}, "data em formato errado"),
        ({**pedido, "speaker": "fulano"}, "speaker fora do cadastro"),
        ({**pedido, "speaker": "so-exemplo"}, "speaker marcado como exemplo"),
    ]
    for ruim, rotulo in casos_ruins:
        erros, _ = validar(ruim, config, speakers, hoje)
        assert erros, "deveria ter recusado: %s" % rotulo

    # ano so aparece quando o evento cai em outro ano
    assert data_extenso(datetime.date(2026, 10, 8), hoje) == "8 de outubro"
    assert data_extenso(datetime.date(2027, 1, 20), hoje) == "20 de janeiro de 2027"

    # o cadastro real tem que continuar carregavel e coerente
    reais = carregar("speakers.json")["speakers"]
    ids = [x["id"] for x in reais]
    assert len(set(ids)) == len(ids), "id duplicado no speakers.json"
    for x in reais:
        assert x.get("nome") and x.get("cargo"), "speaker sem nome ou cargo: %s" % x

    # nichos: slug unico (slug repetido faria duas edicoes colidirem na mesma URL)
    slugs = [n["slug"] for n in config["nichos"]]
    assert len(set(slugs)) == len(slugs), "slug de nicho duplicado no config.json"
    for n in config["nichos"]:
        assert n["valor"] and n["slug"] and n["frase"], "nicho incompleto: %s" % n

    print("autoteste ok: %d renders + %d recusas + %d nichos + %d speakers"
          % (7, len(casos_ruins), len(config["nichos"]), len(reais)))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("solicitacao", nargs="?", help="JSON com a solicitacao")
    ap.add_argument("--out", help="diretorio de saida (default: so valida e imprime resumo)")
    ap.add_argument("--permitir-exemplo", action="store_true",
                    help="aceita o speaker de exemplo (so pra teste)")
    ap.add_argument("--form-spec", action="store_true", help="opcoes pro Apps Script")
    ap.add_argument("--autoteste", action="store_true")
    args = ap.parse_args()

    config, speakers = carregar("config.json"), carregar("speakers.json")

    if args.autoteste:
        autoteste()
        return 0
    if args.form_spec:
        print(json.dumps(form_spec(config, speakers), ensure_ascii=False, indent=2))
        return 0
    if not args.solicitacao:
        ap.error("informe a solicitacao.json, --form-spec ou --autoteste")

    dados = json.load(io.open(args.solicitacao, encoding="utf-8"))
    try:
        slug, arquivos = render(dados, config, speakers,
                                permitir_exemplo=args.permitir_exemplo)
    except ValueError as e:
        sys.stderr.write("SOLICITACAO INVALIDA:\n")
        for linha in str(e).splitlines():
            sys.stderr.write("  - %s\n" % linha)
        return 1

    if not config.get("form_endpoint"):
        sys.stderr.write("AVISO: config.form_endpoint vazio - a LP valida o form mas "
                         "nao envia pra planilha.\n")
    if args.out:
        destino = os.path.join(args.out, slug)
        os.makedirs(destino, exist_ok=True)
        for nome, conteudo in arquivos.items():
            io.open(os.path.join(destino, nome), "w", encoding="utf-8",
                    newline="\n").write(conteudo)
        print(json.dumps({"slug": slug, "dir": destino,
                          "arquivos": sorted(arquivos)}, ensure_ascii=False))
    else:
        print(json.dumps({"slug": slug, "bytes_html": len(arquivos["index.html"])},
                         ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
