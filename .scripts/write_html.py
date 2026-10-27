import json

with open('ipl_matches.csv', 'r', encoding='utf-8') as f:
    matches_csv = f.read()

with open('ipl_player_stats.csv', 'r', encoding='utf-8') as f:
    players_csv = f.read()

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>IPL Cricket Data Analysis &amp; Machine Learning Studio</title>
<meta name="description" content="Interactive IPL Cricket Data Analysis &amp; Machine Learning Dashboard with real-time value filters, predictive models, and statistical inferences."/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Oswald:wght@500;600;700&display=swap" rel="stylesheet"/>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
<style>
:root {{
  --bg: #070a13;
  --bg-card: rgba(255, 255, 255, 0.045);
  --bg-card-hover: rgba(255, 255, 255, 0.08);
  --gold: #f5a623;
  --gold-glow: rgba(245, 166, 35, 0.35);
  --blue: #3b82f6;
  --green: #22c55e;
  --red: #ef4444;
  --purple: #a855f7;
  --cyan: #06b6d4;
  --pink: #ec4899;
  --t1: #f8fafc;
  --t2: #94a3b8;
  --t3: #64748b;
  --brd: rgba(255, 255, 255, 0.09);
  --r: 16px;
  --sh: 0 16px 40px rgba(0, 0, 0, 0.55);
}}
*,*::before,*::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; }}
body {{
  font-family: 'Inter', sans-serif;
  background: var(--bg);
  color: var(--t1);
  min-height: 100vh;
  overflow-x: hidden;
}}
body::before {{
  content: '';
  position: fixed;
  inset: 0;
  z-index: -1;
  background:
    radial-gradient(ellipse 65% 50% at 15% 15%, rgba(245,166,35,0.07) 0%, transparent 60%),
    radial-gradient(ellipse 55% 55% at 85% 75%, rgba(59,130,246,0.07) 0%, transparent 60%),
    radial-gradient(ellipse 45% 45% at 50% 50%, rgba(168,85,247,0.04) 0%, transparent 70%);
}}

/* Top Nav Tabs */
.top-nav {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 32px;
  border-bottom: 1px solid var(--brd);
  background: rgba(10, 14, 26, 0.88);
  backdrop-filter: blur(12px);
  position: sticky;
  top: 0;
  z-index: 100;
}}
.nav-brand {{
  display: flex;
  align-items: center;
  gap: 12px;
  font-family: 'Oswald', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.5px;
}}
.nav-brand .icon-ball {{
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, var(--gold), #ea580c);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  box-shadow: 0 0 16px var(--gold-glow);
}}
.nav-tabs {{
  display: flex;
  gap: 6px;
  background: rgba(255,255,255,0.03);
  padding: 4px;
  border-radius: 40px;
  border: 1px solid var(--brd);
  flex-wrap: wrap;
}}
.nav-tab {{
  padding: 8px 18px;
  border-radius: 30px;
  font-size: 12.5px;
  font-weight: 600;
  border: none;
  background: transparent;
  color: var(--t2);
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}}
.nav-tab:hover {{ color: var(--t1); background: rgba(255,255,255,0.05); }}
.nav-tab.active {{
  background: linear-gradient(135deg, var(--gold), #e87c00);
  color: #000;
  font-weight: 700;
  box-shadow: 0 0 18px var(--gold-glow);
}}
.live-badge {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 700;
  color: var(--green);
  text-transform: uppercase;
  letter-spacing: 1px;
}}
.pulse-dot {{
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--green);
  box-shadow: 0 0 8px var(--green);
  animation: pulse 1.5s infinite;
}}
@keyframes pulse {{
  0%, 100% {{ transform: scale(1); opacity: 1; }}
  50% {{ transform: scale(1.4); opacity: 0.5; }}
}}

/* Hero Header */
.hero {{
  padding: 36px 24px 18px;
  text-align: center;
}}
.hero-badge {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(245,166,35,0.12);
  border: 1px solid rgba(245,166,35,0.3);
  border-radius: 40px;
  padding: 5px 18px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: var(--gold);
  text-transform: uppercase;
  margin-bottom: 14px;
}}
.hero h1 {{
  font-family: 'Oswald', sans-serif;
  font-size: clamp(32px, 5.2vw, 60px);
  font-weight: 700;
  line-height: 1.1;
  background: linear-gradient(135deg, #f5a623 0%, #ffffff 50%, #3b82f6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}
.hero p {{
  margin-top: 10px;
  font-size: 14.5px;
  color: var(--t2);
  max-width: 650px;
  margin-inline: auto;
  line-height: 1.5;
}}

/* Filter Bar */
.filter-bar {{
  max-width: 1360px;
  margin: 16px auto 0;
  padding: 0 24px;
}}
.filter-card {{
  background: var(--bg-card);
  border: 1px solid var(--brd);
  border-radius: var(--r);
  padding: 20px 24px;
  box-shadow: var(--sh);
}}
.filter-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}}
.filter-title {{
  font-size: 12.5px;
  font-weight: 700;
  color: var(--gold);
  text-transform: uppercase;
  letter-spacing: 1.2px;
  display: flex;
  align-items: center;
  gap: 8px;
}}
.preset-group {{
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}}
.preset-btn {{
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--brd);
  color: var(--t2);
  cursor: pointer;
  transition: all 0.2s;
}}
.preset-btn:hover {{ background: rgba(255,255,255,0.09); color: var(--t1); }}
.filter-row {{
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  align-items: flex-end;
}}
.filter-group {{
  display: flex;
  flex-direction: column;
  gap: 8px;
}}
.filter-label {{
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.9px;
  color: var(--t2);
}}
.pills-group {{
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}}
.pill {{
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid var(--brd);
  background: rgba(255,255,255,0.02);
  color: var(--t2);
  cursor: pointer;
  transition: all 0.2s ease;
}}
.pill:hover {{ color: var(--t1); border-color: rgba(255,255,255,0.2); }}
.pill.active {{
  background: var(--gold);
  color: #000;
  font-weight: 700;
  border-color: var(--gold);
  box-shadow: 0 0 12px rgba(245,166,35,0.3);
}}
.team-pill {{
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  border: 1px solid var(--brd);
  background: rgba(255,255,255,0.02);
  color: var(--t2);
  cursor: pointer;
  transition: all 0.2s;
}}
.team-pill.active {{
  border-color: var(--blue);
  color: #fff;
  background: rgba(59,130,246,0.2);
  box-shadow: 0 0 12px rgba(59,130,246,0.25);
}}
.filter-select {{
  background: #0d1120;
  border: 1px solid var(--brd);
  border-radius: 10px;
  color: var(--t1);
  padding: 8px 14px;
  font-size: 13px;
  font-family: inherit;
  cursor: pointer;
  outline: none;
}}
.filter-select:focus {{ border-color: var(--gold); }}
.slider-wrap {{
  display: flex;
  align-items: center;
  gap: 10px;
}}
.range-slider {{
  accent-color: var(--gold);
  cursor: pointer;
}}
.reset-btn {{
  padding: 8px 18px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--gold), #ea580c);
  color: #000;
  font-weight: 700;
  font-size: 12px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}}
.reset-btn:hover {{ transform: translateY(-1px); opacity: 0.9; }}

/* Main container */
.main {{
  max-width: 1360px;
  margin: 0 auto;
  padding: 24px 24px 80px;
}}

/* KPI Grid */
.kpi-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}}
.kpi {{
  background: var(--bg-card);
  border: 1px solid var(--brd);
  border-radius: var(--r);
  padding: 18px 14px;
  text-align: center;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}}
.kpi::before {{
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--kc, var(--gold)), transparent);
}}
.kpi:hover {{
  background: var(--bg-card-hover);
  transform: translateY(-2px);
  box-shadow: var(--sh);
}}
.kpi-icon {{ font-size: 22px; margin-bottom: 6px; }}
.kpi-val {{
  font-family: 'Oswald', sans-serif;
  font-size: 30px;
  font-weight: 700;
  color: var(--kc, var(--gold));
  line-height: 1;
}}
.kpi-lbl {{
  font-size: 10.5px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--t3);
  margin-top: 6px;
}}

/* Summary Pill Row */
.summary-pills {{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 28px;
}}
.sum-pill {{
  background: var(--bg-card);
  border: 1px solid var(--brd);
  border-radius: 40px;
  padding: 8px 18px;
  font-size: 12px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--t2);
}}
.sum-pill strong {{ color: var(--gold); font-size: 13px; }}

/* Section headers */
.sec-title {{
  font-family: 'Oswald', sans-serif;
  font-size: 22px;
  font-weight: 600;
  color: var(--t1);
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 32px 0 16px;
}}
.sec-title::after {{
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, var(--gold), transparent);
}}
.dot {{ width: 9px; height: 9px; border-radius: 50%; }}

/* Grids */
.grid-2 {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(520px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}}
.grid-3 {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}}
.card {{
  background: var(--bg-card);
  border: 1px solid var(--brd);
  border-radius: var(--r);
  overflow: hidden;
  transition: all 0.3s;
}}
.card:hover {{
  transform: translateY(-2px);
  box-shadow: var(--sh);
  border-color: rgba(245,166,35,0.2);
}}
.card-head {{
  padding: 14px 18px;
  border-bottom: 1px solid var(--brd);
  display: flex;
  align-items: center;
  gap: 10px;
}}
.card-title {{ font-size: 13.5px; font-weight: 600; }}
.card-sub {{ font-size: 11px; color: var(--t3); margin-left: auto; }}
.card-body {{ padding: 16px 18px; }}
.chart-wrap {{ position: relative; height: 280px; }}
.chart-wrap-tall {{ position: relative; height: 340px; }}

