# -*- coding: utf-8 -*-
"""Penyimpanan jawaban: Google Sheets bila secrets tersedia, selain itu berkas CSV lokal."""
import logging
import time
from pathlib import Path
import pandas as pd
import streamlit as st

log = logging.getLogger("akpk")

COLUMNS = ["submission_id", "timestamp", "nip", "nama", "pangkat_golongan", "status_kepegawaian",
           "kode_jabatan", "jabatan", "kategori", "unit_kerja", "kode_item", "tipe",
           "pelatihan_sertifikasi", "jenis", "status", "penyelenggara", "penyelenggara_kunci", "pemenuhan"]
LOCAL_CSV = Path(__file__).parent / "data" / "responses.csv"
PERCOBAAN = 3          # jumlah usaha menulis ke Google Sheets bila jaringan bermasalah
JEDA_DASAR = 1.5       # detik; menunggu 1.5 dtk, lalu 3 dtk


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
    try:
        gc.set_timeout((10, 30))      # (sambung, baca) agar tidak menggantung di sinyal lemah
    except Exception:
        pass
    sh = gc.open_by_key(s["gsheet"]["spreadsheet_id"])
    name = s["gsheet"].get("worksheet", "Jawaban")
    try:
        ws = sh.worksheet(name)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(name, rows=2000, cols=len(COLUMNS))
    if ws.row_values(1) != COLUMNS:
        ws.update(range_name="A1", values=[COLUMNS])
    return ws


def _lepas_koneksi():
    """Buang koneksi tersimpan agar percobaan berikutnya membuat koneksi baru."""
    try:
        _worksheet.clear()
    except Exception:
        pass


def already_saved(sid: str) -> bool:
    """True bila nomor pengisian ini sudah tercatat (mencegah data ganda saat kirim ulang)."""
    try:
        if mode() == "gsheets":
            return _worksheet().find(sid, in_column=1) is not None
        if LOCAL_CSV.exists():
            return sid in set(pd.read_csv(LOCAL_CSV, dtype=str, usecols=["submission_id"])["submission_id"])
    except Exception:
        log.warning("already_saved gagal diperiksa", exc_info=True)
    return False


def append_rows(rows: list[dict]) -> None:
    df = pd.DataFrame(rows, columns=COLUMNS).astype(str)
    if mode() == "gsheets":
        sid = rows[0]["submission_id"]
        terakhir = None
        for usaha in range(PERCOBAAN):
            try:
                # jika usaha sebelumnya sebenarnya sudah masuk (balasan hilang di jalan), jangan tulis lagi
                if usaha and already_saved(sid):
                    break
                _worksheet().append_rows(df.values.tolist(), value_input_option="RAW")
                break
            except Exception as e:
                terakhir = e
                log.warning("usaha simpan %d/%d gagal: %s", usaha + 1, PERCOBAAN, type(e).__name__)
                _lepas_koneksi()
                if usaha < PERCOBAAN - 1:
                    time.sleep(JEDA_DASAR * (usaha + 1))
        else:
            raise terakhir
        read_all.clear()
    else:
        LOCAL_CSV.parent.mkdir(exist_ok=True)
        df.to_csv(LOCAL_CSV, mode="a", header=not LOCAL_CSV.exists(), index=False)


@st.cache_data(ttl=30, show_spinner=False)
def read_all() -> pd.DataFrame:
    if mode() == "gsheets":
        try:
            vals = _worksheet().get_all_values()
        except Exception:
            _lepas_koneksi()
            vals = _worksheet().get_all_values()      # satu kali coba ulang dengan koneksi baru
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
