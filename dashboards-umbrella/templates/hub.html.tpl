<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>__TITULO__ · __ORG__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #F8FAFC;
    --surface: #FFFFFF;
    --border: #E5E7EB;
    --text: #0F172A;
    --text-muted: #475569;
    --text-subtle: #64748B;
    --shadow: 0 1px 2px rgba(15,23,42,.04), 0 1px 3px rgba(15,23,42,.05);
    --shadow-lift: 0 6px 16px rgba(15,23,42,.08), 0 2px 4px rgba(15,23,42,.04);
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html { overflow-x: hidden; }
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text);
    font-size: 16px;
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
    padding: 28px 20px 56px;
  }
  .wrap { max-width: 1320px; margin: 0 auto; }

  .head { margin: 12px 0 28px; }
  .head h1 { font-size: 30px; font-weight: 800; letter-spacing: -.025em; }
  .head p { margin-top: 6px; color: var(--text-muted); font-size: 15px; }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 16px;
  }

  .card {
    display: flex;
    flex-direction: column;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px 22px 18px;
    box-shadow: var(--shadow);
    text-decoration: none;
    color: inherit;
    position: relative;
    overflow: hidden;
    transition: box-shadow .15s ease, transform .15s ease, border-color .15s ease;
  }
  .card::before {
    content: '';
    position: absolute;
    inset: 0 auto 0 0;
    width: 3px;
    background: var(--accent);
  }
  .card:hover { box-shadow: var(--shadow-lift); transform: translateY(-2px); border-color: #D7DEE8; }
  .card:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

  .card h2 { font-size: 18px; font-weight: 700; letter-spacing: -.015em; }
  .card .resumo { margin-top: 8px; color: var(--text-muted); font-size: 14px; flex: 1; }

  .badges { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 14px; }
  .badge {
    font-size: 11px; font-weight: 600; letter-spacing: .02em;
    color: var(--text-muted); background: #F1F5F9;
    border-radius: 999px; padding: 4px 9px;
  }
  .badge.brand { color: var(--accent); background: var(--accent-soft); }

  .foot {
    margin-top: 16px; padding-top: 12px; border-top: 1px solid #F1F5F9;
    display: flex; align-items: center; justify-content: space-between; gap: 10px;
    font-size: 12px; color: var(--text-subtle);
  }
  .foot .seta { font-weight: 700; color: var(--accent); }

  .nota {
    margin-top: 28px; font-size: 13px; color: var(--text-subtle);
    border-top: 1px solid var(--border); padding-top: 16px;
  }
  .nota code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12px; }

  @media (max-width: 720px) {
    body { padding: 20px 14px 40px; }
    .head h1 { font-size: 24px; }
  }
</style>
</head>
<body>

<div class="wrap">
  <div class="head">
    <h1>__TITULO__</h1>
    <p>__ORG__ · Content Marketing. Todas atrás da mesma senha — troque de dashboard pela barra do topo.</p>
  </div>

  <div class="grid">
__CARDS__
  </div>

  <p class="nota">
    Uso interno, fora de buscadores. Os dados são exportados do Supabase e embutidos em cada dashboard —
    atualize com <code>/dashboard-atualizar</code>.
  </p>
</div>

<script defer src="/nav.js"></script>
</body>
</html>
