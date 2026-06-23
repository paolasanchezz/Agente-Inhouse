"""
SEO Report - Buzzmonitor BR  |  coletor Google (GSC + GA4)

Coleta dados do Google Search Console e do Google Analytics 4 via OAuth2
(conta Google do proprio usuario). NAO coleta Semrush: a parte de Semrush
e feita pela skill /seo-report via MCP do Semrush (sem chave de API no repo).

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
  2. Rode: python seo_report_buzzmonitor.py
  3. No 1o uso abre o navegador para autorizar (login Google)
  4. Gera seo_data.json com as secoes gsc + ga4
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
    RunReportRequest, DateRange, Metric, Dimension, OrderBy
)

# ============================================================
# CONFIGURAÇÕES
# ============================================================
# Diretorio de trabalho por usuario (fora do repo). Nunca hardcodar caminho
# de maquina: usa SEO_REPORT_DIR se definido, senao ~/.seo-report-buzzmonitor.
BASE_DIR = Path(os.environ.get("SEO_REPORT_DIR", Path.home() / ".seo-report-buzzmonitor"))
BASE_DIR.mkdir(parents=True, exist_ok=True)

CLIENT_SECRETS_FILE = str(BASE_DIR / "client_secret.json")
TOKEN_FILE = str(BASE_DIR / "token.json")
OUTPUT_JSON = str(BASE_DIR / "seo_data.json")

GSC_SITE_URL = "sc-domain:buzzmonitor.com"   # propriedade de dominio no GSC
GA4_PROPERTY_ID = "347467970"                # Buzzmonitor BR

SCOPES = [
    "https://www.googleapis.com/auth/webmasters.readonly",
    "https://www.googleapis.com/auth/analytics.readonly",
]

# Período: últimos 28 dias vs 28 dias anteriores
hoje = datetime.today()
fim = (hoje - timedelta(days=1)).strftime("%Y-%m-%d")
inicio = (hoje - timedelta(days=28)).strftime("%Y-%m-%d")
fim_anterior = (hoje - timedelta(days=29)).strftime("%Y-%m-%d")
inicio_anterior = (hoje - timedelta(days=56)).strftime("%Y-%m-%d")

print(f"\n📊 Gerando relatório SEO — Buzzmonitor BR")
print(f"   Diretório de trabalho: {BASE_DIR}")
print(f"   Período: {inicio} a {fim}\n")


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
# 1. GOOGLE SEARCH CONSOLE
# ============================================================
def get_gsc_data(creds):
    print("🔍 Coletando dados do Google Search Console...")
    try:
        service = build("searchconsole", "v1", credentials=creds)

        # Totais período atual
        body_totais = {"startDate": inicio, "endDate": fim, "dimensions": []}
        res_totais = service.searchanalytics().query(siteUrl=GSC_SITE_URL, body=body_totais).execute()

        # Totais período anterior
        body_anterior = {"startDate": inicio_anterior, "endDate": fim_anterior, "dimensions": []}
        res_anterior = service.searchanalytics().query(siteUrl=GSC_SITE_URL, body=body_anterior).execute()

        totais_atual = res_totais.get("rows", [{}])[0] if res_totais.get("rows") else {}
        totais_anterior = res_anterior.get("rows", [{}])[0] if res_anterior.get("rows") else {}

        # Top páginas do blog
        body_pages = {
            "startDate": inicio, "endDate": fim,
            "dimensions": ["page"], "rowLimit": 25,
            "orderBy": [{"fieldName": "clicks", "sortOrder": "DESCENDING"}]
        }
        res_pages = service.searchanalytics().query(siteUrl=GSC_SITE_URL, body=body_pages).execute()
        top_pages = []
        for row in res_pages.get("rows", []):
            url = row["keys"][0]
            if "/blog/" in url:
                top_pages.append({
                    "url": url,
                    "cliques": int(row.get("clicks", 0)),
                    "impressoes": int(row.get("impressions", 0)),
                    "ctr": round(row.get("ctr", 0) * 100, 2),
                    "posicao": round(row.get("position", 0), 1)
                })

        # Top keywords
        body_kw = {
            "startDate": inicio, "endDate": fim,
            "dimensions": ["query"], "rowLimit": 20,
            "orderBy": [{"fieldName": "clicks", "sortOrder": "DESCENDING"}]
        }
        res_kw = service.searchanalytics().query(siteUrl=GSC_SITE_URL, body=body_kw).execute()
        top_keywords = []
        for row in res_kw.get("rows", []):
            top_keywords.append({
                "keyword": row["keys"][0],
                "cliques": int(row.get("clicks", 0)),
                "impressoes": int(row.get("impressions", 0)),
                "posicao": round(row.get("position", 0), 1)
            })

        print("   ✅ GSC coletado!")
        return {
            "totais": {
                "cliques": int(totais_atual.get("clicks", 0)),
                "impressoes": int(totais_atual.get("impressions", 0)),
                "ctr": round(totais_atual.get("ctr", 0) * 100, 2),
                "posicao_media": round(totais_atual.get("position", 0), 1),
            },
            "variacao": {
                "cliques_anterior": int(totais_anterior.get("clicks", 0)),
                "impressoes_anterior": int(totais_anterior.get("impressions", 0)),
            },
            "top_paginas_blog": top_pages[:10],
            "top_keywords": top_keywords[:15]
        }
    except Exception as e:
        print(f"   ⚠️  Erro no GSC: {e}")
        return {"erro": str(e)}


# ============================================================
# 2. GOOGLE ANALYTICS 4
# ============================================================
def get_ga4_data(creds):
    print("📈 Coletando dados do Google Analytics 4...")
    try:
        client = BetaAnalyticsDataClient(credentials=creds)
        property_id = f"properties/{GA4_PROPERTY_ID}"

        # Totais gerais
        req_geral = RunReportRequest(
            property=property_id,
            date_ranges=[
                DateRange(start_date=inicio, end_date=fim),
                DateRange(start_date=inicio_anterior, end_date=fim_anterior),
            ],
            metrics=[
                Metric(name="sessions"),
                Metric(name="totalUsers"),
                Metric(name="bounceRate"),
                Metric(name="averageSessionDuration"),
            ]
        )
        res_geral = client.run_report(req_geral)
        periodo_atual = res_geral.rows[0].metric_values if res_geral.rows else []
        periodo_anterior = res_geral.rows[1].metric_values if len(res_geral.rows) > 1 else []

        # Top páginas do blog
        req_blog = RunReportRequest(
            property=property_id,
            date_ranges=[DateRange(start_date=inicio, end_date=fim)],
            dimensions=[Dimension(name="pagePath")],
            metrics=[
                Metric(name="sessions"),
                Metric(name="totalUsers"),
                Metric(name="bounceRate"),
            ],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
            limit=25
        )
        res_blog = client.run_report(req_blog)
        top_pages_ga4 = []
        for row in res_blog.rows:
            path = row.dimension_values[0].value
            if "/blog/" in path:
                top_pages_ga4.append({
                    "pagina": path,
                    "sessoes": int(row.metric_values[0].value),
                    "usuarios": int(row.metric_values[1].value),
                    "bounce_rate": round(float(row.metric_values[2].value) * 100, 1)
                })

        # Canais de tráfego
        req_canais = RunReportRequest(
            property=property_id,
            date_ranges=[DateRange(start_date=inicio, end_date=fim)],
            dimensions=[Dimension(name="sessionDefaultChannelGroup")],
            metrics=[Metric(name="sessions"), Metric(name="totalUsers")],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        )
        res_canais = client.run_report(req_canais)
        canais = []
        for row in res_canais.rows:
            canais.append({
                "canal": row.dimension_values[0].value,
                "sessoes": int(row.metric_values[0].value),
                "usuarios": int(row.metric_values[1].value),
            })

        print("   ✅ GA4 coletado!")
        return {
            "totais": {
                "sessoes": int(periodo_atual[0].value) if periodo_atual else 0,
                "usuarios": int(periodo_atual[1].value) if periodo_atual else 0,
                "bounce_rate": round(float(periodo_atual[2].value) * 100, 1) if periodo_atual else 0,
                "duracao_media_seg": round(float(periodo_atual[3].value), 0) if periodo_atual else 0,
            },
            "variacao": {
                "sessoes_anterior": int(periodo_anterior[0].value) if periodo_anterior else 0,
                "usuarios_anterior": int(periodo_anterior[1].value) if periodo_anterior else 0,
            },
            "top_paginas_blog": top_pages_ga4[:10],
            "canais": canais
        }
    except Exception as e:
        print(f"   ⚠️  Erro no GA4: {e}")
        return {"erro": str(e)}


# ============================================================
# EXECUÇÃO
# ============================================================
if __name__ == "__main__":
    print("🔐 Autenticando com sua conta Google...")
    creds = get_credentials()
    print("   ✅ Autenticado!\n")

    dados = {
        "gerado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "periodo": {"inicio": inicio, "fim": fim},
        "gsc": get_gsc_data(creds),
        "ga4": get_ga4_data(creds),
        # A seção "semrush" NÃO é coletada aqui — a skill /seo-report adiciona
        # esses dados via MCP do Semrush (sem chave de API).
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print("\n✅ Coleta Google concluída!")
    print(f"   Arquivo: {OUTPUT_JSON}")
    print("   A skill /seo-report lê este arquivo e busca o Semrush via MCP.\n")
