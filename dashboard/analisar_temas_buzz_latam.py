"""
Analise tematica dos campos de dor e feature em Buzzmonitor LATAM.
Conta top palavras, bigramas e trigramas para deixar os dados sugerirem temas.
Texto em espanhol — stopwords adaptadas.
"""
import csv
import re
from collections import Counter
from pathlib import Path

# Stopwords ES + PT (mistura porque alguns textos vem em PT)
STOPWORDS = set("""
el la los las un una unos unas de del al a y o u en con por para sin sobre entre
desde hasta tras durante mediante segun según contra hacia hasta porque cuando como
donde quien quienes que cual cuales este esta estos estas ese esa esos esas aquel
aquella aquellos aquellas mismo misma mismos mismas pero sino sino tambien también
solo solamente muy mas más menos tanto tanta tantos tantas algun alguna algunos algunas
ningun ninguna ningunos ningunas todo toda todos todas otro otra otros otras
hay habia había habra había había es son fue era ser sido siendo estar esta está
estan están estaba estaban tiene tienen tenia tenía hace hacer hizo haya
le lo les nos os me te se mi mis tu tus su sus nuestro nuestra nuestros nuestras
ya aun aún todavia todavía mientras tras
a o e de da do das dos para por com em na no nas nos as os ja já ainda ou nem mas
porem porém entre cada qual quais como onde quando muito pouco bem mal só sim
seu sua seus suas meu minha nosso nossa este esta isso isto esse essa aquilo
aquele aquela ser estar ter haver fazer ir vir dar ver dizer poder querer saber
foi era sao estao está estão tem tem tinha tinham have tido sido feito vai
sobre tambem também tb tbm pelo pela pelos pelas ate até sem nao não
cliente clientes empresa empresas marca marcas equipe equipes time times equipo equipos
usuario usuarios pessoa pessoas tema temas pode podem precisa precisam usa usar usam
uso utiliza utilizam utilizacao utilização utilizan utilizando atual actual actualmente atualmente
forma formas conta contas vez vezes deve devem possui possuem posee posee tiene
plataforma plataformas ferramenta ferramentas sistema sistemas herramienta herramientas
processo processos proceso procesos servico servicos serviço serviços servicio servicios
conteudo conteúdo conteudos contenido contenidos parte partes alguma algumas algum alguma
buen buena bueno buenos nivel nivel año años mes meses dia dias hora horas
momento momentos varios vários possivel possível posible necesario necessario necessário
n n. no- novo nova novos novas nuevo nueva nuevos nuevas projeto projetos proyecto proyectos
negocio negócio negocios negócios trabalho trabalhos trabajo trabajos area área areas áreas
buzzmonitor agencia agência agencias agências cuenta cuentas
sera será cada caso casos tipo tipos modo modos meio meios geral gerais general generales
todas todos demais outros outras qualquer cualquier pq tu lo la ele ela eles elas isso
otros otras tambien también incluso aun más más mais
""".split())


def tokenize(text: str) -> list[str]:
    text = text.lower()
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[^a-záéíóúâêôãõçàüñ\s-]", " ", text)
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
    base = Path(__file__).parent.parent / "conhecimento" / "clientes-fechados" / "dor-features-buzzmonitor-latam.csv"
    with base.open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    print(f"Total deals analisados: {len(rows)}")

    dor_cols = ["dor_areas_oportunidade", "dor_problema_lead", "dor_spin_problema", "dor_spin_implicacao"]
    feat_cols = [
        "feature_principais_modulos",
        "feature_objetivo",
        "feature_oportunidades_futuras",
        "feature_spin_necessidade",
    ]

    dor_words: list[str] = []
    feat_words: list[str] = []
    for r in rows:
        for c in dor_cols:
            dor_words += tokenize(r.get(c) or "")
        for c in feat_cols:
            feat_words += tokenize(r.get(c) or "")

    show("DOR | top 1-gramas", Counter(dor_words), 60)
    show("DOR | top 2-gramas", Counter(ngrams(dor_words, 2)), 50)
    show("DOR | top 3-gramas", Counter(ngrams(dor_words, 3)), 30)

    show("FEATURE | top 1-gramas", Counter(feat_words), 60)
    show("FEATURE | top 2-gramas", Counter(ngrams(feat_words, 2)), 50)
    show("FEATURE | top 3-gramas", Counter(ngrams(feat_words, 3)), 30)


if __name__ == "__main__":
    main()
