<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DataLens — Intelligent Analysis System</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0a0d14;
    --surface: #111520;
    --surface2: #161b28;
    --surface3: #1c2336;
    --border: #252d42;
    --accent: #4f8ef7;
    --accent2: #7c5af7;
    --accent3: #f75a8e;
    --accent4: #5af7c8;
    --accent5: #f7c15a;
    --text: #e8ecf4;
    --text2: #8892a8;
    --text3: #4e5a70;
    --success: #4caf82;
    --warning: #f7a44a;
    --danger: #f75a5a;
    --radius: 12px;
    --radius-lg: 18px;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'DM Sans', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* HEADER */
  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 32px;
    border-bottom: 1px solid var(--border);
    background: var(--surface);
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(12px);
  }

  .logo {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
  }

  .logo span { color: var(--accent3); -webkit-text-fill-color: var(--accent3); }

  .header-right { display: flex; align-items: center; gap: 12px; }

  .badge {
    background: var(--surface3);
    border: 1px solid var(--border);
    color: var(--text2);
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 20px;
  }

  /* MAIN LAYOUT */
  .container {
    max-width: 1600px;
    margin: 0 auto;
    padding: 28px 32px;
  }

  /* UPLOAD ZONE */
  #upload-zone {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: calc(100vh - 70px);
    gap: 0;
  }

  .upload-card {
    background: var(--surface);
    border: 2px dashed var(--border);
    border-radius: 24px;
    padding: 64px 80px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    max-width: 640px;
    width: 100%;
    position: relative;
    overflow: hidden;
  }

  .upload-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(79,142,247,0.08) 0%, transparent 70%);
    pointer-events: none;
  }

  .upload-card:hover, .upload-card.drag-over {
    border-color: var(--accent);
    background: var(--surface2);
    transform: translateY(-2px);
    box-shadow: 0 20px 60px rgba(79,142,247,0.15);
  }

  .upload-icon {
    width: 72px;
    height: 72px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 24px;
    font-size: 32px;
  }

  .upload-title {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 10px;
    color: var(--text);
  }

  .upload-sub {
    color: var(--text2);
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 28px;
  }

  .upload-btn {
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    color: white;
    border: none;
    padding: 13px 32px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    font-family: 'DM Sans', sans-serif;
    transition: opacity 0.2s;
  }

  .upload-btn:hover { opacity: 0.88; }

  .file-types {
    display: flex;
    gap: 10px;
    justify-content: center;
    margin-top: 20px;
    flex-wrap: wrap;
  }

  .file-type-badge {
    background: var(--surface3);
    border: 1px solid var(--border);
    color: var(--text2);
    font-size: 12px;
    font-family: 'DM Mono', monospace;
    padding: 4px 12px;
    border-radius: 6px;
  }

  #file-input { display: none; }

  /* DASHBOARD */
  #dashboard { display: none; }

  /* TOP BAR */
  .dash-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
    flex-wrap: wrap;
    gap: 12px;
  }

  .file-info {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .file-name {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
  }

  .file-meta {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: var(--text2);
    background: var(--surface2);
    padding: 4px 10px;
    border-radius: 6px;
  }

  .reset-btn {
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text2);
    padding: 8px 18px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 13px;
    font-family: 'DM Sans', sans-serif;
    transition: all 0.2s;
  }

  .reset-btn:hover { border-color: var(--accent3); color: var(--accent3); }

  /* CLEANING NOTES */
  #cleaning-notes {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--warning);
    border-radius: var(--radius);
    padding: 18px 22px;
    margin-bottom: 24px;
  }

  .notes-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: var(--warning);
    margin-bottom: 12px;
  }

  .note-item {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    font-size: 13px;
    color: var(--text2);
    padding: 5px 0;
    border-bottom: 1px solid var(--border);
    line-height: 1.5;
  }

  .note-item:last-child { border-bottom: none; }

  .note-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--warning);
    flex-shrink: 0;
    margin-top: 6px;
  }

  .note-dot.success { background: var(--success); }
  .note-dot.danger { background: var(--danger); }

  /* STATS GRID */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 14px;
    margin-bottom: 24px;
  }

  .stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
  }

  .stat-card:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,0,0,0.3); }

  .stat-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--stat-color, var(--accent));
  }

  .stat-label {
    font-size: 11px;
    color: var(--text3);
    font-family: 'DM Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
  }

  .stat-val {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 700;
    color: var(--stat-color, var(--text));
  }

  .stat-sub { font-size: 11px; color: var(--text3); margin-top: 3px; }

  /* TABS */
  .tab-bar {
    display: flex;
    gap: 4px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 6px;
    margin-bottom: 24px;
    overflow-x: auto;
  }

  .tab-btn {
    padding: 9px 18px;
    border-radius: 8px;
    border: none;
    background: transparent;
    color: var(--text2);
    font-size: 13px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 7px;
  }

  .tab-btn:hover { color: var(--text); background: var(--surface2); }

  .tab-btn.active {
    background: var(--accent);
    color: white;
  }

  .tab-content { display: none; }
  .tab-content.active { display: block; }

  /* CHARTS GRID */
  .charts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(460px, 1fr));
    gap: 20px;
    margin-bottom: 24px;
  }

  .chart-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
  }

  .chart-card.full-width {
    grid-column: 1 / -1;
  }

  .chart-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 18px;
    gap: 12px;
  }

  .chart-title {
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: var(--text);
  }

  .chart-subtitle {
    font-size: 12px;
    color: var(--text3);
    margin-top: 3px;
    font-family: 'DM Mono', monospace;
  }

  .chart-type-badge {
    font-size: 11px;
    font-family: 'DM Mono', monospace;
    padding: 3px 9px;
    border-radius: 5px;
    background: var(--surface3);
    color: var(--text3);
    flex-shrink: 0;
  }

  .chart-wrap {
    position: relative;
    width: 100%;
  }

  /* PIVOT TABLE */
  .pivot-wrap {
    overflow-x: auto;
    border-radius: var(--radius);
    border: 1px solid var(--border);
  }

  .pivot-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    font-family: 'DM Mono', monospace;
  }

  .pivot-table th {
    background: var(--surface3);
    color: var(--text2);
    padding: 10px 14px;
    text-align: left;
    font-weight: 500;
    border-bottom: 1px solid var(--border);
    white-space: nowrap;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .pivot-table td {
    padding: 9px 14px;
    border-bottom: 1px solid var(--border);
    color: var(--text);
  }

  .pivot-table tr:last-child td { border-bottom: none; }
  .pivot-table tr:hover td { background: var(--surface2); }
  .pivot-table td.num { text-align: right; color: var(--accent4); }
  .pivot-table td.label { color: var(--text2); }

  /* DATA PREVIEW TABLE */
  .data-table-wrap {
    overflow-x: auto;
    border-radius: var(--radius);
    border: 1px solid var(--border);
    max-height: 500px;
    overflow-y: auto;
  }

  .data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    font-family: 'DM Mono', monospace;
  }

  .data-table th {
    background: var(--surface3);
    color: var(--accent);
    padding: 11px 14px;
    text-align: left;
    font-weight: 500;
    border-bottom: 1px solid var(--border);
    white-space: nowrap;
    position: sticky;
    top: 0;
    z-index: 2;
    font-size: 11px;
  }

  .data-table td {
    padding: 9px 14px;
    border-bottom: 1px solid var(--border);
    color: var(--text2);
    white-space: nowrap;
    max-width: 180px;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .data-table tr:hover td { background: var(--surface2); color: var(--text); }

  /* HEATMAP */
  .heatmap-container {
    overflow-x: auto;
  }

  .heatmap-table {
    border-collapse: collapse;
    font-size: 11px;
    font-family: 'DM Mono', monospace;
    width: 100%;
  }

  .heatmap-table th {
    padding: 8px 10px;
    color: var(--text2);
    font-weight: 400;
    text-align: center;
    white-space: nowrap;
    font-size: 10px;
  }

  .heatmap-table td {
    width: 60px;
    height: 44px;
    text-align: center;
    font-size: 11px;
    font-weight: 500;
    border: 2px solid var(--bg);
    border-radius: 4px;
    transition: transform 0.15s;
  }

  .heatmap-table td:hover { transform: scale(1.08); z-index: 2; position: relative; cursor: default; }

  /* SECTION TITLE */
  .section-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }

  /* COLUMN GRID */
  .col-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
    margin-bottom: 24px;
  }

  .col-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 14px 16px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .col-card:hover { border-color: var(--accent); }

  .col-name {
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    font-weight: 500;
    color: var(--text);
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .col-type {
    font-size: 11px;
    padding: 2px 7px;
    border-radius: 4px;
    display: inline-block;
    font-family: 'DM Mono', monospace;
  }

  .col-type.numeric { background: rgba(79,142,247,0.15); color: var(--accent); }
  .col-type.categorical { background: rgba(124,90,247,0.15); color: var(--accent2); }
  .col-type.date { background: rgba(90,247,200,0.15); color: var(--accent4); }

  /* LOADING */
  #loading-overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(10,13,20,0.85);
    backdrop-filter: blur(8px);
    z-index: 999;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 18px;
  }

  #loading-overlay.show { display: flex; }

  .spinner {
    width: 44px;
    height: 44px;
    border: 3px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  .loading-text {
    font-family: 'DM Mono', monospace;
    font-size: 14px;
    color: var(--text2);
  }

  /* EMPTY STATE */
  .empty-state {
    text-align: center;
    padding: 48px;
    color: var(--text3);
    font-size: 14px;
  }

  /* RESPONSIVE */
  @media (max-width: 768px) {
    .charts-grid { grid-template-columns: 1fr; }
    header { padding: 14px 18px; }
    .container { padding: 18px; }
    .upload-card { padding: 40px 24px; }
  }
</style>
</head>
<body>

<div id="loading-overlay">
  <div class="spinner"></div>
  <div class="loading-text">Analyzing your data...</div>
</div>

<header>
  <div class="logo">Data<span>Lens</span></div>
  <div class="header-right">
    <div class="badge">Intelligent Analysis System</div>
  </div>
</header>

<!-- UPLOAD ZONE -->
<div id="upload-zone">
  <div class="upload-card" id="drop-zone">
    <div class="upload-icon">📊</div>
    <div class="upload-title">Upload Your Dataset</div>
    <div class="upload-sub">Drop your file here and DataLens will automatically clean it,<br>analyze it, and generate interactive visualizations.</div>
    <button class="upload-btn" onclick="document.getElementById('file-input').click()">Choose File</button>
    <div class="file-types">
      <span class="file-type-badge">.CSV</span>
      <span class="file-type-badge">.XLSX</span>
      <span class="file-type-badge">.XLS</span>
      <span class="file-type-badge">.JSON</span>
      <span class="file-type-badge">.TSV</span>
    </div>
    <input type="file" id="file-input" accept=".csv,.xlsx,.xls,.json,.tsv">
  </div>
</div>

<!-- DASHBOARD -->
<div id="dashboard">
  <div class="container">
    <!-- Top bar -->
    <div class="dash-topbar">
      <div class="file-info">
        <span class="file-name" id="file-display-name">dataset.csv</span>
        <span class="file-meta" id="file-meta-info"></span>
      </div>
      <button class="reset-btn" onclick="resetDashboard()">← Upload New File</button>
    </div>

    <!-- Cleaning Notes -->
    <div id="cleaning-notes" style="display:none">
      <div class="notes-header">⚠ Data Cleaning Report</div>
      <div id="notes-list"></div>
    </div>

    <!-- Stats Row -->
    <div class="stats-grid" id="stats-grid"></div>

    <!-- Tabs -->
    <div class="tab-bar">
      <button class="tab-btn active" onclick="switchTab('overview', this)">📊 Overview</button>
      <button class="tab-btn" onclick="switchTab('distributions', this)">📈 Distributions</button>
      <button class="tab-btn" onclick="switchTab('relationships', this)">🔗 Relationships</button>
      <button class="tab-btn" onclick="switchTab('pivot', this)">🗂 Pivot Tables</button>
      <button class="tab-btn" onclick="switchTab('data', this)">🗄 Raw Data</button>
    </div>

    <!-- Overview Tab -->
    <div id="tab-overview" class="tab-content active">
      <div class="section-title">Column Overview</div>
      <div class="col-grid" id="col-grid"></div>
      <div class="section-title">Key Charts</div>
      <div class="charts-grid" id="overview-charts"></div>
    </div>

    <!-- Distributions Tab -->
    <div id="tab-distributions" class="tab-content">
      <div class="section-title">Distributions & Frequencies</div>
      <div class="charts-grid" id="dist-charts"></div>
    </div>

    <!-- Relationships Tab -->
    <div id="tab-relationships" class="tab-content">
      <div class="section-title">Correlations & Relationships</div>
      <div class="charts-grid" id="rel-charts"></div>
      <div class="chart-card full-width" id="heatmap-card" style="display:none">
        <div class="chart-header">
          <div>
            <div class="chart-title">Correlation Heatmap</div>
            <div class="chart-subtitle">Numeric columns — correlation matrix</div>
          </div>
          <span class="chart-type-badge">HEATMAP</span>
        </div>
        <div class="heatmap-container" id="heatmap-container"></div>
      </div>
    </div>

    <!-- Pivot Tables Tab -->
    <div id="tab-pivot" class="tab-content">
      <div class="section-title">Pivot Tables</div>
      <div id="pivot-tables"></div>
    </div>

    <!-- Raw Data Tab -->
    <div id="tab-data" class="tab-content">
      <div class="section-title">Data Preview (first 200 rows)</div>
      <div class="data-table-wrap" id="data-table-wrap"></div>
    </div>
  </div>
</div>

<script>
// ── Chart registry (for destroy before re-render)
const chartRegistry = {};

// ── Color palette
const PALETTE = [
  '#4f8ef7','#7c5af7','#f75a8e','#5af7c8','#f7c15a',
  '#f75a5a','#5af75a','#f7985a','#5ab3f7','#c55af7'
];

// ── Global data store
let gData = [], gColumns = [], gFileName = '';

// ──────────────────────────────────────────────
//  FILE HANDLING
// ──────────────────────────────────────────────
document.getElementById('file-input').addEventListener('change', e => {
  if (e.target.files[0]) handleFile(e.target.files[0]);
});

const dropZone = document.getElementById('drop-zone');
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('drag-over'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('drag-over');
  if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
});