/* Tables */
.tbl-wrap {{
  overflow-x: auto;
  border-radius: var(--r);
  border: 1px solid var(--brd);
  background: var(--bg-card);
}}
table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 12.5px;
}}
thead {{ background: rgba(245,166,35,0.06); }}
th {{
  padding: 11px 14px;
  text-align: left;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--gold);
  border-bottom: 1px solid var(--brd);
  white-space: nowrap;
  cursor: pointer;
  user-select: none;
}}
th:hover {{ color: #fff; }}
th.asc::after {{ content: ' ↑'; }}
th.desc::after {{ content: ' ↓'; }}
td {{
  padding: 9px 14px;
  color: var(--t2);
  border-bottom: 1px solid rgba(255,255,255,0.03);
}}
tr:last-child td {{ border-bottom: none; }}
tr:hover td {{ background: rgba(255,255,255,0.03); color: var(--t1); }}
td:first-child {{ color: var(--t1); font-weight: 600; }}
.badge-r {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  font-size: 10.5px;
  font-weight: 700;
  background: rgba(255,255,255,0.05);
  color: var(--t3);
}}
.r1 {{ background: linear-gradient(135deg, #f5a623, #ea580c); color: #000; }}
.r2 {{ background: rgba(148,163,184,0.25); color: #cbd5e1; }}
.r3 {{ background: rgba(217,119,6,0.25); color: #f59e0b; }}
.bar-cell {{ display: flex; align-items: center; gap: 8px; }}
.mini-bar {{
  height: 5px;
  border-radius: 3px;
  background: linear-gradient(90deg, var(--gold), #ea580c);
  min-width: 4px;
  transition: width 0.4s;
}}
.pct-text {{ font-size: 11px; white-space: nowrap; }}
.search-wrap {{ margin-bottom: 12px; }}
.search-input {{
  width: 100%;
  background: #0d1120;
  border: 1px solid var(--brd);
  border-radius: 8px;
  color: var(--t1);
  padding: 8px 14px;
  font-size: 12.5px;
  font-family: inherit;
  outline: none;
  transition: border-color 0.2s;
}}
.search-input:focus {{ border-color: var(--blue); }}

/* Insights grid */
.insight-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
  margin-bottom: 30px;
}}
.insight {{
  background: var(--bg-card);
  border: 1px solid var(--brd);
  border-radius: var(--r);
  padding: 20px;
  position: relative;
  transition: all 0.3s;
}}
.insight:hover {{
  transform: translateY(-2px);
  box-shadow: var(--sh);
  border-color: var(--kc, var(--gold));
}}
.insight-em {{ font-size: 26px; margin-bottom: 8px; }}
.insight-ttl {{ font-size: 13.5px; font-weight: 700; color: var(--kc, var(--gold)); margin-bottom: 5px; }}
.insight-txt {{ font-size: 12px; color: var(--t2); line-height: 1.55; }}

/* Gallery View */
.gallery-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
  gap: 22px;
}}
.gallery-card {{
  background: var(--bg-card);
  border: 1px solid var(--brd);
  border-radius: var(--r);
  overflow: hidden;
  transition: all 0.3s;
}}
.gallery-card:hover {{
  transform: translateY(-3px);
  box-shadow: var(--sh);
  border-color: rgba(245,166,35,0.25);
}}
.gallery-card img {{
  width: 100%;
  height: auto;
  display: block;
  border-bottom: 1px solid var(--brd);
  background: #0d1120;
}}
.gallery-info {{ padding: 16px 20px; }}
.gallery-title {{ font-size: 14px; font-weight: 700; color: var(--t1); margin-bottom: 4px; }}
.gallery-desc {{ font-size: 12px; color: var(--t2); line-height: 1.5; }}

/* ML Studio View */
.ml-pred-box {{
  background: linear-gradient(135deg, rgba(59,130,246,0.08), rgba(245,166,35,0.08));
  border: 1px solid rgba(245,166,35,0.3);
  border-radius: var(--r);
  padding: 24px 28px;
  margin-bottom: 30px;
  box-shadow: var(--sh);
}}
.ml-form-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-top: 16px;
  align-items: flex-end;
}}
.pred-btn {{
  padding: 10px 24px;
  background: linear-gradient(135deg, var(--gold), #ea580c);
  color: #000;
  font-weight: 700;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
  height: 40px;
}}
.pred-btn:hover {{ transform: translateY(-1px); box-shadow: 0 0 16px var(--gold-glow); }}
.pred-result-card {{
  margin-top: 20px;
  padding: 16px 20px;
  background: rgba(13,17,32,0.9);
  border: 1px solid var(--brd);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}}
.meter-wrap {{
  flex: 1;
  min-width: 200px;
  height: 12px;
  background: rgba(255,255,255,0.08);
  border-radius: 6px;
  overflow: hidden;
  position: relative;
}}
.meter-fill {{
  height: 100%;
  background: linear-gradient(90deg, var(--gold), var(--blue));
  border-radius: 6px;
  transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}}

/* Data Explorer View */
.exp-controls {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}}
.exp-tabs {{ display: flex; gap: 8px; }}
.exp-tab-btn {{
  padding: 7px 16px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid var(--brd);
  background: rgba(255,255,255,0.03);
  color: var(--t2);
  cursor: pointer;
}}
.exp-tab-btn.active {{
  background: var(--blue);
  color: #fff;
  border-color: var(--blue);
}}
.exp-pagination {{ display: flex; align-items: center; gap: 8px; }}
.page-btn {{
  padding: 6px 12px;
  border-radius: 6px;
  background: rgba(255,255,255,0.05);
  border: 1px solid var(--brd);
  color: var(--t1);
  cursor: pointer;
  font-size: 12px;
}}
.page-btn:disabled {{ opacity: 0.3; cursor: not-allowed; }}

/* Footer */
footer {{
  text-align: center;
  padding: 36px 24px;
  border-top: 1px solid var(--brd);
  color: var(--t3);
  font-size: 12px;
  margin-top: 40px;
}}
footer strong {{ color: var(--gold); }}
footer a {{ color: var(--gold); text-decoration: none; }}

/* Loading Overlay */
#loading {{
  position: fixed;
  inset: 0;
  background: var(--bg);
  z-index: 9999;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
}}
.loader {{
  width: 44px;
  height: 44px;
  border: 3px solid rgba(245,166,35,0.2);
  border-top-color: var(--gold);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}
#load-msg {{ color: var(--t2); font-size: 13px; font-weight: 500; }}

@media(max-width: 640px) {{
  .grid-2, .grid-3, .gallery-grid {{ grid-template-columns: 1fr; }}
  .top-nav {{ flex-direction: column; gap: 12px; align-items: stretch; }}
  .filter-row {{ flex-direction: column; align-items: stretch; }}
}}
</style>
</head>
<body>

<div id="loading">
  <div class="loader"></div>
  <p id="load-msg">Initializing IPL Analytics &amp; ML Studio...</p>
</div>

<!-- TOP NAV -->
<nav class="top-nav">
  <div class="nav-brand">
    <div class="icon-ball">&#127953;</div>
    <span>IPL Cricket Analytics &amp; ML</span>
  </div>
  <div class="nav-tabs">
    <button class="nav-tab active" onclick="switchView('interactive', this)">&#9889; Interactive Studio</button>
    <button class="nav-tab" onclick="switchView('ml', this)">&#129302; ML Studio (IML)</button>
    <button class="nav-tab" onclick="switchView('gallery', this)">&#128202; Deep-Dive Charts</button>
    <button class="nav-tab" onclick="switchView('explorer', this)">&#128196; Data Explorer</button>
  </div>
  <div class="live-badge"><span class="pulse-dot"></span>Live Studio</div>
</nav>

<!-- HERO -->
<header class="hero">
  <div class="hero-badge">&#127942; Seasons 2020 &ndash; 2024 &middot; 300 Matches &middot; 6,600 Player Innings &middot; Supervised ML</div>
  <h1>Interactive IPL Analytics &amp; Machine Learning</h1>
  <p>Perform live value filtering, run real-time match predictions with trained ML models, and explore cross-validated benchmarks.</p>
</header>

<!-- VIEW 1: INTERACTIVE STUDIO -->
<div id="view-interactive">
  <!-- FILTER BAR -->
  <div class="filter-bar">
    <div class="filter-card">
      <div class="filter-header">
        <div class="filter-title">&#128065; Value-Changeable Controls</div>
        <div class="preset-group">
          <span style="font-size:11px;color:var(--t3);align-self:center">Quick Presets:</span>
          <button class="preset-btn" onclick="applyPreset('all')">All Seasons</button>
          <button class="preset-btn" onclick="applyPreset('recent')">Recent (2023-24)</button>
          <button class="preset-btn" onclick="applyPreset('chase')">Field First</button>
          <button class="preset-btn" onclick="applyPreset('rcb')">RCB Focus</button>
          <button class="preset-btn" onclick="applyPreset('mi')">MI Focus</button>
        </div>
      </div>
      <div class="filter-row">
        <!-- Seasons -->
        <div class="filter-group">
          <div class="filter-label">&#128197; Season Multi-Select</div>
          <div class="pills-group" id="season-pills"></div>
        </div>
        <!-- Toss -->
        <div class="filter-group">
          <div class="filter-label">&#129689; Toss Decision</div>
          <select class="filter-select" id="toss-filter">
            <option value="all">All Match Decisions</option>
            <option value="bat">Bat First Only</option>
            <option value="field">Field First (Chasing)</option>
          </select>
        </div>
        <!-- Min Innings Slider -->
        <div class="filter-group" style="min-width: 190px;">
          <div class="filter-label">&#128100; Min Player Innings</div>
          <div class="slider-wrap">
            <input type="range" id="min-innings" min="1" max="25" value="1" class="range-slider" style="flex:1"/>
            <span id="innings-val" style="font-size:11px;color:var(--gold);font-weight:700">Min 1</span>
          </div>
        </div>
        <!-- Reset -->
        <div style="margin-left:auto; display:flex; gap:10px; align-items:center">
          <button class="reset-btn" onclick="resetFilters()">&#8635; Reset Filters</button>
        </div>
      </div>
      <!-- Teams Chips -->
      <div style="margin-top: 16px; padding-top: 14px; border-top: 1px solid var(--brd)">
        <div class="filter-label" style="margin-bottom: 8px;">&#127942; Filter Teams (Toggle to include/exclude)</div>
        <div class="pills-group" id="team-pills"></div>
      </div>
    </div>
  </div>

  <!-- MAIN DASHBOARD CONTENT -->
  <main class="main">
    <!-- KPIS -->
    <div class="kpi-grid">
      <div class="kpi" style="--kc:var(--gold)"><div class="kpi-icon">&#127953;</div><div class="kpi-val" id="kpi-matches">—</div><div class="kpi-lbl">Matches Filtered</div></div>
      <div class="kpi" style="--kc:var(--blue)"><div class="kpi-icon">&#127942;</div><div class="kpi-val" id="kpi-teams">—</div><div class="kpi-lbl">Active Teams</div></div>
      <div class="kpi" style="--kc:var(--green)"><div class="kpi-icon">4&#65039;&#8419;</div><div class="kpi-val" id="kpi-fours">—</div><div class="kpi-lbl">Fours Smashed</div></div>
      <div class="kpi" style="--kc:var(--red)"><div class="kpi-icon">6&#65039;&#8419;</div><div class="kpi-val" id="kpi-sixes">—</div><div class="kpi-lbl">Sixes Cleared</div></div>
      <div class="kpi" style="--kc:var(--purple)"><div class="kpi-icon">&#127919;</div><div class="kpi-val" id="kpi-wickets">—</div><div class="kpi-lbl">Total Wickets</div></div>
      <div class="kpi" style="--kc:var(--cyan)"><div class="kpi-icon">&#128200;</div><div class="kpi-val" id="kpi-avg-score">—</div><div class="kpi-lbl">Avg 1st Inn Score</div></div>
      <div class="kpi" style="--kc:var(--pink)"><div class="kpi-icon">&#129689;</div><div class="kpi-val" id="kpi-toss-rate">—</div><div class="kpi-lbl">Toss Win %</div></div>
      <div class="kpi" style="--kc:var(--gold)"><div class="kpi-icon">&#127949;</div><div class="kpi-val" id="kpi-venues">—</div><div class="kpi-lbl">Host Stadiums</div></div>
    </div>

    <!-- SUMMARY HIGHLIGHTS -->
    <div class="summary-pills" id="sum-pills"></div>

    <!-- SECTION 1: TEAM ANALYTICS -->
    <div class="sec-title"><span class="dot" style="background:var(--gold)"></span>Team Performance &amp; Season Trends</div>
    <div class="grid-2">
      <div class="card">
        <div class="card-head"><span class="dot" style="background:var(--gold)"></span><span class="card-title">Team Win Percentage</span><span class="card-sub" id="sub-team-chart">Live</span></div>
        <div class="card-body"><div class="chart-wrap"><canvas id="chart-team-win"></canvas></div></div>
      </div>
      <div class="card">
        <div class="card-head"><span class="dot" style="background:var(--blue)"></span><span class="card-title">Season-wise Wins Trajectory</span><span class="card-sub">Top Contenders</span></div>
        <div class="card-body"><div class="chart-wrap"><canvas id="chart-season-wins"></canvas></div></div>
      </div>
    </div>

    <!-- STANDINGS TABLE -->
    <div class="tbl-wrap" style="margin-bottom:30px">
      <table id="team-table">
        <thead>
          <tr>
            <th onclick="sortTable('team-table',0)">#</th>
            <th onclick="sortTable('team-table',1)">Franchise</th>
            <th onclick="sortTable('team-table',2)">Matches</th>
            <th onclick="sortTable('team-table',3)">Won</th>
            <th onclick="sortTable('team-table',4)">Lost</th>
            <th onclick="sortTable('team-table',5)">Win %</th>
            <th>Win Ratio Bar</th>
          </tr>
        </thead>
        <tbody id="team-tbody"></tbody>
      </table>
    </div>

    <!-- SECTION 2: PLAYER ANALYTICS -->
    <div class="sec-title"><span class="dot" style="background:var(--green)"></span>Player Performance (Batting &amp; Bowling)</div>
    <div class="grid-2">
      <div class="card">
        <div class="card-head"><span class="dot" style="background:var(--gold)"></span><span class="card-title">Top Run Scorers</span><span class="card-sub" id="sub-batting">Top 10</span></div>
        <div class="card-body"><div class="chart-wrap-tall"><canvas id="chart-batting"></canvas></div></div>
      </div>
      <div class="card">
        <div class="card-head"><span class="dot" style="background:var(--green)"></span><span class="card-title">Top Wicket Takers</span><span class="card-sub" id="sub-bowling">Top 10</span></div>
        <div class="card-body"><div class="chart-wrap-tall"><canvas id="chart-bowling"></canvas></div></div>
      </div>
    </div>

    <!-- PLAYER LEADERBOARDS -->
    <div class="grid-2" style="margin-bottom:30px">
      <div>
        <div class="sec-title" style="margin-top:0"><span class="dot" style="background:var(--gold)"></span>Batters Leaderboard</div>
        <div class="search-wrap"><input class="search-input" id="bat-search" placeholder="&#128269; Search player by name..." oninput="filterTable('bat-search','bat-tbody')"/></div>
        <div class="tbl-wrap">
          <table id="bat-table">
            <thead><tr>
              <th onclick="sortTable('bat-table',0)">#</th>
              <th onclick="sortTable('bat-table',1)">Player</th>
              <th onclick="sortTable('bat-table',2)">Runs</th>
              <th onclick="sortTable('bat-table',3)">Inns</th>
              <th onclick="sortTable('bat-table',4)">SR</th>
              <th onclick="sortTable('bat-table',5)">4s</th>
              <th onclick="sortTable('bat-table',6)">6s</th>
            </tr></thead>
            <tbody id="bat-tbody"></tbody>
          </table>
        </div>
      </div>
      <div>
        <div class="sec-title" style="margin-top:0"><span class="dot" style="background:var(--green)"></span>Bowlers Leaderboard</div>
        <div class="search-wrap"><input class="search-input" id="bowl-search" placeholder="&#128269; Search bowler by name..." oninput="filterTable('bowl-search','bowl-tbody')"/></div>
        <div class="tbl-wrap">
          <table id="bowl-table">
            <thead><tr>
              <th onclick="sortTable('bowl-table',0)">#</th>
              <th onclick="sortTable('bowl-table',1)">Player</th>
              <th onclick="sortTable('bowl-table',2)">Wkts</th>
              <th onclick="sortTable('bowl-table',3)">Overs</th>
              <th onclick="sortTable('bowl-table',4)">Econ</th>
              <th onclick="sortTable('bowl-table',5)">Runs Conc.</th>
            </tr></thead>
            <tbody id="bowl-tbody"></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- SECTION 3: TOSS, VENUES & BOUNDARIES -->
    <div class="sec-title"><span class="dot" style="background:var(--pink)"></span>Toss Impact, Margins &amp; Venue Dynamics</div>
    <div class="grid-3">
      <div class="card">
        <div class="card-head"><span class="dot" style="background:var(--pink)"></span><span class="card-title">Bat vs Field Win Rate</span></div>
        <div class="card-body"><div class="chart-wrap"><canvas id="chart-toss"></canvas></div></div>
      </div>
      <div class="card">
        <div class="card-head"><span class="dot" style="background:var(--cyan)"></span><span class="card-title">Toss Decision Ratio</span></div>
        <div class="card-body"><div class="chart-wrap"><canvas id="chart-toss-split"></canvas></div></div>
      </div>
      <div class="card">
        <div class="card-head"><span class="dot" style="background:var(--red)"></span><span class="card-title">Run Margin Spread</span></div>
        <div class="card-body"><div class="chart-wrap"><canvas id="chart-margins"></canvas></div></div>
      </div>
    </div>

    <div class="grid-2" style="margin-bottom:30px">
      <div class="card">
        <div class="card-head"><span class="dot" style="background:var(--blue)"></span><span class="card-title">Average 1st Innings Score by Venue</span></div>
        <div class="card-body"><div class="chart-wrap-tall"><canvas id="chart-venue"></canvas></div></div>
      </div>
      <div class="card">
        <div class="card-head"><span class="dot" style="background:var(--purple)"></span><span class="card-title">Boundary Count by Season (4s vs 6s)</span></div>
        <div class="card-body"><div class="chart-wrap-tall"><canvas id="chart-boundaries"></canvas></div></div>
      </div>
    </div>

    <!-- SECTION 4: DYNAMIC INSIGHTS -->
    <div class="sec-title"><span class="dot" style="background:var(--gold)"></span>Dynamic Statistical Findings</div>
    <div class="insight-grid" id="insights-grid"></div>
  </main>
</div>

<!-- VIEW 2: MACHINE LEARNING STUDIO (IML) -->
<div id="view-ml" style="display:none; max-width:1360px; margin:0 auto; padding:24px 24px 80px">
  <div style="background:rgba(59,130,246,0.06); border:1px solid rgba(59,130,246,0.25); border-radius:var(--r); padding:20px 24px; margin-bottom:28px">
    <h3 style="font-family:'Oswald',sans-serif; color:var(--blue); font-size:22px; margin-bottom:6px">&#129302; Introduction to Machine Learning (IML) Pipeline</h3>
    <p style="font-size:13px; color:var(--t2); line-height:1.6">
      Trained with <strong>scikit-learn</strong> on 300 IPL matches (80% training / 20% testing split with 5-Fold Stratified Cross-Validation). Includes Supervised Classification (Match Winner Prediction), Supervised Regression (1st Innings Total Score), and Feature Importance interpretability.
    </p>
  </div>

  <!-- INTERACTIVE PREDICTOR WIDGET -->
  <div class="ml-pred-box">
    <div style="font-family:'Oswald',sans-serif; font-size:20px; color:var(--gold); display:flex; align-items:center; gap:8px">
      <span>&#128262; Real-Time Match Winner &amp; Score Predictor</span>
    </div>
    <p style="font-size:12.5px; color:var(--t2); margin-top:4px">Select match parameters to compute estimated win probabilities and score projections:</p>

    <div class="ml-form-grid">
      <div class="filter-group">
        <label class="filter-label">&#127942; Team 1 (Batting 1st)</label>
        <select class="filter-select" id="pred-team1">
          <option value="Royal Challengers Bengaluru">RCB</option>
          <option value="Mumbai Indians" selected>Mumbai Indians</option>
          <option value="Chennai Super Kings">CSK</option>
          <option value="Kolkata Knight Riders">KKR</option>
          <option value="Rajasthan Royals">Rajasthan Royals</option>
          <option value="Punjab Kings">Punjab Kings</option>
          <option value="Delhi Capitals">Delhi Capitals</option>
          <option value="Sunrisers Hyderabad">Sunrisers Hyderabad</option>
        </select>
      </div>
      <div class="filter-group">
        <label class="filter-label">&#127942; Team 2 (Chasing)</label>
        <select class="filter-select" id="pred-team2">
          <option value="Royal Challengers Bengaluru" selected>RCB</option>
          <option value="Mumbai Indians">Mumbai Indians</option>
          <option value="Chennai Super Kings">CSK</option>
          <option value="Kolkata Knight Riders">KKR</option>
          <option value="Rajasthan Royals">Rajasthan Royals</option>
          <option value="Punjab Kings">Punjab Kings</option>
          <option value="Delhi Capitals">Delhi Capitals</option>
          <option value="Sunrisers Hyderabad">Sunrisers Hyderabad</option>
        </select>
      </div>
      <div class="filter-group">
        <label class="filter-label">&#127949; Venue / Stadium</label>
        <select class="filter-select" id="pred-venue">
          <option value="Wankhede Stadium">Wankhede Stadium (Mumbai)</option>
          <option value="M. Chinnaswamy Stadium">M. Chinnaswamy (Bengaluru)</option>
          <option value="M. A. Chidambaram Stadium">M. A. Chidambaram (Chennai)</option>
          <option value="Eden Gardens">Eden Gardens (Kolkata)</option>
          <option value="Sawai Mansingh Stadium">Sawai Mansingh (Jaipur)</option>
          <option value="Arun Jaitley Stadium">Arun Jaitley (Delhi)</option>
          <option value="Rajiv Gandhi Intl Stadium">Rajiv Gandhi (Hyderabad)</option>
          <option value="Narendra Modi Stadium">Narendra Modi (Ahmedabad)</option>
        </select>
      </div>
      <div class="filter-group">
        <label class="filter-label">&#129689; Toss Winner</label>
        <select class="filter-select" id="pred-toss-winner">
          <option value="team1">Team 1 Won Toss</option>
          <option value="team2">Team 2 Won Toss</option>
        </select>
      </div>
      <div class="filter-group">
        <label class="filter-label">&#9878;&#65039; Toss Decision</label>
        <select class="filter-select" id="pred-toss-dec">
          <option value="field">Field First (Chase)</option>
          <option value="bat">Bat First</option>
        </select>
      </div>
      <div>
        <button class="pred-btn" onclick="runMLPrediction()">&#9889; Predict Outcome</button>
      </div>
    </div>

    <!-- PREDICTION RESULTS -->
    <div class="pred-result-card" id="pred-result-card">
      <div>
        <div style="font-size:11px; text-transform:uppercase; letter-spacing:1px; color:var(--t3)">Predicted Match Winner</div>
        <div id="pred-winner-text" style="font-family:'Oswald',sans-serif; font-size:24px; font-weight:700; color:var(--gold); margin-top:2px">
          Mumbai Indians (54.2% Probability)
        </div>
        <div id="pred-score-text" style="font-size:12px; color:var(--t2); margin-top:4px">
          Estimated 1st Innings Target: <strong>167 runs</strong>
        </div>
      </div>
      <div style="min-width:280px; flex:1; max-width:400px">
        <div style="display:flex; justify-content:space-between; font-size:11px; color:var(--t2); margin-bottom:4px">
          <span id="meter-t1-lbl">Team 1: 54%</span>
          <span id="meter-t2-lbl">Team 2: 46%</span>
        </div>
        <div class="meter-wrap">
          <div class="meter-fill" id="pred-meter-fill" style="width:54%"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- CLASSIFICATION BENCHMARKS TABLE -->
  <div class="sec-title"><span class="dot" style="background:var(--blue)"></span>1. Supervised Classification Benchmark (Match Winner)</div>
  <div class="tbl-wrap" style="margin-bottom:28px">
    <table>
      <thead>
        <tr>
          <th>Classification Algorithm</th>
          <th>5-Fold CV Accuracy</th>
          <th>Test Accuracy</th>
          <th>Precision</th>
          <th>Recall</th>
          <th>F1-Score</th>
          <th>ROC-AUC</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Gradient Boosting Classifier</strong></td>
          <td>47.5% (±4.8%)</td>
          <td><strong style="color:var(--green)">53.3%</strong></td>
          <td>55.6%</td>
          <td>48.4%</td>
          <td><strong>51.7%</strong></td>
          <td><strong>0.50</strong></td>
        </tr>
        <tr>
          <td><strong>Logistic Regression (Baseline)</strong></td>
          <td>49.2% (±2.1%)</td>
          <td><strong>51.7%</strong></td>
          <td>53.3%</td>
          <td>51.6%</td>
          <td><strong>52.5%</strong></td>
          <td><strong>0.50</strong></td>
        </tr>
        <tr>
          <td><strong>Random Forest Classifier</strong></td>
          <td>45.4% (±2.4%)</td>
          <td>48.3%</td>
          <td>50.0%</td>
          <td>48.4%</td>
          <td>49.2%</td>
          <td>0.45</td>
        </tr>
        <tr>
          <td><strong>Decision Tree Classifier</strong></td>
          <td><strong style="color:var(--gold)">49.6% (±4.6%)</strong></td>
          <td>46.7%</td>
          <td>48.7%</td>
          <td>61.3%</td>
          <td><strong>54.3%</strong></td>
          <td><strong>0.51</strong></td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- CLASSIFICATION CHARTS -->
  <div class="grid-3" style="margin-bottom:32px">
    <div class="card">
      <div class="card-head"><span class="dot" style="background:var(--blue)"></span><span class="card-title">Model Benchmarks</span></div>
      <div class="card-body"><img src="ml_models_comparison.png" alt="ML Models Comparison" style="width:100%; border-radius:8px"/></div>
    </div>
    <div class="card">
      <div class="card-head"><span class="dot" style="background:var(--gold)"></span><span class="card-title">Confusion Matrix (Random Forest)</span></div>
      <div class="card-body"><img src="ml_confusion_matrix.png" alt="Confusion Matrix" style="width:100%; border-radius:8px"/></div>
    </div>
    <div class="card">
      <div class="card-head"><span class="dot" style="background:var(--purple)"></span><span class="card-title">ROC Curves (Test Set)</span></div>
      <div class="card-body"><img src="ml_roc_curve.png" alt="ROC Curves" style="width:100%; border-radius:8px"/></div>
    </div>
  </div>

  <!-- REGRESSION BENCHMARKS TABLE & CHART -->
  <div class="sec-title"><span class="dot" style="background:var(--purple)"></span>2. Supervised Regression Benchmark (1st Innings Total)</div>
  <div class="grid-2" style="margin-bottom:32px">
    <div>
      <div class="tbl-wrap">
        <table>
          <thead>
            <tr>
              <th>Regression Algorithm</th>
              <th>5-Fold CV RMSE</th>
              <th>Test MAE (runs)</th>
              <th>Test RMSE (runs)</th>
              <th>Test R²</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Ridge Regression (L2)</strong></td>
              <td><strong style="color:var(--green)">25.12 runs</strong></td>
              <td><strong>22.13 runs</strong></td>
              <td><strong>27.59 runs</strong></td>
              <td><strong>-0.077</strong></td>
            </tr>
            <tr>
              <td><strong>Linear Regression</strong></td>
              <td>25.39 runs</td>
              <td>22.22 runs</td>
              <td>27.67 runs</td>
              <td>-0.084</td>
            </tr>
            <tr>
              <td><strong>Random Forest Regressor</strong></td>
              <td>25.97 runs</td>
              <td>23.55 runs</td>
              <td>28.37 runs</td>
              <td>-0.139</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div style="margin-top:16px; padding:16px; background:var(--bg-card); border:1px solid var(--brd); border-radius:var(--r); font-size:12.5px; color:var(--t2); line-height:1.6">
        <strong style="color:var(--gold)">Regression Insights:</strong> Predicting exact T20 match scores pre-match incurs an average error of ~22 runs (MAE). This aligns with cricket dynamics where weather, pitch deterioration, and individual power-hitting explosions introduce high situational variance.
      </div>
    </div>
    <div class="card">
      <div class="card-head"><span class="dot" style="background:var(--purple)"></span><span class="card-title">Actual vs Predicted Scores (Ridge Regression)</span></div>
      <div class="card-body"><img src="ml_regression_actual_vs_pred.png" alt="Regression Actual vs Predicted" style="width:100%; border-radius:8px"/></div>
    </div>
  </div>

  <!-- FEATURE IMPORTANCE -->
  <div class="sec-title"><span class="dot" style="background:var(--green)"></span>3. Model Interpretability &amp; Feature Importance (IML)</div>
  <div class="grid-2">
    <div class="card">
      <div class="card-head"><span class="dot" style="background:var(--green)"></span><span class="card-title">Gini Feature Importance (Random Forest)</span></div>
      <div class="card-body"><img src="ml_feature_importance.png" alt="Feature Importance" style="width:100%; border-radius:8px"/></div>
    </div>
    <div style="display:flex; flex-direction:column; gap:12px; justify-content:center">
      <div class="insight" style="--kc:var(--blue)">
        <div class="insight-ttl">🥇 Win Percentage Differential (0.238 Importance)</div>
        <div class="insight-txt">The historical relative strength differential between Team 1 and Team 2 accounts for nearly 24% of all tree splits in the Random Forest ensemble.</div>
      </div>
      <div class="insight" style="--kc:var(--gold)">
        <div class="insight-ttl">🥈 Fielding First Advantage (0.070 Importance)</div>
        <div class="insight-txt">Opting to bowl first after winning the toss is the second highest single predictor, conferring a chasing advantage.</div>
      </div>
      <div class="insight" style="--kc:var(--purple)">
        <div class="insight-ttl">🥉 Stadium Dynamics (Wankhede &amp; Hyderabad)</div>
        <div class="insight-txt">Pitch-specific boundary dimensions and surface bounce notably alter the probabilities of winning when defending totals.</div>
      </div>
    </div>
  </div>
</div>

<!-- VIEW 3: STATIC DEEP-DIVE CHARTS GALLERY -->
<div id="view-gallery" style="display:none; max-width:1360px; margin:0 auto; padding:24px 24px 80px">
  <div style="background:rgba(245,166,35,0.06); border:1px solid rgba(245,166,35,0.2); border-radius:var(--r); padding:20px 24px; margin-bottom:28px">
    <h3 style="font-family:'Oswald',sans-serif; color:var(--gold); font-size:20px; margin-bottom:6px">&#128202; Publication-Quality Python Matplotlib Visualizations</h3>
    <p style="font-size:13px; color:var(--t2); line-height:1.6">
      Generated automatically by <code>generate_charts.py</code> across the full 5-season dataset. Includes rigorous statistical hypothesis testing, Chi-Square independence analysis, and venue scoring breakdowns.
    </p>
  </div>

  <div class="gallery-grid">
    <div class="gallery-card">
      <img src="chart_1_team_win_pct.png" alt="Team Win %" loading="lazy"/>
      <div class="gallery-info">
        <div class="gallery-title">1. Overall Franchise Win Percentages</div>
        <div class="gallery-desc">Royal Challengers Bengaluru leads all franchises with a 54.7% win rate, followed by Punjab Kings (53.4%) and Rajasthan Royals (51.9%).</div>
      </div>
    </div>
    <div class="gallery-card">
      <img src="chart_2_season_wins_trend.png" alt="Season Wins Trend" loading="lazy"/>
      <div class="gallery-info">
        <div class="gallery-title">2. Top 3 Teams Season-wise Wins Trend</div>
        <div class="gallery-desc">Tracks consistency and fluctuations across 2020-2024 for the top 3 highest win-percentage franchises.</div>
      </div>
    </div>
    <div class="gallery-card">
      <img src="chart_3_top_run_scorers.png" alt="Top Run Scorers" loading="lazy"/>
      <div class="gallery-info">
        <div class="gallery-title">3. Top 10 All-Time Run Scorers</div>
        <div class="gallery-desc">Mumbai_Player2 leads the run charts with 2,166 runs at a strike rate of 138.9, followed closely by Mumbai_Player7 (1,998 runs).</div>
      </div>
    </div>
    <div class="gallery-card">
      <img src="chart_4_top_wicket_takers.png" alt="Top Wicket Takers" loading="lazy"/>
      <div class="gallery-info">
        <div class="gallery-title">4. Top 10 All-Time Wicket Takers</div>
        <div class="gallery-desc">Mumbai_Player5 leads with 52 wickets (econ 8.50), with Mumbai_Player11 second at 51 wickets and Chennai_Player8 third with 47 wickets.</div>
      </div>
    </div>
    <div class="gallery-card">
      <img src="chart_5_toss_decision_winrate.png" alt="Toss Decision Win Rate" loading="lazy"/>
      <div class="gallery-info">
        <div class="gallery-title">5. Toss Decision Impact: Bat vs Field</div>
        <div class="gallery-desc">Fielding first offers a 56.6% win rate vs 46.3% for batting first. However, Chi-Square test (chi2=2.35, p=0.125) reveals toss winner advantage is not statistically significant at alpha=0.05.</div>
      </div>
    </div>
    <div class="gallery-card">
      <img src="chart_6_win_margin_runs.png" alt="Win Margin Distribution" loading="lazy"/>
      <div class="gallery-info">
        <div class="gallery-title">6. Victory Margin Distribution (Runs)</div>
        <div class="gallery-desc">Mean margin of victory by runs is 18.3 runs, indicating predominantly close, competitive encounters across all seasons.</div>
      </div>
    </div>
    <div class="gallery-card">
      <img src="chart_7_venue_scores.png" alt="Venue Scores" loading="lazy"/>
      <div class="gallery-info">
        <div class="gallery-title">7. Average 1st Innings Score by Stadium</div>
        <div class="gallery-desc">Sawai Mansingh Stadium leads in high scores with 172.0 average runs, followed by Wankhede Stadium at 168.0 and Arun Jaitley Stadium at 166.8.</div>
      </div>
    </div>
    <div class="gallery-card">
      <img src="chart_8_potm.png" alt="Player of the Match" loading="lazy"/>
      <div class="gallery-info">
        <div class="gallery-title">8. Top Player of the Match Recipients</div>
        <div class="gallery-desc">Mumbai_Player8 and Punjab_Player4 lead the tournament with 8 POTM awards each across 2020-2024.</div>
      </div>
    </div>
    <div class="gallery-card">
      <img src="chart_9_season_boundaries.png" alt="Season Boundaries" loading="lazy"/>
      <div class="gallery-info">
        <div class="gallery-title">9. Fours vs Sixes Per Season</div>
        <div class="gallery-desc">Total tournament boundaries: 13,925 fours and 8,560 sixes recorded across the 300 matches.</div>
      </div>
    </div>
  </div>
</div>

<!-- VIEW 4: DATA EXPLORER -->
<div id="view-explorer" style="display:none; max-width:1360px; margin:0 auto; padding:24px 24px 80px">
  <div class="exp-controls">
    <div class="exp-tabs">
      <button class="exp-tab-btn active" id="tab-exp-matches" onclick="setExplorerTab('matches')">&#127953; Matches Dataset (300 records)</button>
      <button class="exp-tab-btn" id="tab-exp-players" onclick="setExplorerTab('players')">&#128100; Player Stats Dataset (6,600 records)</button>
    </div>
    <div style="display:flex; gap:10px; align-items:center">
      <input class="search-input" id="exp-search" placeholder="&#128269; Filter records in real time..." style="width:260px" oninput="renderExplorer()"/>
      <div class="exp-pagination">
        <button class="page-btn" id="btn-prev" onclick="changeExpPage(-1)">&#9664; Prev</button>
        <span id="page-num" style="font-size:12px; color:var(--t2)">Page 1</span>
        <button class="page-btn" id="btn-next" onclick="changeExpPage(1)">Next &#9654;</button>
      </div>
    </div>
  </div>

  <div class="tbl-wrap">
    <table id="exp-table">
      <thead id="exp-thead"></thead>
      <tbody id="exp-tbody"></tbody>
    </table>
  </div>
</div>

<!-- FOOTER -->
<footer>
  <p>&#127953; <strong>IPL Cricket Data Analysis &amp; Machine Learning Studio</strong> &middot; Comprehensive IML Pipeline</p>
  <p style="margin-top:6px">Powered by <strong>scikit-learn</strong>, <strong>Chart.js</strong>, <strong>PapaParse</strong> &amp; <strong>Matplotlib</strong> &middot; Responsive, Accessible &amp; Zero-CORS Architecture</p>
</footer>

<!-- EMBEDDED CSV DATA (ZERO CORS RISK) -->
<script id="csv-matches" type="text/csv">
{matches_csv}
</script>

<script id="csv-players" type="text/csv">
{players_csv}
</script>

<!-- JAVASCRIPT ENGINE -->
<script>
// ─────────────────────────────────────────────
// STATE & CONFIG
// ─────────────────────────────────────────────
let allMatches = [], allPlayers = [];
let charts = {{}};
let filters = {{
  seasons: new Set(),
  teams: new Set(),
  toss: 'all',
  minInnings: 1
}};

let expMode = 'matches';
let expPage = 1;
const EXP_PAGE_SIZE = 25;

const TEAM_WIN_PCTS = {{
  'Royal Challengers Bengaluru': 54.7,
  'Punjab Kings': 53.4,
  'Rajasthan Royals': 51.9,
  'Mumbai Indians': 50.6,
  'Chennai Super Kings': 48.0,
  'Kolkata Knight Riders': 47.7,
  'Delhi Capitals': 47.2,
  'Sunrisers Hyderabad': 46.2
}};

const VENUE_AVG_SCORES = {{
  'Sawai Mansingh Stadium': 172.0,
  'Wankhede Stadium': 168.0,
  'Arun Jaitley Stadium': 166.8,
  'M. A. Chidambaram Stadium': 164.9,
  'Eden Gardens': 164.3,
  'M. Chinnaswamy Stadium': 163.7,
  'Rajiv Gandhi Intl Stadium': 162.3,
  'Narendra Modi Stadium': 161.2
}};

const TEAM_COLORS = {{
  'Royal Challengers Bengaluru': '#e74c3c',
  'Punjab Kings': '#ec4899',
  'Rajasthan Royals': '#3b82f6',
  'Mumbai Indians': '#06b6d4',
  'Chennai Super Kings': '#f5a623',
  'Kolkata Knight Riders': '#a855f7',
  'Delhi Capitals': '#6366f1',
  'Sunrisers Hyderabad': '#f97316'
}};

const CHART_DEFAULTS = {{
  color: 'rgba(255,255,255,.6)',
  plugins: {{
    legend: {{ labels: {{ color: 'rgba(255,255,255,.75)', font: {{ size: 11, family: "'Inter',sans-serif" }} }} }}
  }},
  scales: {{
    x: {{ ticks: {{ color: 'rgba(255,255,255,.55)', font: {{ size: 11 }} }}, grid: {{ color: 'rgba(255,255,255,.05)' }} }},
    y: {{ ticks: {{ color: 'rgba(255,255,255,.55)', font: {{ size: 11 }} }}, grid: {{ color: 'rgba(255,255,255,.06)' }} }}
  }}
}};

// ─────────────────────────────────────────────
// DATA LOADING
// ─────────────────────────────────────────────
function loadData() {{
  try {{
    const mEl = document.getElementById('csv-matches');
    const pEl = document.getElementById('csv-players');
    if (mEl && pEl && mEl.textContent.trim().length > 50) {{
      allMatches = Papa.parse(mEl.textContent.trim(), {{ header: true, dynamicTyping: true, skipEmptyLines: true }}).data;
      allPlayers = Papa.parse(pEl.textContent.trim(), {{ header: true, dynamicTyping: true, skipEmptyLines: true }}).data;
      document.getElementById('loading').style.display = 'none';
      init();
      return;
    }}
  }} catch(e) {{
    console.warn('Embedded parse error:', e);
  }}

  // Fallback to fetch
  let loaded = 0;
  const done = () => {{ if (++loaded === 2) {{ document.getElementById('loading').style.display = 'none'; init(); }} }};
  Papa.parse('ipl_matches.csv', {{
    header: true, dynamicTyping: true, skipEmptyLines: true, download: true,
    complete: r => {{ allMatches = r.data; done(); }},
    error: () => {{ document.getElementById('load-msg').textContent = 'Error reading ipl_matches.csv'; }}
  }});
  Papa.parse('ipl_player_stats.csv', {{
    header: true, dynamicTyping: true, skipEmptyLines: true, download: true,
    complete: r => {{ allPlayers = r.data; done(); }},
    error: () => {{ document.getElementById('load-msg').textContent = 'Error reading ipl_player_stats.csv'; }}
  }});
}}

// ─────────────────────────────────────────────
// INITIALIZATION
// ─────────────────────────────────────────────
function init() {{
  const seasons = [...new Set(allMatches.map(m => m.season))].filter(Boolean).sort();
  const teams = [...new Set([...allMatches.map(m => m.team1), ...allMatches.map(m => m.team2)])].filter(Boolean).sort();

  // Populate seasons
  const sContainer = document.getElementById('season-pills');
  sContainer.innerHTML = '';
  seasons.forEach(s => {{
    filters.seasons.add(s);
    const pill = document.createElement('button');
    pill.className = 'pill active';
    pill.textContent = s;
    pill.onclick = () => {{
      if (filters.seasons.has(s)) {{
        if (filters.seasons.size > 1) {{ filters.seasons.delete(s); pill.classList.remove('active'); }}
      }} else {{
        filters.seasons.add(s);
        pill.classList.add('active');
      }}
      render();
    }};
    sContainer.appendChild(pill);
  }});

  // Populate teams
  const tContainer = document.getElementById('team-pills');
  tContainer.innerHTML = '';
  teams.forEach(t => {{
    filters.teams.add(t);
    const pill = document.createElement('button');
    pill.className = 'team-pill active';
    pill.textContent = t.replace('Royal Challengers Bengaluru','RCB').replace('Mumbai Indians','MI').replace('Chennai Super Kings','CSK').replace('Kolkata Knight Riders','KKR').replace('Delhi Capitals','DC').replace('Rajasthan Royals','RR').replace('Punjab Kings','PBKS').replace('Sunrisers Hyderabad','SRH');
    pill.title = t;
    pill.onclick = () => {{
      if (filters.teams.has(t)) {{
        if (filters.teams.size > 1) {{ filters.teams.delete(t); pill.classList.remove('active'); }}
      }} else {{
        filters.teams.add(t);
        pill.classList.add('active');
      }}
      render();
    }};
    tContainer.appendChild(pill);
  }});

  // Toss filter
  document.getElementById('toss-filter').onchange = e => {{
    filters.toss = e.target.value;
    render();
  }};

  // Slider
  const slider = document.getElementById('min-innings');
  slider.oninput = e => {{
    filters.minInnings = +e.target.value;
    document.getElementById('innings-val').textContent = `Min ${{e.target.value}}`;
    render();
  }};

  render();
  renderExplorer();
  runMLPrediction();
}}

// ─────────────────────────────────────────────
// PRESETS
// ─────────────────────────────────────────────
function applyPreset(preset) {{
  const allSeasons = [...new Set(allMatches.map(m => m.season))].filter(Boolean).sort();
  const allTeams = [...new Set([...allMatches.map(m => m.team1), ...allMatches.map(m => m.team2)])].filter(Boolean);

  if (preset === 'all') {{
    filters.seasons = new Set(allSeasons);
    filters.teams = new Set(allTeams);
    filters.toss = 'all';
  }} else if (preset === 'recent') {{
    filters.seasons = new Set([2023, 2024]);
    filters.teams = new Set(allTeams);
    filters.toss = 'all';
  }} else if (preset === 'chase') {{
    filters.seasons = new Set(allSeasons);
    filters.teams = new Set(allTeams);
    filters.toss = 'field';
  }} else if (preset === 'rcb') {{
    filters.seasons = new Set(allSeasons);
    filters.teams = new Set(['Royal Challengers Bengaluru']);
    filters.toss = 'all';
  }} else if (preset === 'mi') {{
    filters.seasons = new Set(allSeasons);
    filters.teams = new Set(['Mumbai Indians']);
    filters.toss = 'all';
  }}

  syncFilterUI();
  render();
}}

function resetFilters() {{
  applyPreset('all');
  document.getElementById('min-innings').value = 1;
  filters.minInnings = 1;
  document.getElementById('innings-val').textContent = 'Min 1';
  render();
}}

function syncFilterUI() {{
  document.querySelectorAll('#season-pills .pill').forEach(p => {{
    p.classList.toggle('active', filters.seasons.has(+p.textContent || p.textContent));
  }});
  document.querySelectorAll('#team-pills .team-pill').forEach(p => {{
    p.classList.toggle('active', filters.teams.has(p.title));
  }});
  document.getElementById('toss-filter').value = filters.toss;
}}

// ─────────────────────────────────────────────
// MASTER FILTER & RENDER
// ─────────────────────────────────────────────
function filteredMatches() {{
  return allMatches.filter(m => {{
    if (!filters.seasons.has(m.season)) return false;
    const teamOk = filters.teams.size === 0 || filters.teams.has(m.team1) || filters.teams.has(m.team2);
    if (!teamOk) return false;
    if (filters.toss !== 'all' && m.toss_decision !== filters.toss) return false;
    return true;
  }});
}}

function filteredPlayers(matchIds) {{
  const ids = new Set(matchIds);
  return allPlayers.filter(p => ids.has(p.match_id) && (filters.teams.size === 0 || filters.teams.has(p.team)));
}}

function render() {{
  const fm = filteredMatches();
  const matchIds = fm.map(m => m.match_id);
  const fp = filteredPlayers(matchIds);

  updateKPIs(fm, fp);
  updateSummaryPills(fm, fp);
  updateTeamChart(fm);
  updateSeasonWins(fm);
  updateTeamTable(fm);
  updateBattingChart(fp);
  updateBowlingChart(fp);
  updateBatTable(fp);
  updateBowlTable(fp);
  updateTossCharts(fm);
  updateVenueChart(fm);
  updateBoundaries(fp, fm);
  updateInsights(fm, fp);
}}

// ─────────────────────────────────────────────
// KPIS
// ─────────────────────────────────────────────
function updateKPIs(fm, fp) {{
  const matches = fm.length;
  const teams = new Set([...fm.map(m => m.team1), ...fm.map(m => m.team2)].filter(t => filters.teams.has(t))).size;
  const fours = fp.reduce((a, p) => a + (+p.fours || 0), 0);
  const sixes = fp.reduce((a, p) => a + (+p.sixes || 0), 0);
  const wickets = fp.reduce((a, p) => a + (+p.wickets_taken || 0), 0);
  const scores = fm.map(m => +m.team1_score).filter(s => s > 0);
  const avgScore = scores.length ? (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(1) : '—';
  const tossWins = fm.filter(m => m.toss_winner === m.winner).length;
  const tossRate = matches ? ((tossWins / matches) * 100).toFixed(1) + '%' : '—';
  const venues = new Set(fm.map(m => m.venue)).size;

  animKPI('kpi-matches', matches);
  animKPI('kpi-teams', teams, false);
  animKPI('kpi-fours', fours);
  animKPI('kpi-sixes', sixes);
  animKPI('kpi-wickets', wickets);
  document.getElementById('kpi-avg-score').textContent = avgScore;
  document.getElementById('kpi-toss-rate').textContent = tossRate;
  animKPI('kpi-venues', venues, false);
}}

function animKPI(id, target, comma=true) {{
  const el = document.getElementById(id);
  if (!el) return;
  const start = +(el.textContent.replace(/,/g, '')) || 0;
  const dur = 400, steps = 20;
  let i = 0;
  const iv = setInterval(() => {{
    i++;
    const v = Math.round(start + (target - start) * (i / steps));
    el.textContent = comma ? v.toLocaleString() : v;
    if (i >= steps) {{
      el.textContent = comma ? target.toLocaleString() : target;
      clearInterval(iv);
    }}
  }}, dur / steps);
}}

// ─────────────────────────────────────────────
// SUMMARY PILLS
// ─────────────────────────────────────────────
function updateSummaryPills(fm, fp) {{
  const batting = groupBy(fp, 'player');
  let topBatter = '—', topRuns = 0, topBowler = '—', topWkts = 0;
  Object.entries(batting).forEach(([p, rows]) => {{
    const r = rows.reduce((a, x) => a + (+x.runs_scored || 0), 0);
    const w = rows.reduce((a, x) => a + (+x.wickets_taken || 0), 0);
    if (r > topRuns) {{ topRuns = r; topBatter = p; }}
    if (w > topWkts) {{ topWkts = w; topBowler = p; }}
  }});
  const topTeam = getTopTeam(fm);
  const el = document.getElementById('sum-pills');
  el.innerHTML = `
    <div class="sum-pill">&#127953; Leading Batter: <strong>${{topBatter}}</strong> (${{topRuns.toLocaleString()}} runs)</div>
    <div class="sum-pill">&#127919; Leading Bowler: <strong>${{topBowler}}</strong> (${{topWkts}} wickets)</div>
    <div class="sum-pill">&#127942; Best Franchise: <strong>${{topTeam.name}}</strong> (${{topTeam.pct}}% win rate)</div>
    <div class="sum-pill">&#127903;&#65039; Filtered Matches: <strong>${{fm.length}}</strong> of ${{allMatches.length}}</div>
  `;
}}

function getTopTeam(fm) {{
  const teams = {{}};
  fm.forEach(m => {{
    [m.team1, m.team2].forEach(t => {{
      if (filters.teams.has(t)) {{
        if (!teams[t]) teams[t] = {{ p: 0, w: 0 }};
        teams[t].p++;
      }}
    }});
    if (m.winner && filters.teams.has(m.winner) && teams[m.winner]) {{
      teams[m.winner].w++;
    }}
  }});
  let best = {{ name: '—', pct: 0 }};
  Object.entries(teams).forEach(([t, s]) => {{
    const pct = s.p ? +((s.w / s.p) * 100).toFixed(1) : 0;
    if (pct > best.pct) best = {{ name: t, pct }};
  }});
  return best;
}}

// ─────────────────────────────────────────────
// TEAM WIN CHART
// ─────────────────────────────────────────────
function updateTeamChart(fm) {{
  const teams = {{}};
  fm.forEach(m => {{
    [m.team1, m.team2].forEach(t => {{
      if (!teams[t]) teams[t] = {{ p: 0, w: 0 }};
      teams[t].p++;
    }});
    if (m.winner && teams[m.winner]) teams[m.winner].w++;
  }});
  const data = Object.entries(teams)
    .map(([t, s]) => ({{ t, pct: s.p ? +((s.w / s.p) * 100).toFixed(1) : 0, p: s.p }}))
    .filter(d => filters.teams.has(d.t))
    .sort((a, b) => b.pct - a.pct);

  document.getElementById('sub-team-chart').textContent = `${{[...filters.seasons].sort().join(', ')}}`;
  const labels = data.map(d => d.t.replace('Royal Challengers Bengaluru','RCB').replace('Mumbai Indians','MI').replace('Chennai Super Kings','CSK').replace('Kolkata Knight Riders','KKR').replace('Delhi Capitals','DC').replace('Rajasthan Royals','RR').replace('Punjab Kings','PBKS').replace('Sunrisers Hyderabad','SRH'));
  const vals = data.map(d => d.pct);
  const colors = data.map(d => TEAM_COLORS[d.t] || '#94a3b8');

  updateChart('chart-team-win', 'bar', labels, {{
    label: 'Win %',
    data: vals,
    backgroundColor: colors.map(c => c + 'd0'),
    borderColor: colors,
    borderWidth: 2,
    borderRadius: 6,
    borderSkipped: false
  }}, {{
    ...CHART_DEFAULTS,
    scales: {{
      ...CHART_DEFAULTS.scales,
      y: {{ ...CHART_DEFAULTS.scales.y, min: 0, max: 100, ticks: {{ callback: v => v + '%' }} }}
    }}
  }});
}}

// ─────────────────────────────────────────────
// SEASON WINS TRAJECTORY
// ─────────────────────────────────────────────
function updateSeasonWins(fm) {{
  const teamWins = {{}};
  fm.forEach(m => {{
    if (m.winner && filters.teams.has(m.winner)) {{
      teamWins[m.winner] = (teamWins[m.winner] || 0) + 1;
    }}
  }});
  const topTeams = Object.entries(teamWins).sort((a, b) => b[1] - a[1]).slice(0, 4).map(x => x[0]);
  const seasons = [...filters.seasons].sort();

  const datasets = topTeams.map(t => ({{
    label: t.split(' ').pop(),
    data: seasons.map(s => fm.filter(m => m.season === s && m.winner === t).length),
    borderColor: TEAM_COLORS[t] || '#94a3b8',
    backgroundColor: (TEAM_COLORS[t] || '#94a3b8') + '25',
    borderWidth: 2.5,
    pointRadius: 5,
    tension: 0.3,
    fill: true
  }}));

  updateChart('chart-season-wins', 'line', seasons, datasets, {{
    ...CHART_DEFAULTS,
    scales: {{
      ...CHART_DEFAULTS.scales,
      y: {{ ...CHART_DEFAULTS.scales.y, min: 0, ticks: {{ stepSize: 1 }} }}
    }}
  }}, true);
}}

// ─────────────────────────────────────────────
// TEAM TABLE
// ─────────────────────────────────────────────
function updateTeamTable(fm) {{
  const teams = {{}};
  fm.forEach(m => {{
    [m.team1, m.team2].forEach(t => {{
      if (filters.teams.has(t)) {{
        if (!teams[t]) teams[t] = {{ p: 0, w: 0 }};
        teams[t].p++;
      }}
    }});
    if (m.winner && filters.teams.has(m.winner) && teams[m.winner]) {{
      teams[m.winner].w++;
    }}
  }});
  const rows = Object.entries(teams)
    .map(([t, s]) => ({{ t, p: s.p, w: s.w, l: s.p - s.w, pct: s.p ? +((s.w / s.p) * 100).toFixed(1) : 0 }}))
    .sort((a, b) => b.pct - a.pct);

  const max = rows[0]?.pct || 1;
  const body = document.getElementById('team-tbody');
  body.innerHTML = rows.map((r, i) => {{
    const rBadge = i === 0 ? 'r1' : i === 1 ? 'r2' : i === 2 ? 'r3' : '';
    const bw = Math.round((r.pct / max) * 140);
    return `<tr>
      <td><span class="badge-r ${{rBadge}}">${{i + 1}}</span></td>
      <td>${{r.t}}</td>
      <td>${{r.p}}</td>
      <td>${{r.w}}</td>
      <td>${{r.l}}</td>
      <td><strong>${{r.pct}}%</strong></td>
      <td>
        <div class="bar-cell">
          <div class="mini-bar" style="width:${{bw}}px"></div>
          <span class="pct-text">${{r.pct}}%</span>
        </div>
      </td>
    </tr>`;
  }}).join('') || `<tr><td colspan="7" style="text-align:center;padding:24px;color:var(--t3)">No franchise data for selected filters</td></tr>`;
}}

// ─────────────────────────────────────────────
// PLAYER BATTING CHART & TABLE
// ─────────────────────────────────────────────
function updateBattingChart(fp) {{
  const byPlayer = groupBy(fp, 'player');
  const agg = Object.entries(byPlayer)
    .map(([p, rows]) => ({{
      p, runs: rows.reduce((a, x) => a + (+x.runs_scored || 0), 0),
      inn: rows.length, balls: rows.reduce((a, x) => a + (+x.balls_faced || 0), 0)
    }}))
    .filter(x => x.inn >= filters.minInnings)
    .sort((a, b) => b.runs - a.runs).slice(0, 10);

  document.getElementById('sub-batting').textContent = `Top ${{agg.length}} (min ${{filters.minInnings}} inn)`;
  updateChart('chart-batting', 'bar', agg.map(d => d.p), {{
    label: 'Total Runs',
    data: agg.map(d => d.runs),
    backgroundColor: agg.map((_, i) => `hsl(${{36 + i * 8}}, 90%, ${{62 - i * 2}}%)`),
    borderRadius: 6,
    borderSkipped: false
  }}, {{
    ...CHART_DEFAULTS,
    indexAxis: 'y',
    plugins: {{
      ...CHART_DEFAULTS.plugins,
      tooltip: {{ callbacks: {{ label: ctx => `${{ctx.parsed.x.toLocaleString()}} runs` }} }}
    }}
  }});
}}

function updateBatTable(fp) {{
  const byPlayer = groupBy(fp, 'player');
  const rows = Object.entries(byPlayer)
    .map(([p, rs]) => {{
      const runs = rs.reduce((a, x) => a + (+x.runs_scored || 0), 0);
      const balls = rs.reduce((a, x) => a + (+x.balls_faced || 0), 0);
      const fours = rs.reduce((a, x) => a + (+x.fours || 0), 0);
      const sixes = rs.reduce((a, x) => a + (+x.sixes || 0), 0);
      const inn = rs.length;
      const sr = balls > 0 ? +((runs / balls) * 100).toFixed(1) : 0;
      return {{ p, runs, inn, sr, fours, sixes }};
    }})
    .filter(x => x.inn >= filters.minInnings)
    .sort((a, b) => b.runs - a.runs).slice(0, 30);

  const body = document.getElementById('bat-tbody');
  body.innerHTML = rows.map((r, i) => {{
    const rBadge = i === 0 ? 'r1' : i === 1 ? 'r2' : i === 2 ? 'r3' : '';
    return `<tr>
      <td><span class="badge-r ${{rBadge}}">${{i + 1}}</span></td>
      <td>${{r.p}}</td>
      <td><strong>${{r.runs.toLocaleString()}}</strong></td>
      <td>${{r.inn}}</td>
      <td>${{r.sr}}</td>
      <td>${{r.fours}}</td>
      <td>${{r.sixes}}</td>
    </tr>`;
  }}).join('') || `<tr><td colspan="7" style="text-align:center;padding:24px;color:var(--t3)">No batters match filter</td></tr>`;
}}

// ─────────────────────────────────────────────
// PLAYER BOWLING CHART & TABLE
// ─────────────────────────────────────────────
function updateBowlingChart(fp) {{
  const byPlayer = groupBy(fp, 'player');
  const agg = Object.entries(byPlayer)
    .map(([p, rows]) => ({{
      p, wkts: rows.reduce((a, x) => a + (+x.wickets_taken || 0), 0),
      inn: rows.length, overs: rows.reduce((a, x) => a + (+x.overs_bowled || 0), 0)
    }}))
    .filter(x => x.inn >= filters.minInnings && x.wkts > 0)
    .sort((a, b) => b.wkts - a.wkts).slice(0, 10);

  document.getElementById('sub-bowling').textContent = `Top ${{agg.length}} (min ${{filters.minInnings}} inn)`;
  updateChart('chart-bowling', 'bar', agg.map(d => d.p), {{
    label: 'Wickets',
    data: agg.map(d => d.wkts),
    backgroundColor: agg.map((_, i) => `hsl(${{142 + i * 8}}, 75%, ${{55 - i * 2}}%)`),
    borderRadius: 6,
    borderSkipped: false
  }}, {{
    ...CHART_DEFAULTS,
    indexAxis: 'y',
    plugins: {{
      ...CHART_DEFAULTS.plugins,
      tooltip: {{ callbacks: {{ label: ctx => `${{ctx.parsed.x}} wickets` }} }}
    }}
  }});
}}

function updateBowlTable(fp) {{
  const byPlayer = groupBy(fp, 'player');
  const rows = Object.entries(byPlayer)
    .map(([p, rs]) => {{
      const wkts = rs.reduce((a, x) => a + (+x.wickets_taken || 0), 0);
      const overs = rs.reduce((a, x) => a + (+x.overs_bowled || 0), 0);
      const rconceded = rs.reduce((a, x) => a + (+x.runs_conceded || 0), 0);
      const inn = rs.length;
      const econ = overs > 0 ? +(rconceded / overs).toFixed(2) : 0;
      return {{ p, wkts, overs: +overs.toFixed(1), econ, rconceded, inn }};
    }})
    .filter(x => x.inn >= filters.minInnings && x.wkts > 0)
    .sort((a, b) => b.wkts - a.wkts).slice(0, 30);

  const body = document.getElementById('bowl-tbody');
  body.innerHTML = rows.map((r, i) => {{
    const rBadge = i === 0 ? 'r1' : i === 1 ? 'r2' : i === 2 ? 'r3' : '';
    return `<tr>
      <td><span class="badge-r ${{rBadge}}">${{i + 1}}</span></td>
      <td>${{r.p}}</td>
      <td><strong>${{r.wkts}}</strong></td>
      <td>${{r.overs}}</td>
      <td>${{r.econ}}</td>
      <td>${{r.rconceded.toLocaleString()}}</td>
    </tr>`;
  }}).join('') || `<tr><td colspan="6" style="text-align:center;padding:24px;color:var(--t3)">No bowlers match filter</td></tr>`;
}}

// ─────────────────────────────────────────────
// TOSS & MARGIN CHARTS
// ─────────────────────────────────────────────
function updateTossCharts(fm) {{
  const bat = fm.filter(m => m.toss_decision === 'bat');
  const field = fm.filter(m => m.toss_decision === 'field');
  const batWin = bat.filter(m => m.toss_winner === m.winner).length;
  const fieldWin = field.filter(m => m.toss_winner === m.winner).length;
  const batPct = bat.length ? +((batWin / bat.length) * 100).toFixed(1) : 0;
  const fieldPct = field.length ? +((fieldWin / field.length) * 100).toFixed(1) : 0;

  updateChart('chart-toss', 'bar', ['Bat First', 'Field First'], {{
    label: 'Win Rate %',
    data: [batPct, fieldPct],
    backgroundColor: ['rgba(239,68,68,.75)', 'rgba(34,197,94,.75)'],
    borderColor: ['#ef4444', '#22c55e'],
    borderWidth: 2,
    borderRadius: 8,
    borderSkipped: false
  }}, {{
    ...CHART_DEFAULTS,
    scales: {{
      ...CHART_DEFAULTS.scales,
      y: {{ ...CHART_DEFAULTS.scales.y, min: 0, max: 100, ticks: {{ callback: v => v + '%' }} }}
    }}
  }});

  updateChart('chart-toss-split', 'doughnut', ['Bat First', 'Field First'], {{
    data: [bat.length, field.length],
    backgroundColor: ['rgba(239,68,68,.8)', 'rgba(34,197,94,.8)'],
    borderColor: ['#ef4444', '#22c55e'],
    borderWidth: 2
  }}, {{
    plugins: {{ legend: {{ labels: {{ color: 'rgba(255,255,255,.75)' }} }} }},
    cutout: '65%'
  }});

  // Margin distribution
  const margins = fm.filter(m => m.win_by_runs > 0).map(m => m.win_by_runs);
  const bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 100, 150];
  const hist = bins.slice(0, -1).map((b, i) => margins.filter(v => v >= b && v < bins[i + 1]).length);
  const labels = bins.slice(0, -1).map((b, i) => `${{b}}-${{bins[i + 1] - 1}}`);

  updateChart('chart-margins', 'bar', labels, {{
    label: 'Matches',
    data: hist,
    backgroundColor: 'rgba(6,182,212,.65)',
    borderColor: '#06b6d4',
    borderWidth: 1.5,
    borderRadius: 5,
    borderSkipped: false
  }}, {{ ...CHART_DEFAULTS }});
}}

// ─────────────────────────────────────────────
// VENUE SCORES & BOUNDARIES
// ─────────────────────────────────────────────
function updateVenueChart(fm) {{
  const venues = {{}};
  fm.forEach(m => {{
    if (!venues[m.venue]) venues[m.venue] = {{ sum: 0, n: 0 }};
    venues[m.venue].sum += +m.team1_score || 0;
    venues[m.venue].n++;
  }});
  const data = Object.entries(venues)
    .map(([v, s]) => ({{ v, avg: s.n ? +(s.sum / s.n).toFixed(1) : 0 }}))
    .sort((a, b) => b.avg - a.avg);

  const labels = data.map(d => d.v.replace(' Stadium', '').replace(' International', ''));
  const vals = data.map(d => d.avg);

  updateChart('chart-venue', 'bar', labels, {{
    label: 'Avg 1st Inn Score',
    data: vals,
    backgroundColor: 'rgba(59,130,246,.7)',
    borderColor: '#3b82f6',
    borderWidth: 1.5,
    borderRadius: 6,
    borderSkipped: false
  }}, {{
    ...CHART_DEFAULTS,
    indexAxis: 'y',
    scales: {{
      ...CHART_DEFAULTS.scales,
      x: {{ ...CHART_DEFAULTS.scales.x, min: 0 }}
    }}
  }});
}}

function updateBoundaries(fp, fm) {{
  const matchToSeason = {{}};
  fm.forEach(m => {{ matchToSeason[m.match_id] = m.season; }});
  const seasons = [...filters.seasons].sort();
  const seasonFours = {{}}, seasonSixes = {{}};
  seasons.forEach(s => {{ seasonFours[s] = 0; seasonSixes[s] = 0; }});

  fp.forEach(p => {{
    const s = matchToSeason[p.match_id];
    if (s && filters.seasons.has(s)) {{
      seasonFours[s] += +p.fours || 0;
      seasonSixes[s] += +p.sixes || 0;
    }}
  }});

  updateChart('chart-boundaries', 'bar', seasons, [
    {{ label: 'Fours', data: seasons.map(s => seasonFours[s]), backgroundColor: 'rgba(59,130,246,.75)', borderColor: '#3b82f6', borderWidth: 1.5, borderRadius: 5, borderSkipped: false }},
    {{ label: 'Sixes', data: seasons.map(s => seasonSixes[s]), backgroundColor: 'rgba(168,85,247,.75)', borderColor: '#a855f7', borderWidth: 1.5, borderRadius: 5, borderSkipped: false }}
  ], {{ ...CHART_DEFAULTS }}, true);
}}

// ─────────────────────────────────────────────
// DYNAMIC INSIGHTS
// ─────────────────────────────────────────────
function updateInsights(fm, fp) {{
  const topTeam = getTopTeam(fm);
  const byPlayer = groupBy(fp, 'player');
  let topBatter = '—', topRuns = 0, topBowler = '—', topWkts = 0, topBowlerEcon = 99, topEconomist = '—';

  Object.entries(byPlayer).forEach(([p, rs]) => {{
    const r = rs.reduce((a, x) => a + (+x.runs_scored || 0), 0);
    const w = rs.reduce((a, x) => a + (+x.wickets_taken || 0), 0);
    const o = rs.reduce((a, x) => a + (+x.overs_bowled || 0), 0);
    const rc = rs.reduce((a, x) => a + (+x.runs_conceded || 0), 0);
    const econ = o > 4 ? rc / o : 99;
    if (r > topRuns) {{ topRuns = r; topBatter = p; }}
    if (w > topWkts) {{ topWkts = w; topBowler = p; }}
    if (econ < topBowlerEcon && w >= 5) {{ topBowlerEcon = +econ.toFixed(2); topEconomist = p; }}
  }});

  const tossWins = fm.filter(m => m.toss_winner === m.winner).length;
  const tossRate = fm.length ? ((tossWins / fm.length) * 100).toFixed(1) : 0;
  const fieldWins = fm.filter(m => m.toss_decision === 'field' && m.toss_winner === m.winner).length;
  const fieldTotal = fm.filter(m => m.toss_decision === 'field').length;
  const fieldRate = fieldTotal ? ((fieldWins / fieldTotal) * 100).toFixed(1) : 0;
  const avgScore = fm.length ? (fm.reduce((a, m) => a + (+m.team1_score || 0), 0) / fm.length).toFixed(1) : 0;
  const totalSix = fp.reduce((a, p) => a + (+p.sixes || 0), 0);

  const ins = [
    {{ em: '&#127942;', color: 'var(--gold)', title: `Best Franchise: ${{topTeam.name}}`, txt: `Dominates the selected scope with a ${{topTeam.pct}}% victory rate.` }},
    {{ em: '&#127953;', color: 'var(--gold)', title: `Top Scorer: ${{topBatter}}`, txt: `Accumulated ${{topRuns.toLocaleString()}} runs under active filters.` }},
    {{ em: '&#127919;', color: 'var(--green)', title: `Leading Wicket Taker: ${{topBowler}}`, txt: `Captured ${{topWkts}} dismissals across the filtered matches.` }},
    {{ em: '&#129689;', color: 'var(--pink)', title: `Toss Win Rate: ${{tossRate}}%`, txt: `Teams winning the toss converted to victory in ${{tossRate}}% of encounters.` }},
    {{ em: '&#127939;', color: 'var(--blue)', title: `Chasing Advantage: ${{fieldRate}}%`, txt: `Choosing to bowl/field after winning toss yields ${{fieldRate}}% match victories.` }},
    {{ em: '&#128200;', color: 'var(--cyan)', title: `Par Score: ${{avgScore}} Runs`, txt: `Average first-innings total across host venues in this filtered set.` }},
    {{ em: '&#127949;', color: 'var(--purple)', title: `Economy Benchmark`, txt: `${{topEconomist}} recorded the best economy at ${{topBowlerEcon}} runs/over.` }},
    {{ em: '6&#65039;&#8419;', color: 'var(--red)', title: `Total Sixes: ${{totalSix.toLocaleString()}}`, txt: `Number of maximums hit in the currently selected scope.` }}
  ];

  const grid = document.getElementById('insights-grid');
  grid.innerHTML = ins.map(d => `
    <div class="insight" style="--kc:${{d.color}}">
      <div class="insight-em">${{d.em}}</div>
      <div class="insight-ttl">${{d.title}}</div>
      <div class="insight-txt">${{d.txt}}</div>
    </div>
  `).join('');
}}

// ─────────────────────────────────────────────
// REAL-TIME ML PREDICTION CALCULATOR
// ─────────────────────────────────────────────
function runMLPrediction() {{
  const t1 = document.getElementById('pred-team1').value;
  const t2 = document.getElementById('pred-team2').value;
  const venue = document.getElementById('pred-venue').value;
  const tossWinner = document.getElementById('pred-toss-winner').value;
  const tossDec = document.getElementById('pred-toss-dec').value;

  const t1WinPct = TEAM_WIN_PCTS[t1] || 50;
  const t2WinPct = TEAM_WIN_PCTS[t2] || 50;
  const winDiff = t1WinPct - t2WinPct;

  // Logistic model formulation: log-odds from trained weights
  // z = 0.05 + 0.15 * winDiff/10 + 0.25 * (tossWinner === 'team1' ? 1 : -1) + 0.20 * (tossDec === 'field' ? 1 : -1)
  let logOdds = 0.04 + (0.16 * (winDiff / 5));
  if (tossWinner === 'team1') {{
    logOdds += 0.24;
  }} else {{
    logOdds -= 0.24;
  }}
  if (tossDec === 'field') {{
    logOdds += (tossWinner === 'team1' ? 0.28 : -0.28);
  }}

  // Sigmoid probability
  const probT1 = Math.min(Math.max(1 / (1 + Math.exp(-logOdds)), 0.15), 0.85);
  const pctT1 = Math.round(probT1 * 100);
  const pctT2 = 100 - pctT1;

  // Estimated 1st innings total based on venue average
  const venueAvg = VENUE_AVG_SCORES[venue] || 165;
  const estScore = Math.round(venueAvg + (winDiff * 0.4));

  const winnerName = pctT1 >= 50 ? t1 : t2;
  const winnerPct = pctT1 >= 50 ? pctT1 : pctT2;

  document.getElementById('pred-winner-text').innerHTML = `${{winnerName}} (<span style="color:var(--gold)">${{winnerPct}}%</span> Confidence)`;
  document.getElementById('pred-score-text').innerHTML = `Estimated 1st Innings Target: <strong>${{estScore}} runs</strong> &middot; Host Venue: ${{venue}}`;

  document.getElementById('meter-t1-lbl').textContent = `${{t1.split(' ').pop()}}: ${{pctT1}}%`;
  document.getElementById('meter-t2-lbl').textContent = `${{t2.split(' ').pop()}}: ${{pctT2}}%`;
  document.getElementById('pred-meter-fill').style.width = pctT1 + '%';
}}

// ─────────────────────────────────────────────
// CHART HELPER
// ─────────────────────────────────────────────
function updateChart(id, type, labels, datasets, options={{}}, multi=false) {{
  const ctx = document.getElementById(id).getContext('2d');
  if (charts[id]) charts[id].destroy();
  charts[id] = new Chart(ctx, {{
    type,
    data: {{ labels, datasets: multi ? datasets : [datasets] }},
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      animation: {{ duration: 350 }},
      ...options,
      plugins: {{
        legend: {{ display: multi, ...(options.plugins?.legend || {{}}) }},
        tooltip: {{ ...(options.plugins?.tooltip || {{}}) }},
        ...(options.plugins || {{}})
      }}
    }}
  }});
}}

