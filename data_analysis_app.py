import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import json
import requests
import re
from datetime import datetime

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #12121a;
    --border: #1e1e2e;
    --accent: #7c3aed;
    --accent2: #06b6d4;
    --text: #e2e8f0;
    --muted: #64748b;
    --success: #10b981;
    --warning: #f59e0b;
}

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

/* Hide default streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container {padding-top: 2rem; max-width: 1200px;}

/* Hero Section */
.hero {
    text-align: center;
    padding: 5rem 2rem 3rem;
    background: radial-gradient(ellipse at 50% 0%, #7c3aed22 0%, transparent 70%);
    border-bottom: 1px solid var(--border);
    margin-bottom: 3rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    background: linear-gradient(135deg, #fff 30%, #7c3aed 70%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
    margin-bottom: 1rem;
}
.hero p {
    color: var(--muted);
    font-size: 1.1rem;
    max-width: 500px;
    margin: 0 auto 2rem;
}

/* Glowing CTA Button */
.cta-btn {
    display: inline-block;
    padding: 1rem 2.5rem;
    background: linear-gradient(135deg, #7c3aed, #6d28d9);
    border: 1px solid #8b5cf6;
    border-radius: 8px;
    color: white !important;
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    text-decoration: none;
    cursor: pointer;
    box-shadow: 0 0 30px #7c3aed44, 0 4px 20px rgba(0,0,0,0.4);
    transition: all 0.3s ease;
    letter-spacing: 0.05em;
}
.cta-btn:hover {
    box-shadow: 0 0 50px #7c3aed88, 0 8px 30px rgba(0,0,0,0.4);
    transform: translateY(-2px);
}

/* Upload Zone */
.upload-zone {
    border: 2px dashed var(--accent);
    border-radius: 16px;
    padding: 3rem;
    text-align: center;
    background: linear-gradient(135deg, #7c3aed08, #06b6d408);
    margin: 2rem 0;
    transition: all 0.3s ease;
}
.upload-zone:hover {
    background: linear-gradient(135deg, #7c3aed15, #06b6d415);
    border-color: #8b5cf6;
}
.upload-icon { font-size: 3rem; margin-bottom: 1rem; }
.upload-zone h3 { font-size: 1.3rem; margin-bottom: 0.5rem; }
.upload-zone p { color: var(--muted); font-size: 0.9rem; }

/* Stats Cards */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}
.stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}
.stat-number {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--accent2);
    display: block;
}
.stat-label {
    font-size: 0.75rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.3rem;
    display: block;
}

/* Analysis Cards */
.analysis-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
}
.analysis-card h4 {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: var(--accent2);
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Insight Box */
.insight-box {
    background: linear-gradient(135deg, #7c3aed15, #06b6d410);
    border: 1px solid #7c3aed44;
    border-left: 3px solid var(--accent);
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin: 0.75rem 0;
    font-size: 0.95rem;
    line-height: 1.6;
}
.insight-box.warning {
    border-left-color: var(--warning);
    background: linear-gradient(135deg, #f59e0b10, transparent);
}
.insight-box.success {
    border-left-color: var(--success);
    background: linear-gradient(135deg, #10b98110, transparent);
}

/* Progress Bar */
.progress-container {
    background: var(--border);
    border-radius: 4px;
    height: 6px;
    margin: 0.5rem 0;
    overflow: hidden;
}
.progress-bar {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    transition: width 0.5s ease;
}

/* Section Labels */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.2em;
    margin-bottom: 0.5rem;
    display: block;
}

/* AI Response Styling */
.ai-response {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1rem;
    line-height: 1.8;
    font-size: 0.95rem;
}
.ai-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: linear-gradient(135deg, #7c3aed22, #06b6d422);
    border: 1px solid #7c3aed44;
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
    color: var(--accent2);
    margin-bottom: 1rem;
    letter-spacing: 0.05em;
}

/* Streamlit overrides */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
    border: 1px solid #8b5cf6 !important;
    color: white !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 1.5rem !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 20px #7c3aed33 !important;
}
.stButton > button:hover {
    box-shadow: 0 0 40px #7c3aed66 !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
}

.stTextArea textarea, .stTextInput input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px #7c3aed33 !important;
}

.stDataFrame { border-radius: 12px; overflow: hidden; }
.stTabs [data-baseweb="tab"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent2) !important;
}
div[data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace !important;
    color: var(--accent2) !important;
}

/* Divider */
.styled-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

# ─── Helper: Claude API ──────────────────────────────────────────────────────
def ask_claude(system_prompt, user_prompt):
    headers = {"Content-Type": "application/json"}
    body = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1500,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}]
    }
    try:
        resp = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=body, timeout=60)
        data = resp.json()
        return data["content"][0]["text"]
    except Exception as e:
        return f"Error contacting AI: {str(e)}"

