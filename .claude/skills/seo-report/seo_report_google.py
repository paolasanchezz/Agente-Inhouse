"""
SEO Report — coletor Google (GSC + GA4), multi-contexto (marca x regiao)

Coleta dados do Google Search Console e do Google Analytics 4 via OAuth2
(conta Google do proprio usuario), para todos os contextos configurados em
CONTEXTS abaixo. NAO coleta Semrush nem Supabase: isso e feito pela skill
/seo-report via MCP do Semrush e via psycopg (ver .claude/skills/seo-report/
seo_report_conversoes.py), respectivamente.

Credenciais e saida ficam FORA do repositorio, num diretorio de trabalho
por usuario (nunca commitado):
  - por padrao: ~/.seo-report-buzzmonitor/
  - ou defina a variavel de ambiente SEO_REPORT_DIR para apontar outro lugar

Arquivos nesse diretorio:
  - client_secret.json  (voce baixa do Google Cloud Console — entrada)
  - token.json          (gerado no 1o login — nao commitar)
  - seo_data.json       (saida — consumida pela skill)

Como usar:
  1. Coloque client_secret.json no diretorio de trabalho (ver acima)
  2. Rode: python seo_report_google.py
  3. No 1o uso abre o navegador para autorizar (login Google)
  4. Gera seo_data.json com uma secao "contexts", 1 entrada por contexto
     configurado (contextos sem gsc_site/ga4_properties ficam com
     gsc=None / ga4=None — a skill mostra "fonte nao configurada")
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest, DateRange, Metric, Dimension, OrderBy,
    Filter, FilterExpression, FilterExpressionList
)

# ============================================================
# CONFIGURAÇÃO POR CONTEXTO (marca x regiao)
# ============================================================
# gsc_site: propriedade do Search Console (sc-domain:... ou URL-prefixo). None = sem acesso ainda.
# ga4_properties: dict {bucket_label: property_id}. Contextos onde site+blog compartilham o
#   MESMO domInio (Buzzmonitor) usam 1 soh property e o split site/blog vem de blog_match
#   (filtro de path aplicado na query). Contextos onde site e blog sao properties GA4
#   DISTINTAS (Cxpress) listam as duas aqui e o script soma pra formar o "total".
# region_match: substring que restringe a propriedade aa fatia desse contexto (necessario
#   quando 2 regioes dividem o mesmo dominio/property — ex. buzzmonitor.com/es/ e /pt-pt/
#   dividem a MESMA property GA4). None quando a propriedade ja e exclusiva do contexto.
# blog_match: substring que identifica paginas/sessoes de blog dentro do que jah foi
#   restringido por region_match. Usada tanto em GSC (dimensao "page", URL completa)
#   quanto em GA4 (dimensao "pagePath" ou, no caso de property dedicada, dispensada).
CONTEXTS = {
    "buzzmonitor-br": {
        "label": "Buzzmonitor BR",
        "gsc_site": "sc-domain:buzzmonitor.com",
        # G-8RFQ3EHK6B, GTM-PDSV26W. Property ID 347467970 (confirmado Out/2026 — nao
        # confundir com Stream ID 4379354626 que aparece no Tag Assistant).
        "ga4_properties": {"combinado": "347467970"},
        "region_match": None,
        "blog_match": "/blog/",
    },
    "buzzmonitor-latam": {
        "label": "Buzzmonitor LATAM",
        # Migracao ~20/Set/2026: getbuzzmonitor.com/es/ -> buzzmonitor.com/es/.
        # Agora compartilha sc-domain com BM BR; region_match /es/ filtra corretamente.
        # Blog passou a ter path distinto (/blog/es/) — blog_match por substring resolve.
        # GA4: G-0LBBM4WJ2Z, GTM-PC4TJ6H. Property ID 347502824 (nao confundir com
        # Stream ID 4379559544). Mesma property da BM PT.
        "gsc_site": "sc-domain:buzzmonitor.com",
        "ga4_properties": {"combinado": "347502824"},
        "region_match": "/es/",
        "blog_match": "/blog/",
    },
    "buzzmonitor-pt": {
        "label": "Buzzmonitor Portugal",
        # Migracao ~20/Set/2026: getbuzzmonitor.com/pt/ -> buzzmonitor.com/pt-pt/.
        # Compartilha sc-domain com BM BR; region_match /pt-pt/ filtra corretamente.
        # GA4: G-0LBBM4WJ2Z, Property ID 347502824 — mesma property da LATAM.
        # Path correto e /pt-pt/ (nao /pt/) — confirmado Tag Assistant Out/2026.
        "gsc_site": "sc-domain:buzzmonitor.com",
        "ga4_properties": {"combinado": "347502824"},
        "region_match": "/pt-pt/",
        "blog_match": "/blog/",
    },
    "cxpress-br": {
        "label": "Cxpress BR",
        "gsc_site": "sc-domain:cxpress.io",
        "ga4_properties": {"site": "339689858", "blog": "345714231"},
        "region_match": None,
        "blog_match": "blog.cxpress.io",
    },
    "cxpress-latam": {
        "label": "Cxpress LATAM",
        # Confirmado com o Maretto (2026-07-28): GA4/GSC NUNCA foram configurados nesse
        # dominio (sem pixel/tag instalado, sem verificacao de propriedade) — nao e "acesso
        # pendente", e "fonte nao existe ainda". Depende de dev instalar o pixel primeiro.
        "gsc_site": None,
        "ga4_properties": None,
        "region_match": None,
        "blog_match": "blog.cxpress.ai",
    },
    "cxpress-pt": {
        "label": "Cxpress Portugal",
        "gsc_site": None,  # idem cxpress-latam: GA4/GSC nunca configurados
        "ga4_properties": None,
        "region_match": None,
        "blog_match": "blog.cxpress.pt",
    },
    "elife-br": {
        "label": "Elife BR",
        "gsc_site": None,  # sem GSC (2026-07-28)
        "ga4_properties": {"combinado": "369456629"},
        "region_match": None,
        # NAO usa "/blog/" (confirmado via Semrush real 2026-07-28) — posts ficam em
        # /index.php/AAAA/MM/DD/slug/ (permalink padrao WordPress por data). O dominio
        # tambem tem subdominios de projeto de cliente (volkswagen-web., koin.) misturados
        # no mesmo target Semrush — esses NAO sao blog, mas tampouco batem "/index.php/",
        # entao caem no bucket "site" corretamente.
        "blog_match": "/index.php/",
    },
    "elife-pt": {
        "label": "Elife Portugal",
        "gsc_site": None,  # sem GSC
        "ga4_properties": None,  # sem GA4 tambem (so Elife BR tem)
        "region_match": None,
        # Presenca organica quase nula no Semrush (2026-07-28) — sem padrao de blog claro
        # pra inferir ainda. Reavaliar quando houver mais dado ou confirmar com o time.
        "blog_match": "/blog/",
    },
}

BASE_DIR = Path(os.environ.get("SEO_REPORT_DIR", Path.home() / ".seo-report-buzzmonitor"))
BASE_DIR.mkdir(parents=True, exist_ok=True)

CLIENT_SECRETS_FILE = str(BASE_DIR / "client_secret.json")
TOKEN_FILE = str(BASE_DIR / "token.json")
OUTPUT_JSON = str(BASE_DIR / "seo_data.json")

SCOPES = [
    "https://www.googleapis.com/auth/webmasters.readonly",
    "https://www.googleapis.com/auth/analytics.readonly",
]

# Período: últimos 28 dias vs 28 dias anteriores (default). Pra comparar mes fechado
# vs mes anterior (ex: relatorio mensal pra diretoria), defina as 4 variaveis de ambiente
# abaixo (formato YYYY-MM-DD) antes de rodar — nao precisa mexer no codigo.
hoje = datetime.today()
if os.environ.get("SEO_REPORT_INICIO"):
    inicio = os.environ["SEO_REPORT_INICIO"]
    fim = os.environ["SEO_REPORT_FIM"]
    inicio_anterior = os.environ["SEO_REPORT_INICIO_ANTERIOR"]
    fim_anterior = os.environ["SEO_REPORT_FIM_ANTERIOR"]
else:
    fim = (hoje - timedelta(days=1)).strftime("%Y-%m-%d")
    inicio = (hoje - timedelta(days=28)).strftime("%Y-%m-%d")
    fim_anterior = (hoje - timedelta(days=29)).strftime("%Y-%m-%d")
    inicio_anterior = (hoje - timedelta(days=56)).strftime("%Y-%m-%d")


# ============================================================
# AUTENTICAÇÃO OAUTH2
# ============================================================
def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRETS_FILE):
                print("❌ client_secret.json não encontrado em:")
                print(f"   {CLIENT_SECRETS_FILE}")
                print("   Baixe as credenciais OAuth2 (Desktop) do Google Cloud Console")
                print("   e salve nesse caminho. Depois rode novamente.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return creds


# ============================================================
# GOOGLE SEARCH CONSOLE (por contexto)
# ============================================================
def _gsc_filter_groups(region_match, blog_match, bucket):
    """Monta dimensionFilterGroups pra restringir a query a um "bucket" (site|blog|total)
    dentro da propriedade GSC, usando a dimensao "page" (URL completa por linha)."""
    filters = []
    if region_match:
        filters.append({"dimension": "page", "operator": "contains", "expression": region_match})
    if bucket == "blog":
        filters.append({"dimension": "page", "operator": "contains", "expression": blog_match})
    elif bucket == "site":
        filters.append({"dimension": "page", "operator": "notContains", "expression": blog_match})
    # bucket == "total": so o region_match (se houver) já restringe; sem filtro extra de blog
    return [{"groupType": "and", "filters": filters}] if filters else []


def _gsc_totais(service, site_url, d_ini, d_fim, region_match, blog_match, bucket):
    body = {
        "startDate": d_ini, "endDate": d_fim, "dimensions": [],
        "dimensionFilterGroups": _gsc_filter_groups(region_match, blog_match, bucket),
    }
    res = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
    rows = res.get("rows", [{}])
    return rows[0] if rows else {}


def get_gsc_data(creds, ctx_key, cfg):
    if not cfg.get("gsc_site"):
        return None
    print(f"🔍 [{cfg['label']}] Coletando Google Search Console...")
    try:
        service = build("searchconsole", "v1", credentials=creds)
        site_url = cfg["gsc_site"]
        region_match = cfg.get("region_match")
        blog_match = cfg["blog_match"]

        buckets = {}
        for bucket in ("site", "blog", "total"):
            atual = _gsc_totais(service, site_url, inicio, fim, region_match, blog_match, bucket)
            anterior = _gsc_totais(service, site_url, inicio_anterior, fim_anterior, region_match, blog_match, bucket)
            buckets[bucket] = {
                "cliques": int(atual.get("clicks", 0)),
                "impressoes": int(atual.get("impressions", 0)),
                "ctr": round(atual.get("ctr", 0) * 100, 2),
                "posicao_media": round(atual.get("position", 0), 1),
                "cliques_anterior": int(anterior.get("clicks", 0)),
                "impressoes_anterior": int(anterior.get("impressions", 0)),
            }

        # Top páginas — restrito ao bucket "blog" (conteudo, o que interessa pro relatorio)
        body_pages = {
            "startDate": inicio, "endDate": fim,
            "dimensions": ["page"], "rowLimit": 25,
            "orderBy": [{"fieldName": "clicks", "sortOrder": "DESCENDING"}],
            "dimensionFilterGroups": _gsc_filter_groups(region_match, blog_match, "blog"),
        }
        res_pages = service.searchanalytics().query(siteUrl=site_url, body=body_pages).execute()
        top_pages = [{
            "url": row["keys"][0],
            "cliques": int(row.get("clicks", 0)),
            "impressoes": int(row.get("impressions", 0)),
            "ctr": round(row.get("ctr", 0) * 100, 2),
            "posicao": round(row.get("position", 0), 1),
        } for row in res_pages.get("rows", [])]

        # Top keywords — mesmo bucket "blog"
        body_kw = {
            "startDate": inicio, "endDate": fim,
            "dimensions": ["query"], "rowLimit": 20,
            "orderBy": [{"fieldName": "clicks", "sortOrder": "DESCENDING"}],
            "dimensionFilterGroups": _gsc_filter_groups(region_match, blog_match, "blog"),
        }
        res_kw = service.searchanalytics().query(siteUrl=site_url, body=body_kw).execute()
        top_keywords = [{
            "keyword": row["keys"][0],
            "cliques": int(row.get("clicks", 0)),
            "impressoes": int(row.get("impressions", 0)),
            "posicao": round(row.get("position", 0), 1),
        } for row in res_kw.get("rows", [])]

        print(f"   ✅ GSC coletado ({cfg['label']})!")
        return {
            "site": buckets["site"],
            "blog": buckets["blog"],
            "total": buckets["total"],
            "top_paginas_blog": top_pages[:10],
            "top_keywords": top_keywords[:15],
        }
    except Exception as e:
        print(f"   ⚠️  Erro no GSC ({cfg['label']}): {e}")
        return {"erro": str(e)}


# ============================================================
# GOOGLE ANALYTICS 4 (por contexto)
# ============================================================
def _ga4_page_filter(region_match, blog_match, bucket):
    """FilterExpression pra dimensao pagePath, usado quando site+blog dividem a MESMA
    property GA4 (contextos com domain unico, ex. Buzzmonitor)."""
    clauses = []
    if region_match:
        clauses.append(FilterExpression(filter=Filter(
            field_name="pagePath",
            string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.CONTAINS, value=region_match),
        )))
    if bucket == "blog":
        clauses.append(FilterExpression(filter=Filter(
            field_name="pagePath",
            string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.CONTAINS, value=blog_match),
        )))
    elif bucket == "site":
        clauses.append(FilterExpression(not_expression=FilterExpression(filter=Filter(
            field_name="pagePath",
            string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.CONTAINS, value=blog_match),
        ))))
    if not clauses:
        return None
    if len(clauses) == 1:
        return clauses[0]
    return FilterExpression(and_group=FilterExpressionList(expressions=clauses))


def _ga4_bucket_filter(cfg, bucket):
    return _ga4_page_filter(cfg.get("region_match"), cfg.get("blog_match"), bucket)


def _ga4_totais(client, property_id, d_ini, d_fim, dimension_filter=None):
    req = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date=d_ini, end_date=d_fim)],
        metrics=[
            Metric(name="sessions"),
            Metric(name="totalUsers"),
            Metric(name="bounceRate"),
            Metric(name="userEngagementDuration"),
        ],
        dimension_filter=dimension_filter,
    )
    res = client.run_report(req)
    if not res.rows:
        return {"sessoes": 0, "usuarios": 0, "bounce_rate": 0, "engajamento_seg": 0}
    v = res.rows[0].metric_values
    return {
        "sessoes": int(v[0].value),
        "usuarios": int(v[1].value),
        "bounce_rate": round(float(v[2].value) * 100, 1),
        "engajamento_seg": round(float(v[3].value), 0),
    }


def _ga4_soma(a, b):
    """Combina 2 buckets de properties GA4 DISTINTAS (ex. Cxpress site+blog).
    bounce_rate reponderado por sessoes (nao dah pra so somar 2 percentuais)."""
    sessoes = a["sessoes"] + b["sessoes"]
    bounced_a = a["sessoes"] * a["bounce_rate"] / 100
    bounced_b = b["sessoes"] * b["bounce_rate"] / 100
    return {
        "sessoes": sessoes,
        "usuarios": a["usuarios"] + b["usuarios"],
        "bounce_rate": round((bounced_a + bounced_b) / sessoes * 100, 1) if sessoes else 0,
        "engajamento_seg": round(a["engajamento_seg"] + b["engajamento_seg"], 0),
    }


def _ga4_derivar_duracao_media(bucket):
    sessoes = bucket.get("sessoes", 0)
    seg = bucket.get("engajamento_seg", 0)
    bucket["duracao_media_seg"] = round(seg / sessoes, 0) if sessoes else 0
    return bucket


def get_ga4_data(creds, ctx_key, cfg):
    properties = cfg.get("ga4_properties")
    if not properties:
        return None
    print(f"📈 [{cfg['label']}] Coletando Google Analytics 4...")
    try:
        client = BetaAnalyticsDataClient(credentials=creds)

        if len(properties) == 1:
            # Site + blog no MESMO dominio/property -> filtro de path por bucket
            property_id = next(iter(properties.values()))
            buckets = {}
            for bucket in ("site", "blog", "total"):
                atual = _ga4_totais(client, property_id, inicio, fim, _ga4_bucket_filter(cfg, bucket))
                anterior = _ga4_totais(client, property_id, inicio_anterior, fim_anterior, _ga4_bucket_filter(cfg, bucket))
                atual["sessoes_anterior"] = anterior["sessoes"]
                atual["usuarios_anterior"] = anterior["usuarios"]
                buckets[bucket] = _ga4_derivar_duracao_media(atual)
            top_pages_filter = _ga4_bucket_filter(cfg, "blog")
        else:
            # Site e blog sao properties GA4 DISTINTAS (ex. Cxpress) -> soma pro "total"
            site_id, blog_id = properties["site"], properties["blog"]
            site_atual = _ga4_totais(client, site_id, inicio, fim)
            site_anterior = _ga4_totais(client, site_id, inicio_anterior, fim_anterior)
            blog_atual = _ga4_totais(client, blog_id, inicio, fim)
            blog_anterior = _ga4_totais(client, blog_id, inicio_anterior, fim_anterior)
            site_atual["sessoes_anterior"] = site_anterior["sessoes"]
            site_atual["usuarios_anterior"] = site_anterior["usuarios"]
            blog_atual["sessoes_anterior"] = blog_anterior["sessoes"]
            blog_atual["usuarios_anterior"] = blog_anterior["usuarios"]
            total_atual = _ga4_soma(site_atual, blog_atual)
            total_atual["sessoes_anterior"] = site_atual["sessoes_anterior"] + blog_atual["sessoes_anterior"]
            total_atual["usuarios_anterior"] = site_atual["usuarios_anterior"] + blog_atual["usuarios_anterior"]
            buckets = {
                "site": _ga4_derivar_duracao_media(site_atual),
                "blog": _ga4_derivar_duracao_media(blog_atual),
                "total": _ga4_derivar_duracao_media(total_atual),
            }
            property_id = blog_id  # top paginas/canais saem da property do blog
            top_pages_filter = None

        # Top páginas (dentro do bucket blog)
        req_pages = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[DateRange(start_date=inicio, end_date=fim)],
            dimensions=[Dimension(name="pagePath")],
            metrics=[Metric(name="sessions"), Metric(name="totalUsers"), Metric(name="bounceRate")],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
            dimension_filter=top_pages_filter,
            limit=25,
        )
        res_pages = client.run_report(req_pages)
        top_pages = [{
            "pagina": row.dimension_values[0].value,
            "sessoes": int(row.metric_values[0].value),
            "usuarios": int(row.metric_values[1].value),
            "bounce_rate": round(float(row.metric_values[2].value) * 100, 1),
        } for row in res_pages.rows]

        # Canais de tráfego (bucket "total": todo o dominio/contexto)
        canal_filter = _ga4_bucket_filter(cfg, "total") if len(properties) == 1 else None
        req_canais = RunReportRequest(
            property=f"properties/{property_id if len(properties) == 1 else site_id}",
            date_ranges=[DateRange(start_date=inicio, end_date=fim)],
            dimensions=[Dimension(name="sessionDefaultChannelGroup")],
            metrics=[Metric(name="sessions"), Metric(name="totalUsers")],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
            dimension_filter=canal_filter,
        )
        res_canais = client.run_report(req_canais)
        canais = [{
            "canal": row.dimension_values[0].value,
            "sessoes": int(row.metric_values[0].value),
            "usuarios": int(row.metric_values[1].value),
        } for row in res_canais.rows]

        print(f"   ✅ GA4 coletado ({cfg['label']})!")
        return {
            "site": buckets["site"],
            "blog": buckets["blog"],
            "total": buckets["total"],
            "top_paginas_blog": top_pages[:10],
            "canais": canais,
        }
    except Exception as e:
        print(f"   ⚠️  Erro no GA4 ({cfg['label']}): {e}")
        return {"erro": str(e)}


# ============================================================
# EXECUÇÃO
# ============================================================
if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print(f"📊 Gerando relatório SEO — {len(CONTEXTS)} contextos")
    print(f"   Diretório de trabalho: {BASE_DIR}")
    print(f"   Período: {inicio} a {fim}\n")

    print("🔐 Autenticando com sua conta Google...")
    creds = get_credentials()
    print("   ✅ Autenticado!\n")

    contexts_out = {}
    for ctx_key, cfg in CONTEXTS.items():
        contexts_out[ctx_key] = {
            "label": cfg["label"],
            "gsc": get_gsc_data(creds, ctx_key, cfg),
            "ga4": get_ga4_data(creds, ctx_key, cfg),
        }

    dados = {
        "gerado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "periodo": {"inicio": inicio, "fim": fim},
        "contexts": contexts_out,
        # As secoes "semrush" e "supabase" NAO sao coletadas aqui — a skill
        # /seo-report adiciona semrush via MCP e supabase via seo_report_conversoes.py.
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print("\n✅ Coleta Google concluída!")
    print(f"   Arquivo: {OUTPUT_JSON}")
    print("   A skill /seo-report lê este arquivo e busca Semrush (MCP) + Supabase.\n")
