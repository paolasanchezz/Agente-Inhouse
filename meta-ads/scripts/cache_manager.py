"""
cache_manager.py — Gerenciamento do banco SQLite local e mapeamento de contas.

SOMENTE LEITURA: este módulo nunca faz chamadas de escrita à Meta API.
Apenas gerencia o banco de dados local (SQLite).
"""

import os
import json
import time
import datetime
import sqlite3
from pathlib import Path
from functools import wraps
from dotenv import load_dotenv

# Carrega .env da raiz do projeto (um nível acima de meta-ads/)
ROOT_DIR = Path(__file__).parent.parent  # meta-ads/
load_dotenv(ROOT_DIR / ".env")

DB_PATH = Path(__file__).parent.parent / "data" / "meta_ads.db"
BENCHMARKS_PATH = Path(__file__).parent.parent / "data" / "benchmarks.json"

# ============================================================
# Rate limiting — centralizado aqui para evitar duplicação
# ============================================================

RATE_LIMIT_DELAY     = 1.0   # segundos entre chamadas individuais
BATCH_DELAY          = 3.0   # segundos após processar um lote
MAX_RETRIES          = 3
BACKOFF_BASE         = 60    # segundos — dobra a cada retry (60, 120, 240)
META_RATE_LIMIT_CODES = [17, 32, 613]


