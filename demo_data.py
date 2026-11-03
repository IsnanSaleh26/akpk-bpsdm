# -*- coding: utf-8 -*-
"""Data contoh (fiktif) agar dashboard bisa dicoba sebelum ada jawaban asli."""
import numpy as np, pandas as pd
from datetime import datetime, timedelta
from storage import COLUMNS

DEPAN = ["Andi", "Siti", "La Ode", "Wa Ode", "Muh.", "Nur", "Rahmat", "Fitri", "Hasan", "Dewi", "Arif", "Sri", "Yusuf", "Ratna", "Irwan", "Lestari", "Basri", "Hartini", "Jufri", "Mega"]
BELAKANG = ["Saputra", "Rahayu", "Hidayat", "Wulandari", "Kurniawan", "Nasir", "Pratama", "Ningsih", "Mansur", "Astuti", "Rusdi", "Sari", "Tamrin", "Fauzi", "Lamodi", "Hamid"]
BIDANG = ["Bidang Sertifikasi Kompetensi dan Pengelolaan Kelembagaan", "Bidang Pengembangan Kompetensi Teknis Inti",
          "Bidang Pengembangan Kompetensi Teknis Umum dan Fungsional", "Bidang Pengembangan Kompetensi Manajerial"]
GOL = {"Struktural / Manajerial": ["IV/c", "IV/a", "III/d", "III/c"], "Jabatan Fungsional": ["IV/c", "IV/a", "III/d", "III/c", "III/b", "III/a"],
       "Jabatan Pelaksana": ["III/c", "III/a", "II/d", "II/b", "I/d"]}
P_SUDAH = {"Wajib": 0.74, "Dianjurkan": 0.36, "Bersyarat": 0.30, "Pelengkap": 0.18}
BONUS = {"Kepemimpinan": 0.1, "Dasar": 0.15, "Fungsional": 0.05, "Asesmen": -0.12, "Sertifikasi Profesi": -0.12, "Sertifikasi": -0.1}


def unit_for(row, rng):
    n, k = row["jabatan"], row["kategori"]
    if n.startswith("Kepala Badan"): return "Pimpinan (Kepala Badan)"
    if n.startswith("Sekretaris") or "Sub Bagian" in n: return "Sekretariat"
    if n.startswith("Kepala Bidang") or "Sub Bidang" in n: return BIDANG[min(3, int(row["no"]) - 3) % 4] if n.startswith("Kepala Bidang") else rng.choice(BIDANG)
    if k == "Jabatan Fungsional": return "Kelompok Jabatan Fungsional"
    return rng.choice(["Sekretariat"] + BIDANG)


def make_demo(jab: pd.DataFrame, items: pd.DataFrame, n: int = 96, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    w = np.where(jab["kategori"].str.startswith("Struktural"), 1.0, np.where(jab["kategori"].str.startswith("Jabatan F"), 2.2, 1.8))
    w = w / w.sum()
    picks = list(jab.index) + list(rng.choice(jab.index, size=n - len(jab), p=w))   # tiap jabatan terwakili minimal 1
    rows, now = [], datetime(2026, 10, 30, 8, 0)
    for i, ji in enumerate(picks):
        j = jab.loc[ji]
        nama = f"{rng.choice(DEPAN)} {rng.choice(BELAKANG)}"
        nip = "19" + "".join(rng.choice(list("0123456789"), 16))
        ts = (now - timedelta(days=float(rng.beta(1.6, 2.4) * 21), hours=float(rng.uniform(0, 9)))).strftime("%Y-%m-%d %H:%M:%S")
        sid = f"AKPK-DEMO-{i + 1:04d}"
        unit = unit_for(j, rng)
        gol = rng.choice(GOL[j["kategori"]])
        stat = rng.choice(["PNS", "PNS", "PNS", "PPPK", "CPNS"], p=[.4, .25, .15, .15, .05])
        theta = rng.normal(0, 0.17)
        for _, it in items[items.kode_jabatan == j["kode_jabatan"]].iterrows():
            p = np.clip(P_SUDAH[it["status"]] + BONUS.get(it["jenis"], 0) + theta, 0.03, 0.97)
            rows.append(dict(submission_id=sid, timestamp=ts, nip=nip, nama=nama, pangkat_golongan=gol, status_kepegawaian=stat,
                             kode_jabatan=j["kode_jabatan"], jabatan=j["jabatan"], kategori=j["kategori"], unit_kerja=unit,
                             kode_item=it["kode_item"], tipe=it["tipe"], pelatihan_sertifikasi=it["pelatihan_sertifikasi"], jenis=it["jenis"],
                             status=it["status"], penyelenggara=it["penyelenggara"], penyelenggara_kunci=it["penyelenggara_kunci"],
                             pemenuhan="Sudah" if rng.random() < p else "Belum"))
    return pd.DataFrame(rows, columns=COLUMNS)