function handleFile(file) {
  gFileName = file.name;
  showLoading();
  const ext = file.name.split('.').pop().toLowerCase();

  if (ext === 'csv' || ext === 'tsv') {
    const reader = new FileReader();
    reader.onload = ev => {
      const result = Papa.parse(ev.target.result, { header: true, skipEmptyLines: true, dynamicTyping: true, delimiter: ext === 'tsv' ? '\t' : undefined });
      processData(result.data, result.meta.fields);
    };
    reader.readAsText(file);
  } else if (ext === 'xlsx' || ext === 'xls') {
    const reader = new FileReader();
    reader.onload = ev => {
      const wb = XLSX.read(ev.target.result, { type: 'array' });
      const ws = wb.Sheets[wb.SheetNames[0]];
      const rows = XLSX.utils.sheet_to_json(ws, { defval: null });
      const cols = rows.length ? Object.keys(rows[0]) : [];
      processData(rows, cols);
    };
    reader.readAsArrayBuffer(file);
  } else if (ext === 'json') {
    const reader = new FileReader();
    reader.onload = ev => {
      let data = JSON.parse(ev.target.result);
      if (!Array.isArray(data)) data = [data];
      const cols = data.length ? Object.keys(data[0]) : [];
      processData(data, cols);
    };
    reader.readAsText(file);
  } else {
    hideLoading();
    alert('Unsupported file format. Please use CSV, XLSX, XLS, JSON, or TSV.');
  }
}