def retry_on_throttle(max_retries=MAX_RETRIES, backoff=BACKOFF_BASE):
    """
    Decorator: retry com backoff exponencial em caso de throttle da Meta API.
    Importar daqui — não duplicar em outros módulos.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                    time.sleep(RATE_LIMIT_DELAY)
                    return result
                except Exception as e:
                    code = getattr(e, "api_error_code", lambda: None)()
                    if code in META_RATE_LIMIT_CODES:
                        wait = backoff * (2 ** attempt)
                        print(f"[AVISO]  Throttle (código {code}). Tentativa {attempt+1}/{max_retries}. Aguardando {wait}s...")
                        time.sleep(wait)
                    else:
                        raise
            raise RuntimeError(f"Rate limit persistente após {max_retries} tentativas.")
        return wrapper
    return decorator

# ============================================================
# Mapa de contas
# ============================================================

ACCOUNTS = {
    "buzzmonitor_brl": {
        "label": "Buzzmonitor Brasil (BRL)",
        "currency": "BRL",
        "currency_symbol": "R$",
        "env_key": "META_ACCOUNT_BUZZMONITOR_BRL",
        "benchmark_group": "brl",
    },
    "buzzmonitor_usd": {
        "label": "Buzzmonitor Latam (USD)",
        "currency": "USD",
        "currency_symbol": "$",
        "env_key": "META_ACCOUNT_BUZZMONITOR_USD",
        "benchmark_group": "usd",
    },
    "buzzmonitor_eur": {
        "label": "Buzzmonitor Portugal (EUR)",
        "currency": "EUR",
        "currency_symbol": "€",
        "env_key": "META_ACCOUNT_BUZZMONITOR_EUR",
        "benchmark_group": "eur",
    },
    "cxpress_brl": {
        "label": "Cxpress Brasil (BRL)",
        "currency": "BRL",
        "currency_symbol": "R$",
        "env_key": "META_ACCOUNT_CXPRESS_BRL",
        "benchmark_group": "brl",
    },
    "cxpress_usd": {
        "label": "Cxpress Latam (USD)",
        "currency": "USD",
        "currency_symbol": "$",
        "env_key": "META_ACCOUNT_CXPRESS_USD",
        "benchmark_group": "usd",
    },
    "cxpress_eur": {
        "label": "Cxpress Portugal (EUR)",
        "currency": "EUR",
        "currency_symbol": "€",
        "env_key": "META_ACCOUNT_CXPRESS_EUR",
        "benchmark_group": "eur",
    },
}


def get_account_id(account_key: str) -> str:
    """Retorna o ID da conta (act_XXXXXXXXX) a partir da variável de ambiente."""
    account = ACCOUNTS.get(account_key)
    if not account:
        raise ValueError(f"Conta desconhecida: '{account_key}'. Válidas: {list(ACCOUNTS.keys())}")
    account_id = os.getenv(account["env_key"])
    if not account_id:
        raise EnvironmentError(
            f"Variável de ambiente '{account['env_key']}' não encontrada. "
            f"Configure o .env com o ID da conta {account['label']}."
        )
    return account_id


def check_token_expiry() -> None:
    """Alerta se o token expirar em menos de 10 dias."""
    created_at_str = os.getenv("META_TOKEN_CREATED_AT")
    if not created_at_str:
        print("[AVISO]  META_TOKEN_CREATED_AT não definido no .env — não é possível verificar expiração do token.")
        return
    try:
        created_at = datetime.date.fromisoformat(created_at_str)
        expires_at = created_at + datetime.timedelta(days=60)
        days_left = (expires_at - datetime.date.today()).days
        if days_left <= 0:
            raise RuntimeError(
                f"[ERRO] Token Meta Ads EXPIRADO em {expires_at}. "
                "Gere um novo token em Business Manager > Configurações > Tokens de acesso."
            )
        if days_left <= 10:
            print(f"[AVISO]  ATENÇÃO: Token Meta Ads expira em {days_left} dia(s) ({expires_at}). Renove em breve.")
    except ValueError:
        print(f"[AVISO]  META_TOKEN_CREATED_AT tem formato inválido: '{created_at_str}'. Use YYYY-MM-DD.")


# ============================================================
# Inferência de tipo de campanha por nome
# ============================================================

CAMPAIGN_TYPE_RULES = [
    # Ordem importa: mais específico primeiro
    {
        "keywords": ["buzztalk", "buzztalks", "presencial"],
        "type": "evento_presencial",
    },
    {
        "keywords": ["webinar", "aula", "evento", "workshop", "masterclass"],
        "type": "webinar",
    },
    {
        "keywords": [
            "ebook", "e-book", "material", "guia", "checklist", "playbook",
            "manual", "whitepaper", "planilha", "template", "kit", "rico",
        ],
        "type": "material_rico",
    },
    {
        "keywords": [
            "remarketing", "retargeting", "remarket", "rmkt", "rtg",
            "visitou", "carrinho", "abandono",
        ],
        "type": "remarketing",
    },
]


def infer_campaign_type(campaign_name: str) -> str:
    name_lower = campaign_name.lower()
    for rule in CAMPAIGN_TYPE_RULES:
        if any(kw in name_lower for kw in rule["keywords"]):
            return rule["type"]
    return "nao_classificada"


def get_funnel_group(campaign_type: str) -> str:
    if campaign_type in ["webinar", "material_rico", "evento_presencial"]:
        return "topo"
    if campaign_type == "remarketing":
        return "fundo"
    return "nao_classificado"


# ============================================================
# Banco de dados SQLite
# ============================================================

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS campaigns (
    id                TEXT PRIMARY KEY,
    account_key       TEXT NOT NULL,
    name              TEXT NOT NULL,
    objective         TEXT,
    status            TEXT,
    campaign_type     TEXT,
    funnel_group      TEXT,
    daily_budget      REAL,
    lifetime_budget   REAL,
    results_indicator TEXT,
    last_active_date  TEXT,
    fetched_at        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS adsets (
    id              TEXT PRIMARY KEY,
    campaign_id     TEXT NOT NULL,
    account_key     TEXT NOT NULL,
    name            TEXT NOT NULL,
    status          TEXT,
    optimization_goal TEXT,
    daily_budget    REAL,
    lifetime_budget REAL,
    fetched_at      TEXT NOT NULL,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);

CREATE TABLE IF NOT EXISTS ads (
    id              TEXT PRIMARY KEY,
    adset_id        TEXT NOT NULL,
    campaign_id     TEXT NOT NULL,
    account_key     TEXT NOT NULL,
    name            TEXT NOT NULL,
    status          TEXT,
    fetched_at      TEXT NOT NULL,
    FOREIGN KEY (adset_id) REFERENCES adsets(id)
);

CREATE TABLE IF NOT EXISTS insights (
    entity_type         TEXT NOT NULL,
    entity_id           TEXT NOT NULL,
    account_key         TEXT NOT NULL,
    date                TEXT NOT NULL,
    spend               REAL DEFAULT 0,
    impressions         INTEGER DEFAULT 0,
    reach               INTEGER DEFAULT 0,
    frequency           REAL DEFAULT 0,
    link_clicks         INTEGER DEFAULT 0,
    ctr_link            REAL DEFAULT 0,
    cpm                 REAL DEFAULT 0,
    cpc_link            REAL DEFAULT 0,
    leads               INTEGER DEFAULT 0,
    cost_per_lead       REAL DEFAULT 0,
    lp_conversion_rate  REAL DEFAULT 0,
    video_p25           REAL DEFAULT 0,
    video_p50           REAL DEFAULT 0,
    video_p75           REAL DEFAULT 0,
    video_p100          REAL DEFAULT 0,
    fetched_at          TEXT NOT NULL
);
"""

