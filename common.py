# -*- coding: utf-8 -*-
"""Tema, CSS, dan pemuat data master yang dipakai kedua aplikasi."""
import html
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).parent
NAVY, INK, BLUE, ORANGE, MUTED, LINE, BG = "#14305A", "#0F1C33", "#1F6FB2", "#E4730C", "#5B6B84", "#DCE3ED", "#F3F6FA"
GREEN, AMBER, GREY = "#1E7B4F", "#E4A23B", "#A7B3C6"
STATUS_ORDER = ["Wajib", "Dianjurkan", "Bersyarat", "Pelengkap"]
STATUS_COLOR = {"Wajib": "#1B4A85", "Dianjurkan": "#4F86C6", "Bersyarat": "#97B9E0", "Pelengkap": "#C9D8EC"}
KATEGORI = ["Struktural / Manajerial", "Jabatan Fungsional", "Jabatan Pelaksana"]

UNIT_KERJA = ["Pimpinan (Kepala Badan)", "Sekretariat",
              "Bidang Sertifikasi Kompetensi dan Pengelolaan Kelembagaan",
              "Bidang Pengembangan Kompetensi Teknis Inti",
              "Bidang Pengembangan Kompetensi Teknis Umum dan Fungsional",
              "Bidang Pengembangan Kompetensi Manajerial",
              "Kelompok Jabatan Fungsional"]

GOL_PNS = ["I/a - Juru Muda", "I/b - Juru Muda Tingkat I", "I/c - Juru", "I/d - Juru Tingkat I",
           "II/a - Pengatur Muda", "II/b - Pengatur Muda Tingkat I", "II/c - Pengatur", "II/d - Pengatur Tingkat I",
           "III/a - Penata Muda", "III/b - Penata Muda Tingkat I", "III/c - Penata", "III/d - Penata Tingkat I",
           "IV/a - Pembina", "IV/b - Pembina Tingkat I", "IV/c - Pembina Utama Muda", "IV/d - Pembina Utama Madya", "IV/e - Pembina Utama"]