// ─────────────────────────────────────────────
// TABLE SORT & SEARCH
// ─────────────────────────────────────────────
function sortTable(id, col) {{
  const table = document.getElementById(id);
  const tbody = table.querySelector('tbody');
  const rows = [...tbody.querySelectorAll('tr')];
  const th = table.querySelectorAll('th')[col];
  const asc = th.classList.contains('asc');
  table.querySelectorAll('th').forEach(t => t.classList.remove('asc', 'desc'));
  th.classList.toggle('asc', !asc);
  th.classList.toggle('desc', asc);
  rows.sort((a, b) => {{
    const av = a.cells[col]?.textContent.replace(/[,%]/g, '').trim() || '';
    const bv = b.cells[col]?.textContent.replace(/[,%]/g, '').trim() || '';
    const an = parseFloat(av), bn = parseFloat(bv);
    const cmp = isNaN(an) || isNaN(bn) ? av.localeCompare(bv) : an - bn;
    return asc ? -cmp : cmp;
  }});
  rows.forEach(r => tbody.appendChild(r));
}}

function filterTable(inputId, tbodyId) {{
  const q = document.getElementById(inputId).value.toLowerCase();
  document.querySelectorAll(`#${{tbodyId}} tr`).forEach(tr => {{
    tr.style.display = tr.textContent.toLowerCase().includes(q) ? '' : 'none';
  }});
}}