// ──────────────────────────────────────────────
//  DATA PROCESSING
// ──────────────────────────────────────────────
function processData(raw, cols) {
  const notes = [];
  let data = raw.map(r => ({ ...r }));

  // 1. Remove completely empty rows
  const before = data.length;
  data = data.filter(r => cols.some(c => r[c] !== null && r[c] !== '' && r[c] !== undefined));
  if (data.length < before) notes.push({ type: 'warning', msg: `Removed ${before - data.length} fully empty row(s).` });

  // 2. Trim whitespace on string cols
  cols.forEach(c => {
    let trimmed = 0;
    data.forEach(r => {
      if (typeof r[c] === 'string' && r[c] !== r[c].trim()) { r[c] = r[c].trim(); trimmed++; }
    });
    if (trimmed > 0) notes.push({ type: 'success', msg: `Trimmed whitespace in "${c}" (${trimmed} cells).` });
  });

  // 3. Detect & parse date columns
  cols.forEach(c => {
    const sample = data.slice(0, 20).map(r => r[c]).filter(v => v !== null && v !== '');
    const dateCount = sample.filter(v => {
      if (typeof v === 'string') { const d = new Date(v); return !isNaN(d) && v.match(/\d{2,4}[-/]\d{1,2}[-/]\d{1,2}/); }
      return false;
    }).length;
    if (dateCount / sample.length > 0.6) {
      notes.push({ type: 'success', msg: `Detected date format in column "${c}" — parsed as Date.` });
    }
  });

  // 4. Detect nulls/missing
  const nullCols = {};
  cols.forEach(c => {
    const nullCount = data.filter(r => r[c] === null || r[c] === '' || r[c] === undefined).length;
    if (nullCount > 0) nullCols[c] = nullCount;
  });
  Object.entries(nullCols).forEach(([c, n]) => {
    const pct = ((n / data.length) * 100).toFixed(1);
    notes.push({ type: pct > 30 ? 'danger' : 'warning', msg: `Column "${c}" has ${n} missing values (${pct}%).` });
  });

  // 5. Duplicate rows
  const seen = new Set();
  let dupCount = 0;
  data = data.filter(r => {
    const key = JSON.stringify(r);
    if (seen.has(key)) { dupCount++; return false; }
    seen.add(key); return true;
  });
  if (dupCount > 0) notes.push({ type: 'warning', msg: `Removed ${dupCount} duplicate row(s).` });

  // 6. Fill missing numerics with median
  cols.forEach(c => {
    const vals = data.map(r => r[c]).filter(v => typeof v === 'number' && !isNaN(v));
    if (vals.length === 0) return;
    const nullCount = data.filter(r => r[c] === null || r[c] === '' || r[c] === undefined).length;
    if (nullCount > 0 && nullCount < data.length * 0.5) {
      const sorted = [...vals].sort((a, b) => a - b);
      const median = sorted[Math.floor(sorted.length / 2)];
      data.forEach(r => { if (r[c] === null || r[c] === '' || r[c] === undefined) r[c] = median; });
      notes.push({ type: 'success', msg: `Filled ${nullCount} missing values in "${c}" with median (${median}).` });
    }
  });

  gData = data;
  gColumns = cols;

  setTimeout(() => {
    hideLoading();
    renderDashboard(notes);
  }, 400);
}

