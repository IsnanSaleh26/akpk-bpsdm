# -*- coding: utf-8 -*-
"""Penyimpanan jawaban: Google Sheets bila secrets tersedia, selain itu berkas CSV lokal."""
from pathlib import Path
import pandas as pd
import streamlit as st

COLUMNS = ["submission_id", "timestamp", "nip", "nama", "pangkat_golongan", "status_kepegawaian",
           "kode_jabatan", "jabatan", "kategori", "unit_kerja", "kode_item", "tipe",
           "pelatihan_sertifikasi", "jenis", "status", "penyelenggara", "penyelenggara_kunci", "pemenuhan"]
LOCAL_CSV = Path(__file__).parent / "data" / "responses.csv"


def _secrets():
    try:
        return st.secrets
    except Exception:
        return {}


def mode() -> str:
    s = _secrets()
    try:
        return "gsheets" if ("gcp_service_account" in s and "gsheet" in s) else "lokal"
    except Exception:
        return "lokal"


@st.cache_resource(show_spinner=False)
def _worksheet():
    import gspread
    s = st.secrets
    gc = gspread.service_account_from_dict(dict(s["gcp_service_account"]))
    sh = gc.open_by_key(s["gsheet"]["spreadsheet_id"])
    name = s["gsheet"].get("worksheet", "Jawaban")
    try:
        ws = sh.worksheet(name)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(name, rows=2000, cols=len(COLUMNS))
    if ws.row_values(1) != COLUMNS:
        ws.update(range_name="A1", values=[COLUMNS])
    return ws


def append_rows(rows: list[dict]) -> None:
    df = pd.DataFrame(rows, columns=COLUMNS).astype(str)
    if mode() == "gsheets":
        _worksheet().append_rows(df.values.tolist(), value_input_option="RAW")
        st.cache_data.clear()
    else:
        LOCAL_CSV.parent.mkdir(exist_ok=True)
        df.to_csv(LOCAL_CSV, mode="a", header=not LOCAL_CSV.exists(), index=False)


@st.cache_data(ttl=30, show_spinner=False)
def read_all() -> pd.DataFrame:
    if mode() == "gsheets":
        vals = _worksheet().get_all_values()
        df = pd.DataFrame(vals[1:], columns=vals[0]) if len(vals) > 1 else pd.DataFrame(columns=COLUMNS)
    elif LOCAL_CSV.exists():
        df = pd.read_csv(LOCAL_CSV, dtype=str).fillna("")
    else:
        df = pd.DataFrame(columns=COLUMNS)
    return df


def latest_per_nip(df: pd.DataFrame) -> pd.DataFrame:
    """Jika pegawai mengisi lebih dari sekali, pakai pengisian terbaru."""
    if df.empty:
        return df
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    last = df.sort_values("timestamp").groupby("nip")["submission_id"].last()
    return df[df["submission_id"].isin(last.values)]


def nip_exists(nip: str):
    try:
        df = read_all()
        hit = df[df["nip"] == nip]
        return None if hit.empty else hit["timestamp"].max()
    except Exception:
        return None