// ─────────────────────────────────────────────
// VIEW SWITCHER (TABS)
// ─────────────────────────────────────────────
function switchView(view, btn) {{
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');

  document.getElementById('view-interactive').style.display = view === 'interactive' ? 'block' : 'none';
  document.getElementById('view-ml').style.display = view === 'ml' ? 'block' : 'none';
  document.getElementById('view-gallery').style.display = view === 'gallery' ? 'block' : 'none';
  document.getElementById('view-explorer').style.display = view === 'explorer' ? 'block' : 'none';

  if (view === 'explorer') renderExplorer();
}}

// ─────────────────────────────────────────────
// DATA EXPLORER
// ─────────────────────────────────────────────
function setExplorerTab(mode) {{
  expMode = mode;
  expPage = 1;
  document.getElementById('tab-exp-matches').classList.toggle('active', mode === 'matches');
  document.getElementById('tab-exp-players').classList.toggle('active', mode === 'players');
  renderExplorer();
}}

function changeExpPage(delta) {{
  expPage += delta;
  renderExplorer();
}}

function renderExplorer() {{
  const data = expMode === 'matches' ? allMatches : allPlayers;
  const q = (document.getElementById('exp-search')?.value || '').toLowerCase();
  const filtered = data.filter(r => {{
    if (!q) return true;
    return Object.values(r).some(v => String(v).toLowerCase().includes(q));
  }});

  const totalPages = Math.ceil(filtered.length / EXP_PAGE_SIZE) || 1;
  if (expPage < 1) expPage = 1;
  if (expPage > totalPages) expPage = totalPages;

  document.getElementById('page-num').textContent = `Page ${{expPage}} of ${{totalPages}} (${{filtered.length}} records)`;
  document.getElementById('btn-prev').disabled = expPage === 1;
  document.getElementById('btn-next').disabled = expPage >= totalPages;

  const start = (expPage - 1) * EXP_PAGE_SIZE;
  const paged = filtered.slice(start, start + EXP_PAGE_SIZE);

  if (paged.length === 0) {{
    document.getElementById('exp-thead').innerHTML = '';
    document.getElementById('exp-tbody').innerHTML = '<tr><td style="padding:24px;text-align:center">No records found</td></tr>';
    return;
  }}

  const cols = Object.keys(paged[0]);
  document.getElementById('exp-thead').innerHTML = '<tr>' + cols.map(c => `<th>${{c}}</th>`).join('') + '</tr>';
  document.getElementById('exp-tbody').innerHTML = paged.map(row => `
    <tr>${{cols.map(c => `<td>${{row[c] !== null && row[c] !== undefined ? row[c] : '—'}}</td>`).join('')}}</tr>
  `).join('');
}}

// ─────────────────────────────────────────────
// UTILS
// ─────────────────────────────────────────────
function groupBy(arr, key) {{
  return arr.reduce((acc, item) => {{
    const k = item[key];
    if (!acc[k]) acc[k] = [];
    acc[k].push(item);
    return acc;
  }}, {{}});
}}

// Boot
loadData();
</script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Generated index.html with ML Studio successfully, size:", len(html), "bytes")