// ──────────────────────────────────────────────
//  COLUMN CLASSIFICATION
// ──────────────────────────────────────────────
function classifyCols(data, cols) {
  const numeric = [], categorical = [], dateCols = [];
  cols.forEach(c => {
    const vals = data.map(r => r[c]).filter(v => v !== null && v !== '' && v !== undefined);
    const numVals = vals.filter(v => typeof v === 'number' && !isNaN(v));
    const unique = new Set(vals).size;
    if (numVals.length / vals.length > 0.7) numeric.push(c);
    else if (vals.some(v => typeof v === 'string' && v.match(/\d{2,4}[-/]\d{1,2}[-/]\d{1,2}/))) dateCols.push(c);
    else categorical.push(c);
  });
  return { numeric, categorical, dateCols };
}

// ──────────────────────────────────────────────
//  STATS
// ──────────────────────────────────────────────
function numStats(data, col) {
  const vals = data.map(r => r[col]).filter(v => typeof v === 'number' && !isNaN(v));
  if (!vals.length) return {};
  const sorted = [...vals].sort((a, b) => a - b);
  const sum = vals.reduce((a, b) => a + b, 0);
  const mean = sum / vals.length;
  const variance = vals.reduce((a, v) => a + (v - mean) ** 2, 0) / vals.length;
  return {
    min: sorted[0], max: sorted[sorted.length - 1],
    mean: +mean.toFixed(2), median: sorted[Math.floor(sorted.length / 2)],
    std: +Math.sqrt(variance).toFixed(2), count: vals.length, sum: +sum.toFixed(2)
  };
}