INDEXES_SQL = [
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_insights_pk ON insights(entity_id, entity_type, account_key, date)",
    "CREATE INDEX IF NOT EXISTS idx_insights_account_date ON insights(account_key, date)",
    "CREATE INDEX IF NOT EXISTS idx_insights_entity ON insights(entity_id, entity_type)",
    "CREATE INDEX IF NOT EXISTS idx_campaigns_account ON campaigns(account_key)",
    "CREATE INDEX IF NOT EXISTS idx_adsets_campaign ON adsets(campaign_id)",
    "CREATE INDEX IF NOT EXISTS idx_ads_adset ON ads(adset_id)",
]


def get_connection() -> sqlite3.Connection:
    """Retorna conexão SQLite com row_factory configurado."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def migrate_database() -> None:
    """Aplica migrações incrementais no banco existente. Idempotente."""
    conn = get_connection()
    migrations = [
        "ALTER TABLE adsets ADD COLUMN daily_budget REAL",
        "ALTER TABLE adsets ADD COLUMN lifetime_budget REAL",
        "ALTER TABLE campaigns ADD COLUMN results_indicator TEXT",
    ]
    with conn:
        for sql in migrations:
            try:
                conn.execute(sql)
            except Exception:
                pass  # Coluna já existe — ignorar
    conn.close()


def setup_database() -> None:
    """Cria tabelas e índices se não existirem. Idempotente."""
    conn = get_connection()
    with conn:
        conn.executescript(SCHEMA_SQL)
        for idx_sql in INDEXES_SQL:
            conn.execute(idx_sql)
    conn.close()
    migrate_database()
    print(f"[OK] Banco inicializado: {DB_PATH}")


# ============================================================
# Funções de escrita no banco
# ============================================================

def save_campaign(campaign: dict) -> None:
    conn = get_connection()
    now = datetime.datetime.utcnow().isoformat()
    with conn:
        conn.execute(
            """INSERT OR REPLACE INTO campaigns
               (id, account_key, name, objective, status, campaign_type, funnel_group,
                daily_budget, lifetime_budget, results_indicator, last_active_date, fetched_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                campaign["id"],
                campaign["account_key"],
                campaign["name"],
                campaign.get("objective"),
                campaign.get("status"),
                campaign.get("campaign_type", infer_campaign_type(campaign["name"])),
                campaign.get("funnel_group", get_funnel_group(infer_campaign_type(campaign["name"]))),
                campaign.get("daily_budget"),
                campaign.get("lifetime_budget"),
                campaign.get("results_indicator"),
                campaign.get("last_active_date"),
                now,
            ),
        )
    conn.close()