# ─── Data Helpers ────────────────────────────────────────────────────────────
def load_data(file):
    name = file.name.lower()
    try:
        if name.endswith(".csv"):
            df = pd.read_csv(file, encoding="utf-8")
        elif name.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file)
        elif name.endswith(".json"):
            df = pd.read_json(file)
        elif name.endswith(".tsv"):
            df = pd.read_csv(file, sep="\t", encoding="utf-8")
        else:
            return None
    except UnicodeDecodeError:
        # Retry with latin-1 for CSV/TSV if UTF-8 fails
        file.seek(0)
        if name.endswith(".csv"):
            df = pd.read_csv(file, encoding="latin-1")
        elif name.endswith(".tsv"):
            df = pd.read_csv(file, sep="\t", encoding="latin-1")
        else:
            return None

    # Auto-convert columns that look numeric but were read as strings
    for col in df.columns:
        if df[col].dtype == object:
            # Strip whitespace
            df[col] = df[col].astype(str).str.strip()
            # Try converting to numeric (handles commas like "1,234")
            converted = df[col].str.replace(",", "", regex=False)
            converted = pd.to_numeric(converted, errors="coerce")
            # Only replace if most values converted successfully (>50%)
            if converted.notna().sum() / max(len(df), 1) > 0.5:
                df[col] = converted

    return df

def df_summary(df):
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    missing = df.isnull().sum().sum()
    dup = df.duplicated().sum()
    return {
        "rows": len(df),
        "cols": len(df.columns),
        "numeric": len(numeric_cols),
        "categorical": len(cat_cols),
        "missing": int(missing),
        "duplicates": int(dup),
        "numeric_cols": numeric_cols,
        "cat_cols": cat_cols,
    }

def build_context(df, summary):
    ctx = f"""Dataset: {summary['rows']} rows × {summary['cols']} columns
Numeric columns ({summary['numeric']}): {', '.join(summary['numeric_cols'][:10])}
Categorical columns ({summary['categorical']}): {', '.join(summary['cat_cols'][:10])}
Missing values: {summary['missing']}
Duplicates: {summary['duplicates']}

Basic Statistics:
{df.describe().to_string()}

First 5 rows:
{df.head().to_string()}
"""
    return ctx

# ─── Session State Init ───────────────────────────────────────────────────────
for key in ["show_upload", "df", "analysis_done", "ai_insights", "user_question", "ai_answer"]:
    if key not in st.session_state:
        st.session_state[key] = None if key not in ["show_upload", "analysis_done"] else False