function valueCounts(data, col) {
  const counts = {};
  data.forEach(r => {
    const v = r[col];
    if (v !== null && v !== '' && v !== undefined) counts[v] = (counts[v] || 0) + 1;
  });
  return Object.entries(counts).sort((a, b) => b[1] - a[1]);
}

function correlationMatrix(data, numCols) {
  const means = {}, stds = {};
  numCols.forEach(c => {
    const s = numStats(data, c);
    means[c] = s.mean; stds[c] = s.std;
  });
  const matrix = {};
  numCols.forEach(c1 => {
    matrix[c1] = {};
    numCols.forEach(c2 => {
      const vals = data.filter(r =>
        typeof r[c1] === 'number' && !isNaN(r[c1]) &&
        typeof r[c2] === 'number' && !isNaN(r[c2])
      );
      if (!vals.length || !stds[c1] || !stds[c2]) { matrix[c1][c2] = 0; return; }
      const cov = vals.reduce((a, r) => a + (r[c1] - means[c1]) * (r[c2] - means[c2]), 0) / vals.length;
      matrix[c1][c2] = +(cov / (stds[c1] * stds[c2])).toFixed(3);
    });
  });
  return matrix;
}

// ──────────────────────────────────────────────
//  RENDER DASHBOARD
// ──────────────────────────────────────────────
function renderDashboard(notes) {
  // Destroy old charts
  Object.values(chartRegistry).forEach(c => c.destroy());
  Object.keys(chartRegistry).forEach(k => delete chartRegistry[k]);

  const data = gData, cols = gColumns;
  const { numeric, categorical, dateCols } = classifyCols(data, cols);

  // File info
  document.getElementById('file-display-name').textContent = gFileName;
  document.getElementById('file-meta-info').textContent = `${data.length} rows × ${cols.length} cols`;

  // Cleaning notes
  const notesDiv = document.getElementById('cleaning-notes');
  const notesList = document.getElementById('notes-list');
  notesList.innerHTML = '';
  if (notes.length) {
    notes.forEach(n => {
      notesList.innerHTML += `<div class="note-item"><div class="note-dot ${n.type}"></div><span>${n.msg}</span></div>`;
    });
    notesDiv.style.display = 'block';
  } else {
    notesDiv.style.display = 'none';
  }

  // Stats
  const sg = document.getElementById('stats-grid');
  sg.innerHTML = '';
  const statsData = [
    { label: 'Total Rows', val: data.length, color: 'var(--accent)', sub: 'after cleaning' },
    { label: 'Columns', val: cols.length, color: 'var(--accent2)', sub: 'total features' },
    { label: 'Numeric', val: numeric.length, color: 'var(--accent4)', sub: 'numeric cols' },
    { label: 'Categorical', val: categorical.length, color: 'var(--accent5)', sub: 'categorical cols' },
    { label: 'Missing', val: cols.reduce((a, c) => a + data.filter(r => r[c] === null || r[c] === '' || r[c] === undefined).length, 0), color: 'var(--warning)', sub: 'total null cells' },
    { label: 'Cleaning Notes', val: notes.length, color: notes.length ? 'var(--warning)' : 'var(--success)', sub: 'actions taken' },
  ];
  statsData.forEach(s => {
    sg.innerHTML += `<div class="stat-card" style="--stat-color:${s.color}">
      <div class="stat-label">${s.label}</div>
      <div class="stat-val">${s.val.toLocaleString()}</div>
      <div class="stat-sub">${s.sub}</div>
    </div>`;
  });

  // Column cards
  const colGrid = document.getElementById('col-grid');
  colGrid.innerHTML = '';
  cols.forEach(c => {
    const type = numeric.includes(c) ? 'numeric' : dateCols.includes(c) ? 'date' : 'categorical';
    const unique = new Set(data.map(r => r[c]).filter(v => v !== null && v !== '')).size;
    colGrid.innerHTML += `<div class="col-card">
      <div class="col-name">${c}</div>
      <span class="col-type ${type}">${type}</span>
      <div style="font-size:11px;color:var(--text3);margin-top:6px;font-family:'DM Mono',monospace">${unique} unique values</div>
    </div>`;
  });

  // ── Overview charts
  const oc = document.getElementById('overview-charts');
  oc.innerHTML = '';

  // Bar chart: first categorical value counts
  if (categorical.length) {
    const c = categorical[0];
    const vc = valueCounts(data, c).slice(0, 15);
    const id = 'ov-bar-' + c;
    oc.innerHTML += chartCard(id, `"${c}" Distribution`, 'Top values', 'BAR');
    setTimeout(() => {
      const ctx = document.getElementById(id)?.getContext('2d');
      if (!ctx) return;
      chartRegistry[id] = new Chart(ctx, {
        type: 'bar',
        data: { labels: vc.map(v => String(v[0]).slice(0, 18)), datasets: [{ label: 'Count', data: vc.map(v => v[1]), backgroundColor: PALETTE.map(p => p + 'cc'), borderRadius: 6, borderSkipped: false }] },
        options: chartOpts('Count')
      });
    }, 50);
  }

  // Pie chart: second categorical
  if (categorical.length > 1) {
    const c = categorical[1];
    const vc = valueCounts(data, c).slice(0, 8);
    const id = 'ov-pie-' + c;
    oc.innerHTML += chartCard(id, `"${c}" Composition`, 'Proportional breakdown', 'PIE');
    setTimeout(() => {
      const ctx = document.getElementById(id)?.getContext('2d');
      if (!ctx) return;
      chartRegistry[id] = new Chart(ctx, {
        type: 'pie',
        data: { labels: vc.map(v => String(v[0]).slice(0, 20)), datasets: [{ data: vc.map(v => v[1]), backgroundColor: PALETTE, borderWidth: 2, borderColor: 'var(--surface)' }] },
        options: { responsive: true, plugins: { legend: { position: 'right', labels: { color: '#8892a8', font: { family: 'DM Mono', size: 11 }, padding: 12 } } } }
      });
    }, 50);
  }

  // Line chart: first numeric over rows
  if (numeric.length) {
    const c = numeric[0];
    const step = Math.max(1, Math.floor(data.length / 80));
    const pts = data.filter((_, i) => i % step === 0).map((r, i) => ({ x: i * step, y: r[c] }));
    const id = 'ov-line-' + c;
    oc.innerHTML += chartCard(id, `"${c}" Trend`, 'Row-by-row values', 'LINE');
    setTimeout(() => {
      const ctx = document.getElementById(id)?.getContext('2d');
      if (!ctx) return;
      chartRegistry[id] = new Chart(ctx, {
        type: 'line',
        data: { datasets: [{ label: c, data: pts, borderColor: PALETTE[0], backgroundColor: PALETTE[0] + '22', fill: true, tension: 0.35, pointRadius: 0, borderWidth: 2 }] },
        options: { ...chartOpts(c), scales: { x: { type: 'linear', title: { display: true, text: 'Row', color: '#4e5a70', font: { family: 'DM Mono', size: 11 } }, grid: { color: '#1c2336' }, ticks: { color: '#4e5a70', font: { family: 'DM Mono', size: 10 } } }, y: { grid: { color: '#1c2336' }, ticks: { color: '#4e5a70', font: { family: 'DM Mono', size: 10 } } } } }
      });
    }, 50);
  }

  // ── Distributions charts
  const dc = document.getElementById('dist-charts');
  dc.innerHTML = '';

  // Histogram for each numeric col
  numeric.forEach((c, i) => {
    const vals = data.map(r => r[c]).filter(v => typeof v === 'number' && !isNaN(v));
    const s = numStats(data, c);
    const bins = 20;
    const step = (s.max - s.min) / bins;
    if (step === 0) return;
    const buckets = Array(bins).fill(0);
    const labels = [];
    for (let b = 0; b < bins; b++) labels.push((s.min + b * step).toFixed(1));
    vals.forEach(v => {
      const idx = Math.min(bins - 1, Math.floor((v - s.min) / step));
      buckets[idx]++;
    });
    const id = 'dist-hist-' + i;
    dc.innerHTML += chartCard(id, `"${c}" Histogram`, `mean: ${s.mean} | std: ${s.std}`, 'HISTOGRAM');
    setTimeout(() => {
      const ctx = document.getElementById(id)?.getContext('2d');
      if (!ctx) return;
      chartRegistry[id] = new Chart(ctx, {
        type: 'bar',
        data: { labels, datasets: [{ label: c, data: buckets, backgroundColor: PALETTE[i % PALETTE.length] + 'bb', borderColor: PALETTE[i % PALETTE.length], borderWidth: 1, borderRadius: 4, barPercentage: 1, categoryPercentage: 1 }] },
        options: chartOpts('Frequency')
      });
    }, 50);
  });

  // Bar/pie for each categorical
  categorical.forEach((c, i) => {
    const vc = valueCounts(data, c).slice(0, 12);
    if (vc.length <= 6) {
      // Pie
      const id = 'dist-pie-' + i;
      dc.innerHTML += chartCard(id, `"${c}" Breakdown`, `${vc.length} categories`, 'PIE');
      setTimeout(() => {
        const ctx = document.getElementById(id)?.getContext('2d');
        if (!ctx) return;
        chartRegistry[id] = new Chart(ctx, {
          type: 'pie',
          data: { labels: vc.map(v => String(v[0]).slice(0, 20)), datasets: [{ data: vc.map(v => v[1]), backgroundColor: PALETTE, borderWidth: 2, borderColor: 'var(--surface)' }] },
          options: { responsive: true, plugins: { legend: { position: 'right', labels: { color: '#8892a8', font: { family: 'DM Mono', size: 11 }, padding: 12 } } } }
        });
      }, 50);
    } else {
      // Bar
      const id = 'dist-bar-' + i;
      dc.innerHTML += chartCard(id, `"${c}" Top Values`, `showing top 12`, 'BAR');
      setTimeout(() => {
        const ctx = document.getElementById(id)?.getContext('2d');
        if (!ctx) return;
        chartRegistry[id] = new Chart(ctx, {
          type: 'bar',
          data: { labels: vc.map(v => String(v[0]).slice(0, 16)), datasets: [{ label: 'Count', data: vc.map(v => v[1]), backgroundColor: PALETTE[(i + 2) % PALETTE.length] + 'cc', borderRadius: 6, borderSkipped: false }] },
          options: chartOpts('Count')
        });
      }, 50);
    }
  });

  // ── Relationships
  const rc = document.getElementById('rel-charts');
  rc.innerHTML = '';

  // Scatter plots for numeric pairs
  if (numeric.length >= 2) {
    for (let a = 0; a < Math.min(numeric.length - 1, 3); a++) {
      for (let b = a + 1; b < Math.min(numeric.length, 4); b++) {
        const cx = numeric[a], cy = numeric[b];
        const pts = data
          .filter(r => typeof r[cx] === 'number' && typeof r[cy] === 'number' && !isNaN(r[cx]) && !isNaN(r[cy]))
          .slice(0, 500)
          .map(r => ({ x: r[cx], y: r[cy] }));
        const id = `scatter-${a}-${b}`;
        rc.innerHTML += chartCard(id, `"${cx}" vs "${cy}"`, 'Scatter plot', 'SCATTER');
        setTimeout(() => {
          const ctx = document.getElementById(id)?.getContext('2d');
          if (!ctx) return;
          chartRegistry[id] = new Chart(ctx, {
            type: 'scatter',
            data: { datasets: [{ label: `${cx} vs ${cy}`, data: pts, backgroundColor: PALETTE[(a + b) % PALETTE.length] + '99', pointRadius: 4 }] },
            options: { responsive: true, plugins: { legend: { display: false } }, scales: {
              x: { title: { display: true, text: cx, color: '#4e5a70', font: { family: 'DM Mono', size: 11 } }, grid: { color: '#1c2336' }, ticks: { color: '#4e5a70', font: { family: 'DM Mono', size: 10 } } },
              y: { title: { display: true, text: cy, color: '#4e5a70', font: { family: 'DM Mono', size: 11 } }, grid: { color: '#1c2336' }, ticks: { color: '#4e5a70', font: { family: 'DM Mono', size: 10 } } }
            }}
          });
        }, 50);
      }
    }
  }

  // Heatmap
  const numForHeat = numeric.slice(0, 8);
  if (numForHeat.length >= 2) {
    const matrix = correlationMatrix(data, numForHeat);
    document.getElementById('heatmap-card').style.display = '';
    const hc = document.getElementById('heatmap-container');
    let html = '<table class="heatmap-table"><thead><tr><th></th>' + numForHeat.map(c => `<th title="${c}">${c.slice(0, 10)}</th>`).join('') + '</tr></thead><tbody>';
    numForHeat.forEach(r => {
      html += `<tr><th style="text-align:right;padding-right:10px;color:var(--text2);font-size:10px">${r.slice(0, 12)}</th>`;
      numForHeat.forEach(c => {
        const val = matrix[r][c];
        const abs = Math.abs(val);
        const color = val > 0
          ? `rgba(79,142,247,${abs * 0.9})`
          : `rgba(247,90,142,${abs * 0.9})`;
        const textColor = abs > 0.4 ? '#fff' : '#8892a8';
        html += `<td style="background:${color};color:${textColor}" title="${r} × ${c}: ${val}">${val}</td>`;
      });
      html += '</tr>';
    });
    html += '</tbody></table>';
    hc.innerHTML = html;
  } else {
    document.getElementById('heatmap-card').style.display = 'none';
  }

  // ── Pivot Tables
  const pt = document.getElementById('pivot-tables');
  pt.innerHTML = '';

  // For each categorical col crossed with numeric cols
  const pivotCats = categorical.slice(0, 3);
  const pivotNums = numeric.slice(0, 4);

  if (pivotCats.length && pivotNums.length) {
    pivotCats.forEach((cat, ci) => {
      const groups = {};
      data.forEach(r => {
        const key = r[cat] !== null && r[cat] !== '' && r[cat] !== undefined ? String(r[cat]) : '(empty)';
        if (!groups[key]) groups[key] = {};
        pivotNums.forEach(n => {
          if (!groups[key][n]) groups[key][n] = [];
          if (typeof r[n] === 'number' && !isNaN(r[n])) groups[key][n].push(r[n]);
        });
      });

      const keys = Object.keys(groups).slice(0, 20);
      let html = `<div class="section-title" style="margin-top:${ci ? '24px' : '0'}">"${cat}" × Numeric Summary</div>
        <div class="pivot-wrap"><table class="pivot-table"><thead><tr>
        <th>${cat}</th><th>Count</th>`;
      pivotNums.forEach(n => html += `<th>${n} (avg)</th><th>${n} (sum)</th>`);
      html += '</tr></thead><tbody>';

      keys.forEach(k => {
        const g = groups[k];
        const cnt = g[pivotNums[0]] ? g[pivotNums[0]].length : 0;
        html += `<tr><td class="label">${String(k).slice(0, 30)}</td><td class="num">${cnt}</td>`;
        pivotNums.forEach(n => {
          const vals = g[n] || [];
          const avg = vals.length ? (vals.reduce((a, b) => a + b, 0) / vals.length).toFixed(2) : '-';
          const sum = vals.length ? vals.reduce((a, b) => a + b, 0).toFixed(2) : '-';
          html += `<td class="num">${avg}</td><td class="num">${sum}</td>`;
        });
        html += '</tr>';
      });
      html += '</tbody></table></div>';
      pt.innerHTML += html;
    });
  } else {
    pt.innerHTML = '<div class="empty-state">No categorical columns available for pivot tables.</div>';
  }

  // ── Numeric stats pivot
  if (numeric.length) {
    let html = '<div class="section-title" style="margin-top:24px">Numeric Statistics Summary</div><div class="pivot-wrap"><table class="pivot-table"><thead><tr><th>Column</th><th>Count</th><th>Min</th><th>Max</th><th>Mean</th><th>Median</th><th>Std Dev</th><th>Sum</th></tr></thead><tbody>';
    numeric.forEach(c => {
      const s = numStats(data, c);
      html += `<tr><td class="label">${c}</td><td class="num">${s.count}</td><td class="num">${s.min}</td><td class="num">${s.max}</td><td class="num">${s.mean}</td><td class="num">${s.median}</td><td class="num">${s.std}</td><td class="num">${s.sum}</td></tr>`;
    });
    html += '</tbody></table></div>';
    pt.innerHTML += html;
  }

  // ── Data Preview Table
  const dtw = document.getElementById('data-table-wrap');
  const previewData = data.slice(0, 200);
  let tableHtml = '<table class="data-table"><thead><tr>' + cols.map(c => `<th>${c}</th>`).join('') + '</tr></thead><tbody>';
  previewData.forEach(r => {
    tableHtml += '<tr>' + cols.map(c => {
      const v = r[c];
      const display = v === null || v === undefined ? '<span style="color:var(--danger)">null</span>' : String(v).slice(0, 40);
      return `<td>${display}</td>`;
    }).join('') + '</tr>';
  });
  tableHtml += '</tbody></table>';
  dtw.innerHTML = tableHtml;

  // Show dashboard
  document.getElementById('upload-zone').style.display = 'none';
  document.getElementById('dashboard').style.display = 'block';
  switchTab('overview', document.querySelector('.tab-btn'));
}