def update_campaign_indicator(campaign_id: str, indicator: str) -> None:
    """Atualiza o indicador de conversão primária da campanha."""
    conn = get_connection()
    with conn:
        conn.execute(
            "UPDATE campaigns SET results_indicator=? WHERE id=?",
            (indicator, campaign_id),
        )
    conn.close()


def get_campaign_indicators(account_key: str) -> dict:
    """Retorna {campaign_id: results_indicator} para todas as campanhas da conta."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, results_indicator FROM campaigns WHERE account_key=?",
        [account_key],
    ).fetchall()
    conn.close()
    return {r["id"]: r["results_indicator"] for r in rows}


def get_adset_campaign_map(account_key: str) -> dict:
    """Retorna {adset_id: campaign_id} para todos os adsets da conta."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, campaign_id FROM adsets WHERE account_key=?",
        [account_key],
    ).fetchall()
    conn.close()
    return {r["id"]: r["campaign_id"] for r in rows}


def get_ad_campaign_map(account_key: str) -> dict:
    """Retorna {ad_id: campaign_id} para todos os anúncios da conta."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, campaign_id FROM ads WHERE account_key=?",
        [account_key],
    ).fetchall()
    conn.close()
    return {r["id"]: r["campaign_id"] for r in rows}


def save_adset(adset: dict) -> None:
    conn = get_connection()
    now = datetime.datetime.utcnow().isoformat()
    with conn:
        conn.execute(
            """INSERT OR REPLACE INTO adsets
               (id, campaign_id, account_key, name, status, optimization_goal,
                daily_budget, lifetime_budget, fetched_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                adset["id"],
                adset["campaign_id"],
                adset["account_key"],
                adset["name"],
                adset.get("status"),
                adset.get("optimization_goal"),
                adset.get("daily_budget"),
                adset.get("lifetime_budget"),
                now,
            ),
        )
    conn.close()


def save_ad(ad: dict) -> None:
    conn = get_connection()
    now = datetime.datetime.utcnow().isoformat()
    with conn:
        conn.execute(
            """INSERT OR REPLACE INTO ads
               (id, adset_id, campaign_id, account_key, name, status, fetched_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                ad["id"],
                ad["adset_id"],
                ad["campaign_id"],
                ad["account_key"],
                ad["name"],
                ad.get("status"),
                now,
            ),
        )
    conn.close()


def save_insight(insight: dict) -> None:
    """Insere ou substitui linha de insight (unicidade por entity_id+type+account+date)."""
    conn = get_connection()
    now = datetime.datetime.utcnow().isoformat()
    with conn:
        conn.execute(
            """INSERT OR REPLACE INTO insights
               (entity_type, entity_id, account_key, date, spend, impressions, reach,
                frequency, link_clicks, ctr_link, cpm, cpc_link, leads, cost_per_lead,
                lp_conversion_rate, video_p25, video_p50, video_p75, video_p100, fetched_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                insight["entity_type"],
                insight["entity_id"],
                insight["account_key"],
                insight["date"],
                insight.get("spend", 0),
                insight.get("impressions", 0),
                insight.get("reach", 0),
                insight.get("frequency", 0),
                insight.get("link_clicks", 0),
                insight.get("ctr_link", 0),
                insight.get("cpm", 0),
                insight.get("cpc_link", 0),
                insight.get("leads", 0),
                insight.get("cost_per_lead", 0),
                insight.get("lp_conversion_rate", 0),
                insight.get("video_p25", 0),
                insight.get("video_p50", 0),
                insight.get("video_p75", 0),
                insight.get("video_p100", 0),
                now,
            ),
        )
    conn.close()


def update_campaign_last_active(campaign_id: str, date: str) -> None:
    """Atualiza last_active_date para evitar re-fetch de campanhas pausadas."""
    conn = get_connection()
    with conn:
        conn.execute(
            "UPDATE campaigns SET last_active_date=? WHERE id=?",
            (date, campaign_id),
        )
    conn.close()