GOL_PPPK = [f"Golongan {r}" for r in ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII"]]


@st.cache_data(show_spinner=False)
def load_master():
    jab = pd.read_excel(ROOT / "data" / "master_akpk.xlsx", "Jabatan", dtype=str)
    items = pd.read_excel(ROOT / "data" / "master_akpk.xlsx", "Master", dtype=str).fillna("")
    jab["no"] = jab["no"].astype(int)
    return jab, items


def esc(x) -> str:
    return html.escape(str(x))


FONT = "@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');"

BASE_CSS = FONT + f"""
/* ================= dasar ================= */
html, :root, .stApp {{ color-scheme: light only; }}
html, body, [class*="css"], .stApp, button, input, textarea, select {{ font-family: 'Plus Jakarta Sans', system-ui, -apple-system, 'Segoe UI', sans-serif !important; }}
.stApp {{ background: {BG}; color: {INK}; }}
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {{ display: none !important; }}
header[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ padding-top: 1rem; padding-bottom: 4rem; }}
h1, h2, h3 {{ color: {INK}; letter-spacing: -0.01em; }}
.stApp label, .stApp [data-testid="stWidgetLabel"] p, .stApp [data-testid="stCheckbox"] p, .stApp [data-testid="stRadio"] p {{ color: {INK}; }}
.stApp [data-testid="stWidgetLabel"] p {{ font-weight: 600; font-size: .88rem; }}
.stApp [data-testid="stCaptionContainer"] {{ color: {MUTED}; }}

/* ================= hero ================= */
.hero {{ position: relative; overflow: hidden; border-radius: 20px; padding: 28px 32px; color: #fff;
  background: linear-gradient(120deg, #0F2547 0%, {NAVY} 55%, #1F5F9C 100%); margin-bottom: 16px; }}
.hero h1 {{ color: #fff; font-size: 1.7rem; line-height: 1.25; font-weight: 800; margin: 0 0 6px 0; padding: 0; max-width: 34ch; }}
.hero p {{ margin: 0; color: #C9D8EE; font-size: .95rem; max-width: 50ch; line-height: 1.55; }}
.hero .org {{ color: #F2C37A; font-weight: 700; font-size: .88rem; margin-bottom: 10px; }}
.hero svg {{ position: absolute; right: -40px; top: -50px; width: 300px; height: 300px; opacity: .9; pointer-events: none; }}
.hero.compact {{ padding: 16px 22px; border-radius: 16px; margin-bottom: 12px; }}
.hero.compact .org {{ margin-bottom: 3px; font-size: .78rem; }}
.hero.compact h1 {{ font-size: 1.12rem; margin: 0; }}
.hero.compact p {{ display: none; }}
.hero.compact svg {{ width: 150px; height: 150px; right: -30px; top: -45px; }}
@media (max-width: 640px) {{
  .hero {{ padding: 22px 20px; }} .hero h1 {{ font-size: 1.35rem; }}
  .hero svg {{ width: 200px; height: 200px; right: -60px; top: -60px; }}
  .hero.compact {{ padding: 14px 18px; }} .hero.compact h1 {{ font-size: 1.02rem; }}
}}

/* ================= stepper ================= */
.stepper {{ display: flex; gap: 8px; margin: 4px 0 16px 0; }}
.stepper .st {{ flex: 1; display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: 12px; background: #fff; border: 1px solid {LINE}; color: {MUTED}; font-size: .85rem; font-weight: 600; }}
.stepper .st b {{ display: inline-flex; width: 26px; height: 26px; border-radius: 50%; align-items: center; justify-content: center; background: #E8EEF6; color: {MUTED}; font-size: .8rem; flex: none; }}
.stepper .st.on {{ border-color: {NAVY}; color: {NAVY}; box-shadow: 0 0 0 3px rgba(31,78,140,.10); }}
.stepper .st.on b {{ background: {NAVY}; color: #fff; }}
.stepper .st.done b {{ background: {GREEN}; color: #fff; }}
.stepper .st.done {{ color: {INK}; }}
@media (max-width: 640px) {{ .stepper .st span {{ display: none; }} .stepper .st.on span {{ display: inline; }} .stepper .st {{ padding: 8px 10px; }} }}

/* ================= judul bagian ================= */
.sec {{ font-size: 1.05rem; font-weight: 800; color: {INK}; margin: 24px 0 10px 0; }}
.sec small {{ display: block; font-weight: 500; color: {MUTED}; font-size: .84rem; margin: 2px 0 0 0; line-height: 1.45; }}

/* ================= kartu & isian ================= */
.stApp div[data-testid="stVerticalBlockBorderWrapper"] {{ border-radius: 14px; background: #fff; border-color: {LINE}; }}
.stApp .stTextInput input, .stApp [data-baseweb="select"] > div {{ border-radius: 10px; background: #fff; color: {INK}; border: 1px solid #B9C7DB; min-height: 44px; }}
.stApp .stTextInput input::placeholder {{ color: #7C8AA0; }}
.stApp .stTextInput input:focus {{ border-color: {BLUE}; box-shadow: 0 0 0 3px rgba(31,111,178,.18); }}

/* ================= tombol: warna eksplisit agar terbaca di semua perangkat ================= */
.stApp .stButton > button, .stApp .stDownloadButton > button, .stApp button[data-testid="stBaseButton-secondary"] {{
  border-radius: 10px; font-weight: 700; padding: .55rem 1.1rem; min-height: 46px;
  background: #fff; color: {NAVY}; border: 1.5px solid #8FA6C4; box-shadow: 0 1px 2px rgba(15,28,51,.08); }}
.stApp .stButton > button:hover, .stApp .stDownloadButton > button:hover, .stApp button[data-testid="stBaseButton-secondary"]:hover {{
  background: #EEF3FA; color: {NAVY}; border-color: {NAVY}; }}
.stApp .stButton > button p, .stApp .stDownloadButton > button p {{ color: inherit; }}
.stApp .stButton > button[kind="primary"], .stApp button[data-testid="stBaseButton-primary"] {{
  background: {NAVY}; color: #fff; border: 1.5px solid {NAVY}; box-shadow: 0 2px 6px rgba(20,48,90,.25); }}
.stApp .stButton > button[kind="primary"]:hover, .stApp button[data-testid="stBaseButton-primary"]:hover {{
  background: #1F4E8C; border-color: #1F4E8C; color: #fff; }}
.stApp .stButton > button:focus-visible, .stApp .stDownloadButton > button:focus-visible {{ outline: 3px solid rgba(31,111,178,.45); outline-offset: 2px; }}

/* pilihan Sudah / Belum */
.stApp [data-testid="stButtonGroup"] button {{ background: #fff; color: {INK}; border: 1.5px solid #8FA6C4; min-height: 46px; font-weight: 700; }}
.stApp [data-testid="stButtonGroup"] button p {{ color: inherit; }}
.stApp [data-testid="stButtonGroup"] button:hover {{ background: #EEF3FA; border-color: {NAVY}; }}
.stApp [data-testid="stButtonGroup"] button[data-testid="stBaseButton-segmented_controlActive"],
.stApp [data-testid="stButtonGroup"] button[aria-checked="true"], .stApp [data-testid="stButtonGroup"] button[aria-pressed="true"] {{
  background: {NAVY}; color: #fff; border-color: {NAVY}; }}

/* ================= butir pelatihan: strip warna menurut status ================= */
.stApp [class*="st-key-item_Wajib_"] {{ border-left: 5px solid {NAVY} !important; border-radius: 14px; }}
.stApp [class*="st-key-item_Dianjurkan_"] {{ border-left: 5px solid {BLUE} !important; border-radius: 14px; }}
.stApp [class*="st-key-item_Bersyarat_"] {{ border-left: 5px solid {AMBER} !important; border-radius: 14px; }}
.stApp [class*="st-key-item_Pelengkap_"] {{ border-left: 5px solid {GREY} !important; border-radius: 14px; }}
.item-t {{ font-weight: 600; font-size: .96rem; line-height: 1.45; color: {INK}; margin-bottom: 8px; }}
.item-m {{ font-size: .8rem; color: {MUTED}; margin-top: 8px; line-height: 1.5; }}
.badge {{ display: inline-block; padding: 2px 10px; border-radius: 999px; font-size: .74rem; font-weight: 700; margin-right: 6px; }}
.b-Wajib {{ background: {NAVY}; color: #fff; }}
.b-Dianjurkan {{ background: #DCE9F8; color: #1B4A85; }}
.b-Bersyarat {{ background: #FFF0D6; color: #8A5200; }}
.b-Pelengkap {{ background: #ECEFF4; color: #4B5870; }}
.b-jenis {{ border: 1px solid {LINE}; color: {MUTED}; background: #fff; }}

/* ================= bilah kemajuan (menempel di atas saat menggulir) ================= */
.stApp [class*="st-key-progbar"] {{ position: sticky; top: 0; z-index: 60; background: {BG}; padding: 8px 0 6px 0; }}
.stApp div:has(> [class*="st-key-progbar"]) {{ position: sticky; top: 0; z-index: 60; }}
.pbar {{ background: #fff; border: 1px solid {LINE}; border-radius: 12px; padding: 10px 14px; box-shadow: 0 4px 12px rgba(15,28,51,.06); }}
.pbar .pt {{ display: flex; justify-content: space-between; align-items: baseline; font-size: .84rem; color: {MUTED}; font-weight: 600; margin-bottom: 7px; }}
.pbar .pt b {{ color: {INK}; font-weight: 800; }}
.pbar .pt span {{ color: {NAVY}; font-weight: 800; }}
.pbar .track {{ height: 8px; border-radius: 99px; background: {LINE}; overflow: hidden; }}
.pbar .track i {{ display: block; height: 100%; background: {BLUE}; border-radius: 99px; transition: width .25s ease; }}
.pbar.full .track i {{ background: {GREEN}; }}
.pbar.full .pt span {{ color: {GREEN}; }}

/* ================= kartu jabatan, chip, hasil ================= */
.jab-card {{ background: #fff; border: 1px solid {LINE}; border-left: 5px solid {NAVY}; border-radius: 12px; padding: 14px 18px; margin: 8px 0 4px 0; }}
.jab-card .n {{ font-weight: 800; font-size: 1.02rem; color: {INK}; }}
.jab-card .i {{ color: {MUTED}; font-size: .85rem; margin-top: 2px; }}
.jab-card.s-Wajib {{ border-left-color: {NAVY}; }} .jab-card.s-Dianjurkan {{ border-left-color: {BLUE}; }}
.jab-card.s-Bersyarat {{ border-left-color: {AMBER}; }} .jab-card.s-Pelengkap {{ border-left-color: {GREY}; }}
.chip {{ display: inline-block; padding: 3px 10px; border-radius: 8px; background: #EEF3FA; color: {NAVY}; font-size: .78rem; font-weight: 700; margin: 10px 6px 0 0; }}
.chip.w {{ background: {NAVY}; color: #fff; }}

.kpi {{ background: #fff; border: 1px solid {LINE}; border-radius: 14px; padding: 16px 18px; height: 100%; }}
.kpi .v {{ font-size: 2rem; font-weight: 800; color: {INK}; line-height: 1.1; letter-spacing: -0.02em; }}
.kpi .v small {{ font-size: 1rem; color: {MUTED}; font-weight: 600; letter-spacing: 0; }}
.kpi .l {{ font-size: .84rem; color: {MUTED}; margin-top: 6px; font-weight: 600; }}
.kpi .s {{ font-size: .78rem; color: {MUTED}; margin-top: 2px; }}
.kpi.a {{ border-top: 4px solid {BLUE}; }} .kpi.b {{ border-top: 4px solid {NAVY}; }} .kpi.c {{ border-top: 4px solid {ORANGE}; }} .kpi.d {{ border-top: 4px solid #8A94A6; }}

.panel-t {{ font-weight: 800; font-size: 1rem; color: {INK}; margin: 0 0 2px 0; }}
.panel-s {{ color: {MUTED}; font-size: .84rem; margin: 0 0 6px 0; }}
.done-card {{ background: #fff; border: 1px solid {LINE}; border-radius: 18px; padding: 28px; text-align: center; }}
.done-card .ck {{ width: 54px; height: 54px; border-radius: 50%; background: {GREEN}; color: #fff; display: inline-flex; align-items: center; justify-content: center; font-size: 1.6rem; font-weight: 800; }}
.done-card h2 {{ margin: 12px 0 4px 0; font-size: 1.4rem; }}
.demo-pill {{ display: inline-block; background: #FFF0D6; color: #8A5200; border-radius: 999px; padding: 3px 12px; font-size: .78rem; font-weight: 700; }}
.foot {{ text-align: center; color: {MUTED}; font-size: .78rem; margin-top: 36px; }}

/* ================= layar kecil ================= */
@media (max-width: 640px) {{
  .block-container {{ padding-left: 1rem; padding-right: 1rem; }}
  .stApp .stButton > button, .stApp .stDownloadButton > button {{ min-height: 50px; width: 100%; }}
  .stApp [data-testid="stButtonGroup"] button {{ min-height: 50px; }}
  .item-t {{ font-size: .93rem; }}
  .kpi .v {{ font-size: 1.7rem; }}
}}
"""

RING = """<svg viewBox="0 0 300 300" aria-hidden="true" fill="none" stroke="#fff">
<circle cx="150" cy="150" r="120" stroke-opacity=".10" stroke-width="22"/>
<circle cx="150" cy="150" r="120" stroke-opacity=".22" stroke-width="2" stroke-dasharray="38 14"/>
<circle cx="150" cy="150" r="88" stroke-opacity=".16" stroke-width="2"/>
<circle cx="150" cy="150" r="60" stroke="#F2C37A" stroke-opacity=".55" stroke-width="2" stroke-dasharray="3 9" stroke-linecap="round"/></svg>"""


def inject_css(extra: str = ""):
    st.markdown(f"<style>{BASE_CSS}{extra}</style>", unsafe_allow_html=True)


def hero(title: str, text: str, org: str = "BPSDM Provinsi Sulawesi Tenggara", compact: bool = False):
    cls = "hero compact" if compact else "hero"
    st.markdown(f'<div class="{cls}">{RING}<div class="org">{esc(org)}</div><h1>{esc(title)}</h1><p>{esc(text)}</p></div>', unsafe_allow_html=True)


def badge(status: str) -> str:
    return f'<span class="badge b-{esc(status)}">{esc(status)}</span>'