// ──────────────────────────────────────────────
//  HELPERS
// ──────────────────────────────────────────────
function chartCard(id, title, subtitle, type) {
  return `<div class="chart-card">
    <div class="chart-header">
      <div>
        <div class="chart-title">${title}</div>
        <div class="chart-subtitle">${subtitle}</div>
      </div>
      <span class="chart-type-badge">${type}</span>
    </div>
    <div class="chart-wrap"><canvas id="${id}" height="240"></canvas></div>
  </div>`;
}

function chartOpts(yLabel) {
  return {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: {
      x: { grid: { color: '#1c2336' }, ticks: { color: '#4e5a70', font: { family: 'DM Mono', size: 10 }, maxRotation: 40 } },
      y: { grid: { color: '#1c2336' }, ticks: { color: '#4e5a70', font: { family: 'DM Mono', size: 10 } }, title: { display: !!yLabel, text: yLabel, color: '#4e5a70', font: { family: 'DM Mono', size: 11 } } }
    }
  };
}

function switchTab(name, btn) {
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  if (btn) btn.classList.add('active');
}

function resetDashboard() {
  Object.values(chartRegistry).forEach(c => c.destroy());
  Object.keys(chartRegistry).forEach(k => delete chartRegistry[k]);
  document.getElementById('upload-zone').style.display = 'flex';
  document.getElementById('dashboard').style.display = 'none';
  document.getElementById('file-input').value = '';
  gData = []; gColumns = []; gFileName = '';
}

function showLoading() { document.getElementById('loading-overlay').classList.add('show'); }
function hideLoading() { document.getElementById('loading-overlay').classList.remove('show'); }
</script>
</body>
</html>