# ============================================================
# Funções de leitura do banco
# ============================================================

def get_campaigns(account_key: str, active_only: bool = False) -> list:
    conn = get_connection()
    query = "SELECT * FROM campaigns WHERE account_key=?"
    params = [account_key]
    if active_only:
        query += " AND status='ACTIVE'"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_adsets(campaign_id: str) -> list:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM adsets WHERE campaign_id=?", [campaign_id]).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_ads(adset_id: str) -> list:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM ads WHERE adset_id=?", [adset_id]).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_insights(entity_id: str, entity_type: str, account_key: str,
                 date_start: str, date_end: str) -> list:
    conn = get_connection()
    rows = conn.execute(
        """SELECT * FROM insights
           WHERE entity_id=? AND entity_type=? AND account_key=?
           AND date >= ? AND date <= ?
           ORDER BY date""",
        [entity_id, entity_type, account_key, date_start, date_end],
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_existing_insight_dates(entity_id: str, entity_type: str, account_key: str) -> set:
    conn = get_connection()
    rows = conn.execute(
        "SELECT date FROM insights WHERE entity_id=? AND entity_type=? AND account_key=?",
        [entity_id, entity_type, account_key],
    ).fetchall()
    conn.close()
    return {r["date"] for r in rows}


# ============================================================
# Benchmarks
# ============================================================

_benchmarks_cache = None


def load_benchmarks() -> dict:
    global _benchmarks_cache
    if _benchmarks_cache is None:
        with open(BENCHMARKS_PATH, "r", encoding="utf-8") as f:
            _benchmarks_cache = json.load(f)
    return _benchmarks_cache


# ============================================================
# Métricas auxiliares
# ============================================================

def extract_leads(actions: list) -> int:
    if not actions:
        return 0
    lead_types = [
        "lead",
        "offsite_conversion.fb_pixel_lead",
        "onsite_conversion.lead_grouped",
    ]
    for action in actions:
        if action.get("action_type") in lead_types:
            return int(action.get("value", 0))
    return 0


def extract_cost_per_lead(cost_per_action: list) -> float:
    if not cost_per_action:
        return 0.0
    lead_types = ["lead", "offsite_conversion.fb_pixel_lead"]
    for item in cost_per_action:
        if item.get("action_type") in lead_types:
            return float(item.get("value", 0.0))
    return 0.0


def extract_primary_conversions(actions: list, indicator: str) -> int:
    """
    Extrai conversões usando o indicador primário configurado na campanha (results_indicator).
    Fallback para extract_leads() se indicator for None ou 'mixed'.

    indicator formato: "actions:offsite_conversion.custom.XXXXX" ou "actions:lead" etc.
    """
    if not indicator or indicator == "mixed":
        return extract_leads(actions)
    if not actions:
        return 0
    action_type = indicator.replace("actions:", "").strip()
    for action in actions:
        if action.get("action_type") == action_type:
            return int(action.get("value", 0))
    return 0


def extract_primary_cost(cost_per_action: list, indicator: str) -> float:
    """
    Extrai custo por conversão usando o indicador primário da campanha.
    Fallback para extract_cost_per_lead() se indicator for None ou 'mixed'.
    """
    if not indicator or indicator == "mixed":
        return extract_cost_per_lead(cost_per_action)
    if not cost_per_action:
        return 0.0
    action_type = indicator.replace("actions:", "").strip()
    for item in cost_per_action:
        if item.get("action_type") == action_type:
            return float(item.get("value", 0.0))
    return 0.0


def calc_lp_conversion_rate(leads: int, link_clicks: int) -> float:
    """Leads ÷ Cliques no Link × 100. Retorna 0.0 se não houver cliques."""
    if link_clicks == 0:
        return 0.0
    return round((leads / link_clicks) * 100, 2)


if __name__ == "__main__":
    setup_database()
