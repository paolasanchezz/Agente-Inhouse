"""
Analise tematica dos campos de dor e feature em Buzzmonitor Brasil.
Conta top palavras, bigramas e trigramas para deixar os dados sugerirem temas.
"""
import csv
import re
from collections import Counter
from pathlib import Path

STOPWORDS = set("""
a o e de da do das dos para por com em na no nas nos as os ja já ainda ou nem mas
porem porém entre cada qual quais como onde quando muito pouco bem mal só sim
seu sua seus suas meu minha nosso nossa este esta isso isto esse essa aquilo
aquele aquela ser estar ter haver fazer ir vir dar ver dizer poder querer saber
foi era e sao estao está estão tem tem tinha tinham have tido sido feito vai
sobre tambem também tb tbm pelo pela pelos pelas ate até sem nao não  só
ao a as à às um uma uns umas que se mas porem porém ja já entre todo toda
todos todas mesmo mesma cada cada um uma  qualquer alguns algumas algum alguma
muitos muitas vario varios varia varias outra outras outro outros entao então
porque por que assim apenas alem além qq qto qq sob ate até desde quanto
cliente clientes empresa empresas marca marcas equipe equipes time times
usuario usuario usuarios usuario pessoa pessoas tema temas pode pode  podem
precisa precisam usa usar usam uso utiliza utilizam utilizacao utilização atual atualmente
forma formas conta contas vez vezes deve devem possui possuem buzz buzzmonitor
plataforma plataformas ferramenta ferramentas sistema sistemas processo processos
servico servicos serviço serviços conteudo conteúdo conteudos conteúdos parte
alguma algumas algum bom boa nivel nível ano anos mes mês meses dia dias hora horas
momento momentos varios varias possivel possível necessario necessário n n. no novo nova novos novas
projeto projetos negocio negócio negocios negócios trabalho trabalhos area área areas áreas
sera será cada caso casos tipo tipos modo modos meio meios geral gerais
todas todos demais outros outras qualquer pq tu lo la ele ela eles elas isso
""".split())


def tokenize(text: str) -> list[str]:
    text = text.lower()
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[^a-záéíóúâêôãõçàü\s-]", " ", text)
    words = text.split()
    return [w for w in words if len(w) >= 4 and w not in STOPWORDS and not w.isdigit()]


def ngrams(words: list[str], n: int) -> list[tuple]:
    return list(zip(*[words[i:] for i in range(n)]))


def show(title: str, counter: Counter, n: int = 50) -> None:
    print(f"\n=== {title} ===")
    for term, c in counter.most_common(n):
        term_str = term if isinstance(term, str) else " ".join(term)
        print(f"  {c:5d}  {term_str}")


def main() -> None:
    base = Path(__file__).parent.parent / "conhecimento" / "clientes-fechados" / "dor-features-buzzmonitor-brasil.csv"
    with base.open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    print(f"Total deals analisados: {len(rows)}")

    dor_cols = ["dor_dores_atuais", "dor_spin_problema", "dor_spin_implicacao", "dor_bant_need"]
    feat_cols = ["feature_principais_modulos", "feature_objetivo", "feature_spin_necessidade"]

    dor_words: list[str] = []
    feat_words: list[str] = []
    for r in rows:
        for c in dor_cols:
            dor_words += tokenize(r.get(c) or "")
        for c in feat_cols:
            feat_words += tokenize(r.get(c) or "")

    show("DOR | top 1-gramas", Counter(dor_words), 50)
    show("DOR | top 2-gramas", Counter(ngrams(dor_words, 2)), 50)
    show("DOR | top 3-gramas", Counter(ngrams(dor_words, 3)), 30)

    show("FEATURE | top 1-gramas", Counter(feat_words), 50)
    show("FEATURE | top 2-gramas", Counter(ngrams(feat_words, 2)), 50)
    show("FEATURE | top 3-gramas", Counter(ngrams(feat_words, 3)), 30)


if __name__ == "__main__":
    main()