# ─── HERO SECTION ─────────────────────────────────────────────────────────────
if not st.session_state.show_upload:
    st.markdown("""
    <div class="hero">
        <h1>AI Data<br>Analyst</h1>
        <p>Drop your data. Get instant AI-powered insights, visualizations, and deep analysis.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚡  Start Analysis →", use_container_width=True):
            st.session_state.show_upload = True
            st.rerun()

        st.markdown("""
        <div style="display:flex; gap:2rem; justify-content:center; margin-top:3rem; flex-wrap:wrap;">
            <div style="text-align:center">
                <div style="font-size:1.5rem">📊</div>
                <div style="font-size:0.8rem; color:#64748b; margin-top:0.3rem">CSV · Excel · JSON · TSV</div>
            </div>
            <div style="text-align:center">
                <div style="font-size:1.5rem">🤖</div>
                <div style="font-size:0.8rem; color:#64748b; margin-top:0.3rem">AI-Powered Insights</div>
            </div>
            <div style="text-align:center">
                <div style="font-size:1.5rem">📈</div>
                <div style="font-size:0.8rem; color:#64748b; margin-top:0.3rem">Auto Visualizations</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─── UPLOAD & ANALYSIS SECTION ────────────────────────────────────────────────
else:
    st.markdown("""
    <div style="padding:2rem 0 1rem;">
        <span class="section-label">⚡ AI Data Analyst</span>
        <h2 style="font-size:1.8rem; font-weight:800; margin:0;">Upload Your Data</h2>
    </div>
    """, unsafe_allow_html=True)

    # ── File Uploader ──
    if st.session_state.df is None:
        st.markdown("""
        <div class="upload-zone">
            <div class="upload-icon">📂</div>
            <h3>Drop your dataset here</h3>
            <p>Supports CSV, Excel (.xlsx), JSON, TSV</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Choose a file",
            type=["csv", "xlsx", "xls", "json", "tsv"],
            label_visibility="collapsed"
        )

        col_a, col_b = st.columns([3, 1])
        with col_b:
            if st.button("← Back to Home", use_container_width=True):
                st.session_state.show_upload = False
                st.rerun()

        if uploaded:
            df = load_data(uploaded)
            if df is not None:
                st.session_state.df = df
                st.session_state.analysis_done = False
                st.session_state.ai_insights = None
                st.success(f"✅ Loaded **{uploaded.name}** — {len(df):,} rows × {len(df.columns)} columns")

                col1, col2 = st.columns([2, 1])
                with col1:
                    if st.button("🚀  Run Full Analysis", use_container_width=True):
                        st.session_state.analysis_done = True
                        st.rerun()
            else:
                st.error("Could not parse the file. Please try a different format.")

    # ── Analysis Results ──
    else:
        df = st.session_state.df
        summary = df_summary(df)

        # Quick Stats Bar
        st.markdown(f"""
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-number">{summary['rows']:,}</span>
                <span class="stat-label">Rows</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{summary['cols']}</span>
                <span class="stat-label">Columns</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{summary['numeric']}</span>
                <span class="stat-label">Numeric</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{summary['missing']}</span>
                <span class="stat-label">Missing</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{summary['duplicates']}</span>
                <span class="stat-label">Duplicates</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_reset, col_analyze = st.columns([1, 2])
        with col_reset:
            if st.button("🔄 Upload New File"):
                st.session_state.df = None
                st.session_state.analysis_done = False
                st.session_state.ai_insights = None
                st.rerun()
        with col_analyze:
            if not st.session_state.analysis_done:
                if st.button("🚀  Run Full Analysis", use_container_width=True):
                    st.session_state.analysis_done = True
                    st.rerun()

        st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)

        # ── Tabs ──
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Data Preview", "📊 Visualizations", "🤖 AI Insights", "💬 Ask AI"])

        with tab1:
            st.markdown('<div class="analysis-card"><h4>🗂 Dataset Preview</h4>', unsafe_allow_html=True)
            st.dataframe(df.head(50), use_container_width=True, height=350)
            st.markdown('</div>', unsafe_allow_html=True)

            col_l, col_r = st.columns(2)
            with col_l:
                st.markdown('<div class="analysis-card"><h4>📐 Column Types</h4>', unsafe_allow_html=True)
                dtype_df = pd.DataFrame({"Column": df.columns, "Type": df.dtypes.values.astype(str),
                                         "Non-Null": df.count().values, "Null%": (df.isnull().mean()*100).round(1).values})
                st.dataframe(dtype_df, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col_r:
                if summary['numeric_cols']:
                    st.markdown('<div class="analysis-card"><h4>📈 Descriptive Stats</h4>', unsafe_allow_html=True)
                    st.dataframe(df[summary['numeric_cols']].describe().round(3), use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            if not summary['numeric_cols']:
                st.info("No numeric columns found for visualization.")
            else:
                sns.set_theme(style="dark", palette="muted")
                plt.rcParams.update({"figure.facecolor": "#12121a", "axes.facecolor": "#0a0a0f",
                                     "text.color": "#e2e8f0", "axes.labelcolor": "#e2e8f0",
                                     "xtick.color": "#64748b", "ytick.color": "#64748b",
                                     "axes.edgecolor": "#1e1e2e", "grid.color": "#1e1e2e"})

                # Distribution plots
                st.markdown('<div class="analysis-card"><h4>📊 Distributions</h4>', unsafe_allow_html=True)
                cols_to_plot = summary['numeric_cols'][:6]
                n = len(cols_to_plot)
                ncols = min(3, n)
                nrows = (n + ncols - 1) // ncols
                fig, axes = plt.subplots(nrows, ncols, figsize=(5*ncols, 4*nrows), facecolor="#12121a")
                axes = np.array(axes).flatten() if n > 1 else [axes]
                colors = ["#7c3aed", "#06b6d4", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"]
                for i, col in enumerate(cols_to_plot):
                    axes[i].hist(df[col].dropna(), bins=30, color=colors[i % len(colors)], alpha=0.8, edgecolor="none")
                    axes[i].set_title(col, fontsize=11, color="#e2e8f0", pad=8)
                    axes[i].set_facecolor("#0a0a0f")
                for j in range(i+1, len(axes)):
                    axes[j].set_visible(False)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
                st.markdown('</div>', unsafe_allow_html=True)

                # Correlation heatmap
                if len(summary['numeric_cols']) >= 2:
                    st.markdown('<div class="analysis-card"><h4>🔥 Correlation Matrix</h4>', unsafe_allow_html=True)
                    corr = df[summary['numeric_cols']].corr()
                    fig2, ax2 = plt.subplots(figsize=(max(6, len(summary['numeric_cols'])), max(5, len(summary['numeric_cols'])-1)),
                                              facecolor="#12121a")
                    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdPu", ax=ax2,
                                linewidths=0.5, linecolor="#0a0a0f",
                                annot_kws={"size": 9}, cbar_kws={"shrink": 0.8})
                    ax2.set_facecolor("#12121a")
                    plt.tight_layout()
                    st.pyplot(fig2)
                    plt.close()
                    st.markdown('</div>', unsafe_allow_html=True)

                # Missing Values
                if summary['missing'] > 0:
                    st.markdown('<div class="analysis-card"><h4>❓ Missing Values by Column</h4>', unsafe_allow_html=True)
                    missing_s = df.isnull().sum()
                    missing_s = missing_s[missing_s > 0].sort_values(ascending=True)
                    fig3, ax3 = plt.subplots(figsize=(8, max(3, len(missing_s)*0.4)), facecolor="#12121a")
                    ax3.barh(missing_s.index, missing_s.values, color="#ef4444", alpha=0.8)
                    ax3.set_facecolor("#0a0a0f")
                    ax3.set_xlabel("Missing Count", color="#64748b")
                    plt.tight_layout()
                    st.pyplot(fig3)
                    plt.close()
                    st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            if st.session_state.analysis_done and st.session_state.ai_insights is None:
                with st.spinner("🤖 AI is analyzing your dataset..."):
                    ctx = build_context(df, summary)
                    sys_p = """You are an expert data scientist providing concise, actionable insights. 
Format your response with clear sections using emoji headers. Be specific with numbers. 
Identify patterns, anomalies, recommendations. Keep it structured and under 600 words."""
                    user_p = f"Analyze this dataset and provide: key findings, data quality issues, patterns/trends, and 3 actionable recommendations.\n\n{ctx}"
                    st.session_state.ai_insights = ask_claude(sys_p, user_p)

            if st.session_state.ai_insights:
                st.markdown(f"""
                <div class="ai-response">
                    <div class="ai-badge">🤖 Claude AI Analysis</div>
                    <div style="white-space:pre-wrap">{st.session_state.ai_insights}</div>
                </div>
                """, unsafe_allow_html=True)
            elif not st.session_state.analysis_done:
                st.markdown("""
                <div class="insight-box">
                    💡 Click <strong>"Run Full Analysis"</strong> above to get AI-powered insights about your dataset.
                </div>
                """, unsafe_allow_html=True)

        with tab4:
            st.markdown('<div class="analysis-card"><h4>💬 Ask Anything About Your Data</h4>', unsafe_allow_html=True)
            question = st.text_area(
                "Your question",
                placeholder="e.g. What are the main outliers? Which columns are most correlated? What's causing the missing values?",
                height=100,
                label_visibility="collapsed"
            )
            if st.button("🔍 Ask AI", use_container_width=False):
                if question.strip():
                    with st.spinner("Thinking..."):
                        ctx = build_context(df, summary)
                        sys_p = "You are a data analyst expert. Answer questions about the dataset concisely and accurately. Use specific numbers from the data."
                        user_p = f"Dataset context:\n{ctx}\n\nQuestion: {question}"
                        answer = ask_claude(sys_p, user_p)
                        st.session_state.ai_answer = (question, answer)
                else:
                    st.warning("Please enter a question first.")
            st.markdown('</div>', unsafe_allow_html=True)

            if st.session_state.ai_answer:
                q, a = st.session_state.ai_answer
                st.markdown(f"""
                <div style="margin-top:1rem">
                    <div class="insight-box" style="font-size:0.9rem; color:#64748b">❓ {q}</div>
                    <div class="ai-response">
                        <div class="ai-badge">🤖 Claude AI Answer</div>
                        <div style="white-space:pre-wrap">{a}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
