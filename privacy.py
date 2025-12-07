# privacy1.py — PRIVACY MIRROR 
# Run: streamlit run privacy1.py

import os, re, time, csv, io, base64, secrets, string
from pathlib import Path
from typing import Optional, List, Dict, Any
from collections import Counter
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# PDF library (pip install fpdf)
try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="PRIVACY MIRROR",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- GLOBAL UI & STYLES ----------
def inject_global_ui():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Aleo:wght@400;700&family=Noto+Sans+TC:wght@400;600&family=Playfair+Display:wght@600;700&family=Poppins:wght@400;500;600;700&display=swap');

        .block-container { max-width: 1100px !important; margin: 0 auto !important; padding-top: 80px !important; }
        html, body, [class*="css"] { font-family: 'Poppins', sans-serif !important; }
        h1,h2,h3,h4,h5,h6,p,span,div,label, .stMarkdown, .stTextInput label {
          color: #ffffff !important;
        }

        /* ---------- GLOBAL BUTTONS (NORMAL) ---------- */
        .stButton>button {
          background: #ffffff !important;
          color:#000000 !important;
          font-weight:600 !important;
          border-radius:999px !important;
          border:none !important;
          padding:0.5rem 1.6rem !important;
          font-size:14px !important;
          letter-spacing:0.5px !important;
          text-shadow:none !important;
          transition: transform .18s ease, box-shadow .18s ease, background .18s ease !important;
        }
        .stButton>button * {
          color:#000000 !important;
          text-shadow:none !important;
          font-family:'Poppins', sans-serif !important;
        }
        .stButton>button:hover {
          transform: translateY(-1px);
          background:#f5f5f5 !important;
          box-shadow:0 8px 18px rgba(0,0,0,.35) !important;
        }

        /* ---------- DOWNLOAD BUTTONS (ORANGE) ---------- */
        [data-testid="stDownloadButton"] > button {
          background: linear-gradient(135deg, #ffd8a8, #ffb566) !important;
          color: #1a1a1a !important;
          font-weight: 700 !important;
          border-radius: 999px !important;
          border: none !important;
          box-shadow: 0 8px 18px rgba(0,0,0,.25) !important;
          padding: 0.4rem 1.4rem !important;
          font-size:14px !important;
          text-shadow:none !important;
        }
        [data-testid="stDownloadButton"] > button * {
          color:#1a1a1a !important;
          text-shadow:none !important;
          font-family:'Poppins', sans-serif !important;
        }
        [data-testid="stDownloadButton"] > button:hover {
          filter: brightness(1.03);
          transform: translateY(-1px);
        }

        /* Fixed top nav bar */
        .pm-topbar {
          position: fixed;
          top: 0; left: 0; right: 0;
          height: 64px;
          display:flex;
          align-items:center;
          justify-content:center;
          z-index: 1100;
          pointer-events:none;
        }
        .pm-topbar-inner {
          max-width: 1100px;
          width: 100%;
          display:flex;
          align-items:center;
          justify-content:space-between;
          padding: 0 1.2rem;
          pointer-events:auto;
        }
        .pm-logo {
          font-family:'Playfair Display', serif;
          font-size:22px;
          font-weight:600;
          letter-spacing:2px;
        }
        .pm-logo span {
          padding:4px 9px;
          border-radius:999px;
          border:1px solid rgba(255,255,255,0.2);
          backdrop-filter: blur(6px);
        }
        .pm-nav {
          display:flex;
          gap:1rem;
          align-items:center;
        }
        .pm-nav-item {
          font-size:13px;
          text-transform:uppercase;
          letter-spacing:1px;
          padding:6px 10px;
          border-radius:999px;
          border:1px solid transparent;
          cursor:pointer;
        }
        .pm-nav-item.pm-active {
          border-color:rgba(255,255,255,0.7);
          background:rgba(0,0,0,0.4);
        }
        .pm-nav-item:hover {
          background:rgba(0,0,0,0.5);
        }

        /* Hide native radio label */
        div[data-testid="stRadio"] > label { display:none; }
        div[data-testid="stRadio"] div[role="radiogroup"] { display:none; }

        /* Footer */
        .pm-footer {
          position: fixed;
          left:50%;
          transform:translateX(-50%);
          bottom:12px;
          z-index:9999;
          font-family:'Aleo', serif;
          font-size:12px;
          color:#f3f4f6;
          opacity:.95;
          letter-spacing:0.5px;
        }

        /* Feature tiles on hero */
        .pm-feature-row {
          display:flex;
          flex-wrap:wrap;
          gap:18px;
          margin-top:32px;
        }
        .pm-feature-tile {
          flex:1 1 220px;
          min-width:220px;
          background:rgba(0,0,0,0.72);
          border-radius:18px;
          padding:16px 18px;
          border:1px solid rgba(255,255,255,0.12);
          box-shadow:0 8px 22px rgba(0,0,0,0.5);
        }
        .pm-feature-title {
          font-size:14px;
          text-transform:uppercase;
          letter-spacing:1px;
          margin-bottom:6px;
        }
        .pm-feature-body {
          font-size:13px;
          opacity:0.9;
        }

        /* Scan card (slide 2) */
        .pm-form-card {
          background:rgba(0,0,0,0.78);
          border-radius:20px;
          padding:22px 24px;
          border:1px solid rgba(255,255,255,0.14);
          box-shadow:0 16px 40px rgba(0,0,0,0.7);
        }
        .pm-note {
          margin-top:6px;
          font-weight:800;
          color:#fff !important;
          font-family:"Franklin Gothic Demi","Franklin Gothic Medium","Arial Black",Arial,sans-serif !important;
          letter-spacing:.2px;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] { background:#000 !important; color:#fff !important; }
        [data-testid="stSidebar"] * { color:#fff !important; }
        [data-testid="stSidebar"] svg { fill:#000 !important; color:#000 !important; }
        .pm-side-card {
          background: rgba(255,255,255,0.05);
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 12px;
          padding: 12px 14px;
          margin-bottom: 10px;
        }
        button[data-testid="baseButton-headerSidebarToggle"],
        button[data-testid="baseButton-headerHamburger"],
        button[aria-label="Toggle sidebar"] {
          background: rgba(0,0,0,0.65) !important;
          border-radius: 12px !important;
          border: 1px solid rgba(255,255,255,0.25) !important;
          box-shadow: 0 4px 10px rgba(0,0,0,0.45) !important;
          padding: 6px 8px !important;
        }
        button[data-testid="baseButton-headerSidebarToggle"] svg,
        button[data-testid="baseButton-headerHamburger"] svg,
        button[aria-label="Toggle sidebar"] svg {
          color:#000 !important; fill:#000 !important;
        }

        /* Summary strip */
        .pm-summary {
          display:flex;
          gap:16px;
          align-items:center;
          justify-content:space-between;
          padding:16px;
          border-radius:16px;
          background:rgba(0,0,0,0.8);
          border:1px solid rgba(255,255,255,0.14);
          box-shadow:0 16px 40px rgba(0,0,0,0.7);
          margin: 8px 0 14px 0;
        }
        .pm-summary-right { display:flex; gap:18px; align-items:center; flex-wrap:wrap; }
        .pm-kpi {
          min-width: 160px;
          background: rgba(255,255,255,0.04);
          border:1px solid rgba(255,255,255,0.12);
          border-radius:14px;
          padding:10px 14px;
          text-align:center;
        }
        .pm-kpi .kpi-label { font-size:12px; opacity:.85; }
        .pm-kpi .kpi-value { font-size:22px; font-weight:800; margin-top:2px; }

        /* Timeline */
        .pm-timeline { position:relative; margin: 10px 0 0 0; padding-left:22px; }
        .pm-timeline::before {
          content:''; position:absolute; left:50%; top:0; bottom:0;
          width:2px; background: linear-gradient(180deg,#111827,#3b82f6,#111827); opacity:.7;
        }
        .pm-node { display:flex; gap:24px; align-items:flex-start; margin: 18px 0; }
        .pm-node.left  { flex-direction: row-reverse; }
        .pm-bubble {
          position:relative; z-index:2; min-width:70px; height:70px; border-radius:999px;
          background: radial-gradient(120% 120% at 30% 25%, #2563eb, #020617 75%);
          border:1px solid rgba(255,255,255,.2); color:#fff; font-weight:800;
          display:flex; align-items:center; justify-content:center; text-align:center; padding:8px 10px;
          box-shadow: 0 16px 36px rgba(0,0,0,.8); white-space: pre-line;
        }
        .pm-panel {
          flex:1; background: rgba(15,23,42,0.96);
          border:1px solid rgba(148,163,184,.35); border-radius:16px; padding:18px 18px;
          box-shadow: 0 16px 40px rgba(0,0,0,0.75);
        }
        .pm-title { font-family:'Playfair Display', serif; font-size:19px; font-weight:700; margin-bottom:4px; }
        .pm-meta { font-size:12px; opacity:.85; margin-bottom:8px; }
        .pm-list li { margin:3px 0; }

        /* Safety tiles */
        .pm-safety-row {
          display:flex;
          flex-wrap:wrap;
          gap:16px;
          margin-top:10px;
          margin-bottom:18px;
        }
        .pm-safety-card {
          flex:1 1 220px;
          min-width:220px;
          background:rgba(0,0,0,0.82);
          border-radius:18px;
          padding:14px 16px;
          border:1px solid rgba(148,163,184,0.35);
          box-shadow:0 14px 32px rgba(0,0,0,0.75);
        }
        .pm-safety-card h4 {
          font-size:15px;
          text-transform:uppercase;
          letter-spacing:1px;
          margin-bottom:4px;
        }
        .pm-safety-card p {
          font-size:13px;
          opacity:0.9;
        }

        .pm-footer { position: fixed; left:50%; transform:translateX(-50%); bottom:12px; z-index:9999;
                     font-family:'Aleo', serif; font-size:12px; color:#f3f4f6; opacity:.95; letter-spacing:0.5px; }
        </style>
        <div class="pm-footer">© 2025 PRIVACY MIRROR. All rights reserved.</div>
        """,
        unsafe_allow_html=True,
    )

def render_topbar():
    step = st.session_state.get("step", 1)
    labels = {1: "Home", 2: "Scan", 3: "Results", 4: "Safety"}

    st.markdown(
        f"""
        <div class="pm-topbar">
          <div class="pm-topbar-inner">
            <div class="pm-logo"><span>PRIVACY&nbsp;MIRROR</span></div>
            <div class="pm-nav">
              <div class="pm-nav-item {'pm-active' if step==1 else ''}" onclick="window.parent.postMessage('pm-nav-1','*')">{labels[1]}</div>
              <div class="pm-nav-item {'pm-active' if step==2 else ''}" onclick="window.parent.postMessage('pm-nav-2','*')">{labels[2]}</div>
              <div class="pm-nav-item {'pm-active' if step==3 else ''}" onclick="window.parent.postMessage('pm-nav-3','*')">{labels[3]}</div>
              <div class="pm-nav-item {'pm-active' if step==4 else ''}" onclick="window.parent.postMessage('pm-nav-4','*')">{labels[4]}</div>
            </div>
          </div>
        </div>
        <script>
        window.addEventListener('message', (event) => {{
          const msg = event.data;
          if (['pm-nav-1','pm-nav-2','pm-nav-3','pm-nav-4'].includes(msg)) {{
            window.parent.postMessage({{isStreamlitMessage: true, type: msg}}, '*');
          }}
        }});
        </script>
        """,
        unsafe_allow_html=True,
    )

def render_hidden_nav_state():
    step = st.session_state.get("step", 1)
    idx = {1: 0, 2: 1, 3: 2, 4: 3}[step]
    st.radio(
        "Navigation",
        ["Home", "Scan", "Results", "Safety"],
        index=idx,
        key="top_nav",
        label_visibility="collapsed",
    )

def render_sidebar():
    with st.sidebar:
        st.markdown("### 🛡️ Privacy Mirror")
        st.markdown(
            '<div class="pm-side-card">'
            "<b>About:</b> Check if your email or phone appears in known public breach datasets. "
            "Results are fetched live from trusted sources. We never store your data."
            "</div>",
            unsafe_allow_html=True,
        )
        with st.expander("❓ FAQ"):
            st.markdown(
                """
**Do you store my email or phone?**  
No. Everything stays in this browser session. We don’t log or save what you type.

**Are these results 100% complete?**  
No tool can see everything. We show what major public breach datasets report for your input.

**Is it safe to type my password here?**  
We don’t ask for real account passwords. Use the built-in generator to create strong new ones.
                """
            )

def set_background(image_filename: str, step: int) -> None:
    """Lighter overlay so the original background images are more visible."""
    p = Path(image_filename)
    if not p.exists():
        return
    encoded = base64.b64encode(p.read_bytes()).decode()
    st.markdown(
        f"""
        <style>
        @keyframes fadeZoom-{step} {{
          0% {{opacity:0; transform:scale(1.02);}}
          100% {{opacity:1; transform:scale(1);}}
        }}
        .stApp {{
          background-image:
            linear-gradient(145deg, rgba(0,0,0,0.45), rgba(0,0,0,0.35)),
            url("data:image/jpeg;base64,{encoded}");
          background-size: cover;
          background-position: center;
          background-repeat: no-repeat;
          animation: fadeZoom-{step} 0.6s ease both;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------- STATE ----------
if "step" not in st.session_state:
    st.session_state.step = 1
if "inputs" not in st.session_state:
    st.session_state.inputs = {}
if "settings" not in st.session_state:
    st.session_state.settings = {
        "hibp_key": os.getenv("HIBP_API_KEY", "").strip(),
        "dehashed_key": "",
        "animation_gif": "hero.gif",
        "privacy_mode": True,
    }
if "results" not in st.session_state:
    st.session_state.results = {}
if "generated_password" not in st.session_state:
    st.session_state.generated_password = ""
if "phone_error" not in st.session_state:
    st.session_state.phone_error = ""

# ---------- HELPERS ----------
def normalize_phone_basic(raw: str) -> Optional[str]:
    if raw is None:
        return None
    s = raw.strip()
    s = re.sub(r"[^\d+]", "", s)
    if s.startswith("00"):
        s = "+" + s[2:]
    if s.startswith("+") and s[1:].isdigit() and 8 <= len(s[1:]) <= 15:
        return s
    return None

def get_hibp_key() -> str:
    k = st.session_state.settings.get("hibp_key", "").strip()
    if k:
        return k
    try:
        k = st.secrets.get("HIBP_API_KEY", "")
        if k:
            return k.strip()
    except Exception:
        pass
    return os.getenv("HIBP_API_KEY", "").strip()

def get_dehashed_creds():
    user = ""
    key = ""
    try:
        user = st.secrets.get("DEHASHED_USER", "")
        key = st.secrets.get("DEHASHED_KEY", "")
    except Exception:
        pass
    if not user:
        user = os.getenv("DEHASHED_USER", "")
    if not key:
        key = os.getenv("DEHASHED_KEY", "")
    return user.strip(), key.strip()

def check_email_hibp(email: str, timeout: int = 10) -> Optional[List[Dict[str, Any]]]:
    api_key = get_hibp_key()
    if not api_key or not email:
        return None
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{requests.utils.quote(email)}"
    headers = {"hibp-api-key": api_key, "user-agent": "PrivacyMirror/1.0"}
    params = {"truncateResponse": False}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=timeout)
        if r.status_code == 404:
            return []
        if r.status_code in (401, 403, 429):
            return None
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException:
        return None

def check_phone_dehashed(phone: str, timeout: int = 12) -> Optional[Dict[str, Any]]:
    st.session_state.phone_error = ""
    user, key = get_dehashed_creds()
    if not user or not key:
        st.session_state.phone_error = "provider credentials are not configured."
        return None
    if not phone:
        st.session_state.phone_error = "no phone number was provided."
        return None

    url = "https://api.dehashed.com/search"
    params = {"query": f"phone:{phone}"}
    headers = {"Accept": "application/json"}

    try:
        r = requests.get(
            url,
            params=params,
            auth=HTTPBasicAuth(user, key),
            headers=headers,
            timeout=timeout,
        )

        if r.status_code == 404:
            return {"entries": []}

        if r.status_code in (401, 403):
            st.session_state.phone_error = "provider did not accept the configured credentials."
            return None

        r.raise_for_status()
        return r.json()

    except requests.exceptions.Timeout:
        st.session_state.phone_error = "network timeout while contacting phone breach provider."
        return None
    except requests.exceptions.RequestException as e:
        st.session_state.phone_error = f"network or provider error: {e}"
        return None

def severity_for(classes: List[str]) -> str:
    txt = " ".join(c.lower() for c in (classes or []))
    if "password" in txt:
        return "high"
    if any(k in txt for k in ["phone", "credit", "token", "ssn", "dob", "address"]):
        return "med"
    return "low"

def risk_score(breaches: List[Dict[str, Any]]) -> int:
    if breaches is None:
        return 50
    count = len(breaches)
    sens = 0
    for b in breaches or []:
        for c in b.get("DataClasses", []) or []:
            if any(tok in c.lower() for tok in ["password", "phone", "credit", "token", "ssn"]):
                sens += 1
    return min(100, count * 12 + sens * 6)

def compute_stats(breaches: List[Dict[str, Any]]):
    total = len(breaches)
    records = 0
    types_counter = Counter()
    hi = md = lo = 0
    for b in breaches:
        try:
            records += int(b.get("PwnCount") or 0)
        except Exception:
            pass
        classes = b.get("DataClasses", []) or []
        types_counter.update([c.strip() for c in classes if c])
        sev = severity_for(classes)
        if sev == "high":
            hi += 1
        elif sev == "med":
            md += 1
        else:
            lo += 1
    top = types_counter.most_common(8)
    return {
        "total": total,
        "records": records,
        "high": hi,
        "med": md,
        "low": lo,
        "unique_types": len(types_counter),
        "top_types": top,
    }

def breaches_csv_bytes(breaches: List[Dict[str, Any]]) -> bytes:
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["Name", "Domain", "BreachDate", "PwnCount", "DataClasses", "Description"])
    for b in breaches:
        w.writerow(
            [
                b.get("Name", ""),
                b.get("Domain", ""),
                b.get("BreachDate", ""),
                b.get("PwnCount", ""),
                "; ".join(b.get("DataClasses", []) or []),
                (b.get("Description") or "").replace("\n", " "),
            ]
        )
    return out.getvalue().encode("utf-8")

def build_pdf_report(email: str, stats: Dict[str, Any], breaches: List[Dict[str, Any]], risk: int) -> Optional[bytes]:
    if FPDF is None:
        return None

    def t(s: Any) -> str:
        if s is None:
            s = ""
        if not isinstance(s, str):
            s = str(s)
        s = s.replace("—", "-").replace("–", "-").replace("“", '"').replace("”", '"').replace("’", "'")
        return s.encode("latin-1", "replace").decode("latin-1")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, t("Privacy Mirror — Exposure Report"), ln=True)

    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, t(f"Email scanned: {email or 'N/A'}"), ln=True)
    pdf.cell(0, 6, t(f"Generated at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"), ln=True)
    pdf.ln(4)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 7, t("Summary"), ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, t(f"Risk score: {risk}/100"), ln=True)
    pdf.cell(0, 6, t(f"Total breaches: {stats['total']}"), ln=True)
    pdf.cell(0, 6, t(f"Estimated exposed records: {stats['records']}"), ln=True)
    pdf.cell(0, 6, t(f"High/Med/Low severity: {stats['high']} / {stats['med']} / {stats['low']}"), ln=True)
    pdf.ln(4)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 7, t("Breaches"), ln=True)
    pdf.set_font("Arial", "", 10)

    for b in breaches:
        pdf.ln(2)
        name = t(b.get("Name", "Unknown"))
        domain = t(b.get("Domain", ""))
        date = t(b.get("BreachDate", "?"))
        pwn = t(b.get("PwnCount", "?"))

        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, t(f"- {name} ({domain})"), ln=True)

        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 5, t(f"Date: {date}  Records: {pwn}"), ln=True)

        classes = "; ".join(b.get("DataClasses", []) or [])
        if classes:
            pdf.multi_cell(0, 5, t(f"Data types: {classes}"))

        desc = (b.get("Description") or "").replace("\r", " ").replace("\n", " ")
        if desc:
            short_desc = desc[:400] + ("..." if len(desc) > 400 else "")
            pdf.multi_cell(0, 5, t(f"Details: {short_desc}"))

    pdf.ln(4)
    pdf.set_font("Arial", "I", 9)
    pdf.multi_cell(
        0,
        5,
        t(
            "This report is based on public breach datasets. "
            "Absence of a breach in this report does not guarantee that no compromise has occurred."
        ),
    )

    pdf_bytes = pdf.output(dest="S").encode("latin-1", "replace")
    return pdf_bytes

def run_checks(email: str, phone: str):
    st.markdown("<style>.pm-footer{display:none !important}</style>", unsafe_allow_html=True)
    st.session_state.results = {"email": None, "phone": None, "meta": {}}
    progress = st.progress(0)
    status = st.empty()

    status.info("Preparing secure scan…")
    for i in range(1, 21):
        time.sleep(0.003)
        progress.progress(i)

    if email:
        status.info("Checking email against breach providers…")
        for i in range(21, 46):
            time.sleep(0.004)
            progress.progress(i)
        st.session_state.results["email"] = check_email_hibp(email)
        progress.progress(60)

    if phone:
        status.info("Checking phone against leak datasets…")
        for i in range(60, 85):
            time.sleep(0.004)
            progress.progress(i)
        st.session_state.results["phone"] = check_phone_dehashed(phone)
        progress.progress(92)

    status.success("Finalizing results…")
    time.sleep(0.03)
    progress.progress(100)
    status.empty()
    time.sleep(0.02)

    eb = st.session_state.results.get("email")
    st.session_state.results["meta"]["risk"] = risk_score(eb if isinstance(eb, list) else [])
    st.session_state.step = 3
    st.rerun()

def render_score_gauge(value: int, label: str = "Risk Score"):
    value = max(0, min(int(value), 100))
    radius, stroke = 58, 10
    circ = 2 * 3.14159 * radius
    dash = circ * value / 100.0
    gap = circ - dash
    col = "#10b981" if value <= 30 else ("#f59e0b" if value <= 70 else "#ef4444")

    html = f"""
    <div style="width:160px;height:190px;display:flex;align-items:center;justify-content:center;">
      <div style="position:relative;width:140px;height:140px;">
        <svg width="140" height="140" viewBox="0 0 140 140" style="position:absolute;left:0;top:0">
          <defs>
            <linearGradient id="pm-grad" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="{col}" stop-opacity="0.9"/>
              <stop offset="100%" stop-color="#ffffff" stop-opacity="0.2"/>
            </linearGradient>
          </defs>
          <circle cx="70" cy="70" r="{radius}" stroke="rgba(255,255,255,0.15)" stroke-width="{stroke}" fill="none"/>
          <circle cx="70" cy="70" r="{radius}" stroke="url(#pm-grad)" stroke-width="{stroke}" fill="none"
                  stroke-linecap="round" stroke-dasharray="{dash} {gap}" transform="rotate(-90 70 70)"/>
        </svg>
        <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
                    color:#fff;text-shadow:0 0 6px rgba(0,0,0,.45);">
          <div style="font-weight:900;font-size:26px;line-height:1;">{value}</div>
          <div style="font-size:12px;opacity:.85;margin-top:4px;"><b>{label}</b></div>
        </div>
      </div>
    </div>
    """
    components.html(html, height=200, scrolling=False)

def _fmt_month_year(date_str: str) -> str:
    try:
        d = datetime.fromisoformat(date_str)
        return d.strftime("%b\n%Y")
    except Exception:
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d")
            return d.strftime("%b\n%Y")
        except Exception:
            return date_str or "—"

def render_breach_detail(b: Dict[str, Any], align_left: bool = False):
    name = b.get("Name") or b.get("Title") or "Unknown breach"
    date = b.get("BreachDate") or b.get("AddedDate") or "—"
    bubble = _fmt_month_year(date)
    domain = b.get("Domain") or "—"
    pwn = b.get("PwnCount") or "—"
    desc = b.get("Description") or "No description available from the provider."
    classes = b.get("DataClasses", []) or []
    ul = "".join([f"<li>{c}</li>" for c in classes])

    html = f"""
    <div class="pm-node {'left' if align_left else ''}">
      <div class="pm-bubble">{bubble}</div>
      <div class="pm-panel">
        <div class="pm-title">{name}</div>
        <div class="pm-meta">Domain: <b>{domain}</b> • Breached: <b>{date}</b> • Records: <b>{pwn}</b></div>
        <div style="line-height:1.55">{desc}</div>
        <div style="margin-top:10px; font-weight:700">Compromised data:</div>
        <ul class="pm-list">{ul if ul else '<li>Not specified</li>'}</ul>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# ---------- PAGES ----------
def page1():
    set_background("DTB1.jpg", 1)
    inject_global_ui()
    render_topbar()
    render_sidebar()
    render_hidden_nav_state()

    gif = Path(st.session_state.settings.get("animation_gif", "hero.gif"))
    if gif.is_file():
        st.image(str(gif), use_container_width=True)

    st.markdown(
        """
        <div style='margin-top:14px;'>
          <div style="margin-bottom:6px;">
            <span style="
                display:inline-block;
                font-family:'Playfair Display', serif;
                font-size:18px;
                letter-spacing:3px;
                text-transform:uppercase;
                padding:6px 14px;
                border-radius:999px;
                border:1px solid rgba(255,255,255,0.85);
                background:radial-gradient(circle at 0 0, rgba(255,255,255,0.18), rgba(0,0,0,0.85));
                box-shadow:0 0 18px rgba(255,255,255,0.55);
            ">
                PRIVACY&nbsp;MIRROR
            </span>
          </div>
          <h1 style='font-family:Playfair Display; font-size:40px; text-transform:uppercase; letter-spacing:4px; margin-top:10px;'>
            Check Your <span style="border-bottom:2px solid #fff;">Digital Exposure</span>
          </h1>
          <p style='margin-top:10px; font-size:15px; max-width:520px;'>
            One quick scan shows if your email or phone appears in known data breaches —
            so you can act before attackers do.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([0.4, 0.6])
    with c1:
        if st.button("Start scan →", use_container_width=True):
            st.session_state.step = 2
            st.rerun()
        st.caption("No sign up. No tracking. Just a clean privacy check.")
    with c2:
        st.markdown(
            """
            <div class="pm-feature-row">
              <div class="pm-feature-tile">
                <div class="pm-feature-title">Email Exposure</div>
                <div class="pm-feature-body">See which breaches have your email, what data leaked, and how old those incidents are.</div>
              </div>
              <div class="pm-feature-tile">
                <div class="pm-feature-title">Phone Exposure</div>
                <div class="pm-feature-body">Check if your phone number appears in public leak datasets connected to your identity.</div>
              </div>
              <div class="pm-feature-tile">
                <div class="pm-feature-title">Actionable Steps</div>
                <div class="pm-feature-body">Get a simple safety plan and generate strong passwords tailored for your key accounts.</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div style='margin-top:26px; font-family:Noto Sans TC; font-size:13px; opacity:.9;'>We care about your privacy.</div>",
        unsafe_allow_html=True,
    )

def page2():
    set_background("DTB2.jpg", 2)
    inject_global_ui()
    render_topbar()
    render_sidebar()
    render_hidden_nav_state()

    st.markdown("<h2 style='text-transform:uppercase; letter-spacing:3px;'>Scan your exposure</h2>", unsafe_allow_html=True)
    st.caption("We never store or log your email/phone. Checks happen only in this browser session.")

    st.markdown('<div class="pm-form-card">', unsafe_allow_html=True)
    consent = st.checkbox(
        "I consent to checking my data against public breach datasets.", key="consent_box"
    )
    privacy = st.checkbox(
        "Privacy mode (do not store results after session)",
        value=st.session_state.settings.get("privacy_mode", True),
    )
    st.session_state.settings["privacy_mode"] = bool(privacy)

    c_email, c_phone = st.columns(2)

    with c_email:
        email = st.text_input("✉️  Email", key="email_inp")

    with c_phone:
        # Single "Phone number" block with dropdown + number in same area
        st.markdown("📱 Phone number")
        cc_options = [
            ("+1", "United States / Canada"),
            ("+44", "United Kingdom"),
            ("+61", "Australia"),
            ("+91", "India"),
            ("+971", "United Arab Emirates"),
            ("+966", "Saudi Arabia"),
            ("+81", "Japan"),
            ("+49", "Germany"),
            ("+33", "France"),
            ("+39", "Italy"),
            ("+34", "Spain"),
            ("+92", "Pakistan"),
            ("+880", "Bangladesh"),
            ("+94", "Sri Lanka"),
        ]

        def _fmt_cc(opt):
            return f"{opt[0]}  {opt[1]}"

        cc_col, num_col = st.columns([0.9, 1.8])
        with cc_col:
            selected_cc = st.selectbox(
                "",
                cc_options,
                format_func=_fmt_cc,
                key="cc_select",
                label_visibility="collapsed",
            )
        with num_col:
            local_phone = st.text_input(
                "",
                key="phone_inp",
                placeholder="Enter phone without country code",
                label_visibility="collapsed",
            )

        full_phone = ""
        if local_phone.strip():
            digits_only = re.sub(r"\D", "", local_phone)
            full_phone = selected_cc[0] + digits_only

    st.markdown(
        "<div class='pm-note'>You can enter Email OR Phone — only one is required.</div>",
        unsafe_allow_html=True,
    )

    if not get_hibp_key():
        st.caption("Email checks require an email breach provider API key configured by the app owner.")

    email_valid = (
        bool(
            re.match(
                r"^(?=.{6,254}$)[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
                email.strip(),
            )
        )
        if email.strip()
        else False
    )
    phone_norm = normalize_phone_basic(full_phone) if full_phone else None

    if email.strip():
        if email_valid:
            st.success("🎉 Valid email format.")
        else:
            st.error("❌ Please enter a valid Email Address.")

    if full_phone:
        if phone_norm:
            st.success(f"📱 Valid phone: {phone_norm}")
        else:
            st.error("❌ Please enter a valid phone number (digits only, we'll format with your country code).")

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("← Back to home"):
            st.session_state.step = 1
            st.rerun()
    with c2:
        if st.button("Run scan →"):
            if not consent:
                st.error("Please give consent to continue.")
            elif not (email_valid or phone_norm):
                st.error("Enter a valid Email or Phone to continue.")
            else:
                st.session_state.inputs["email"] = email.strip() if email_valid else ""
                st.session_state.inputs["phone"] = phone_norm if phone_norm else ""
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown(
                    "<style>.pm-footer{display:none !important}</style>",
                    unsafe_allow_html=True,
                )
                run_checks(
                    st.session_state.inputs["email"],
                    st.session_state.inputs["phone"],
                )
    st.markdown("</div>", unsafe_allow_html=True)

def page3():
    res = st.session_state.results
    email_res = res.get("email")
    phone_res = res.get("phone")
    phone_hits = 0
    if st.session_state.inputs.get("phone") and isinstance(phone_res, dict):
        phone_hits = len(phone_res.get("entries") or phone_res.get("data") or [])
    breached = (isinstance(email_res, list) and len(email_res) > 0) or (phone_hits > 0)
    set_background("DTB5.jpg" if breached else "DTB3.jpg", 3)

    inject_global_ui()
    render_topbar()
    render_sidebar()
    render_hidden_nav_state()

    risk = res.get("meta", {}).get("risk", 0)
    st.markdown("<h2 style='text-transform:uppercase; letter-spacing:3px;'>Exposure summary</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        render_score_gauge(risk, label="Risk Score")
    with col2:
        stats = compute_stats(email_res or [])
        st.markdown(
            f"""
            <div class="pm-summary">
              <div>
                <div style="font-size:18px; font-weight:800; margin-bottom:4px;">Your breach snapshot</div>
                <div style="font-size:13px; opacity:.85;">Based on known public breach datasets for the details you entered.</div>
              </div>
              <div class="pm-summary-right">
                <div class="pm-kpi"><div class="kpi-label">Total Breaches</div><div class="kpi-value">{stats['total']}</div></div>
                <div class="pm-kpi"><div class="kpi-label">Est. Exposed Records</div><div class="kpi-value">{stats['records']:,}</div></div>
                <div class="pm-kpi"><div class="kpi-label">High / Med / Low</div><div class="kpi-value" style="font-size:18px">{stats['high']} / {stats['med']} / {stats['low']}</div></div>
                <div class="pm-kpi"><div class="kpi-label">Unique Data Types</div><div class="kpi-value">{stats['unique_types']}</div></div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if isinstance(email_res, list) and email_res:
        c_left, c_right = st.columns([1, 1])
        with c_left:
            st.markdown("#### Data types leaked")
            type_stats = compute_stats(email_res)["top_types"]
            if type_stats:
                df = pd.DataFrame(type_stats, columns=["Data Type", "Count"])
                fig = px.bar(
                    df,
                    x="Data Type",
                    y="Count",
                    text="Count",
                    color="Count",
                    color_continuous_scale=["#ffd8a8", "#ffb566", "#ff9f40", "#ff7a00"],
                    template="plotly_dark",
                )
                fig.update_traces(
                    textposition="outside",
                    texttemplate="<b>%{text}</b>",
                    textfont=dict(color="white", size=14),
                    marker_line_color="rgba(255,255,255,.35)",
                    marker_line_width=1.2,
                )
                fig.update_layout(
                    margin=dict(l=10, r=10, t=10, b=10),
                    xaxis_title=None,
                    yaxis_title=None,
                    height=320,
                    bargap=0.25,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white", size=14),
                )
                st.plotly_chart(fig, use_container_width=True)
        with c_right:
            years = []
            for b in email_res:
                ds = b.get("BreachDate") or ""
                if len(ds) >= 4 and ds[:4].isdigit():
                    years.append(int(ds[:4]))
            if years:
                from collections import Counter as _Counter

                yc = _Counter(years)
                df_years = pd.DataFrame(
                    {"Year": sorted(yc.keys()), "Breaches": [yc[y] for y in sorted(yc.keys())]}
                )
                st.markdown("#### Breaches over time")
                fig2 = px.line(
                    df_years,
                    x="Year",
                    y="Breaches",
                    markers=True,
                    template="plotly_dark",
                )
                fig2.update_traces(line_width=3)
                fig2.update_layout(
                    margin=dict(l=10, r=10, t=10, b=10),
                    xaxis_title=None,
                    yaxis_title=None,
                    height=320,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white", size=14),
                )
                st.plotly_chart(fig2, use_container_width=True)

    if email_res is None and st.session_state.inputs.get("email"):
        st.info("ℹ️ Email checks unavailable (missing key, rate-limited, or network issue).")
    elif isinstance(email_res, list) and len(email_res) == 0 and st.session_state.inputs.get("email"):
        st.success("🎉 No known breaches found for this email. Congratulations!")
    elif isinstance(email_res, list):
        st.markdown("#### Email breaches in detail", unsafe_allow_html=True)

        def _key(b):
            return b.get("BreachDate") or b.get("AddedDate") or ""

        breaches_sorted = sorted(email_res, key=_key, reverse=True)
        st.markdown('<div class="pm-timeline">', unsafe_allow_html=True)
        left = False
        for b in breaches_sorted:
            render_breach_detail(b, align_left=left)
            left = not left
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.inputs.get("phone"):
        st.markdown("#### Phone lookup")
        phone_res = res.get("phone")
        if phone_res is None:
            err = st.session_state.get("phone_error") or ""
            if err:
                st.info(f"ℹ️ Phone lookup unavailable: {err}")
            else:
                st.info("ℹ️ Phone lookup unavailable (credentials missing or network error).")
        else:
            hits = phone_res.get("entries") or phone_res.get("data") or []
            if hits:
                st.error(f"⚠️ Phone found in {len(hits)} record(s) (sample shown).")
                st.json(hits[:5])
            else:
                st.success("✅ Phone: No known hits from available datasets.")

    if isinstance(email_res, list) and email_res:
        st.markdown("#### Export")
        st.download_button(
            "Download breaches (CSV)",
            data=breaches_csv_bytes(email_res),
            file_name="breaches.csv",
            mime="text/csv",
        )
        pdf_bytes = build_pdf_report(
            st.session_state.inputs.get("email", ""),
            compute_stats(email_res),
            email_res,
            risk,
        )
        if pdf_bytes:
            st.download_button(
                "Download full report (PDF)",
                data=pdf_bytes,
                file_name="privacy_mirror_report.pdf",
                mime="application/pdf",
            )

    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("← Back to scan"):
            st.session_state.step = 2
            st.rerun()
    with c2:
        if st.button("Next → Safety guide"):
            st.session_state.step = 4
            st.rerun()
    with c3:
        if st.button("Re-scan with same details"):
            email = st.session_state.inputs.get("email", "")
            phone = st.session_state.inputs.get("phone", "")
            run_checks(email, phone)

def page4():
    set_background("DTB4.jpg", 4)
    inject_global_ui()
    render_topbar()
    render_sidebar()
    render_hidden_nav_state()

    st.markdown("<h2 style='text-transform:uppercase; letter-spacing:3px;'>Security playbook</h2>", unsafe_allow_html=True)
    st.caption("Turn your results into simple actions you can take today.")

    st.markdown(
        """
        <div class="pm-safety-row">
          <div class="pm-safety-card">
            <h4>Passwords</h4>
            <p>Update any accounts that share the same password. Start with email, banking, and social media.</p>
          </div>
          <div class="pm-safety-card">
            <h4>2FA / MFA</h4>
            <p>Enable two-factor authentication on critical services. Use an authenticator app instead of SMS when possible.</p>
          </div>
          <div class="pm-safety-card">
            <h4>Recovery info</h4>
            <p>Remove old recovery emails and phone numbers you no longer control. Make sure recovery goes only to you.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Strong password generator")
    length = st.slider("Length", 12, 64, 16)
    if st.button("Generate strong password"):
        st.session_state.generated_password = "".join(
            secrets.choice(
                string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}"
            )
            for _ in range(length)
        )
    if st.session_state.get("generated_password"):
        pwd = st.session_state["generated_password"]
        st.text_input(
            "New password (copy & save securely)", value=pwd, type="password"
        )
        st.caption("Tip: click in the field and press Ctrl+C / ⌘+C to copy.")

    st.markdown("### Extra tips")
    with st.expander("Spot phishing attempts"):
        st.markdown(
            "Check sender addresses carefully, avoid clicking unknown links, and never share one-time codes in chat."
        )
    with st.expander("Email hygiene"):
        st.markdown(
            "Unsubscribe from old services you don’t use. Fewer accounts = fewer places your data can leak from."
        )

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("← Back to results"):
            st.session_state.step = 3
            st.rerun()
    with c2:
        if st.button("Restart scan ↺"):
            st.session_state.step = 1
            st.rerun()

# ---------- ROUTER ----------
def main():
    inject_global_ui()
    render_topbar()

    step = st.session_state.get("step", 1)
    if step == 1:
        page1()
    elif step == 2:
        page2()
    elif step == 3:
        page3()
    elif step == 4:
        page4()
    else:
        st.session_state.step = 1
        page1()

if __name__ == "__main__":
    main()

# PROJECT BY AFTAB,MASOOD,SOHAIL