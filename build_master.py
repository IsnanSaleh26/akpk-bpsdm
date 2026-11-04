# -*- coding: utf-8 -*-
"""Membuat data/master_akpk.xlsx dari master_data.py. Jalankan: python build_master.py"""
import re
import pandas as pd
from master_data import J

# Kata kunci -> nama penyelenggara baku (untuk rekap kebutuhan per penyelenggara)
PENYELENGGARA = [
    (r"\blan\b", "LAN RI"), (r"\bbkn\b|pusdiklat bkn|bkd", "BKN"),
    (r"bpsdm prov|bpsdm sultra", "BPSDM Prov. Sultra"), (r"bpsdm kemendagri|kemendagri", "Kemendagri / BPSDM Kemendagri"),
    (r"bnsp|\blsp\b|lsp ", "BNSP / LSP"), (r"lkpp", "LKPP"), (r"bappenas|bappeda|ap2i", "Bappenas / Bappeda"),
    (r"\bbps\b", "BPS"), (r"komdigi|diskominfo|bssn|blk", "Komdigi / Diskominfo / BSSN"),
    (r"kemenpan|menpan", "KemenPANRB"), (r"bpkp", "BPKP"), (r"kemenkeu|djpb|bppk|djkn|djp\b|bpkad", "Kemenkeu / BPKAD"),
    (r"anri", "ANRI"), (r"brin|perguruan tinggi", "BRIN / Perguruan Tinggi"),
]

def kunci(s: str) -> str:
    t = s.lower()
    out = [label for pat, label in PENYELENGGARA if re.search(pat, t)]
    return "|".join(out) if out else "Lainnya"

def norm_status(s: str) -> str:
    return s.split(" (")[0]

jab_rows, item_rows = [], []
for no, (kat, nama, info, plt, ser) in enumerate(J, 1):
    jid = f"J{no:02d}"
    jab_rows.append(dict(kode_jabatan=jid, no=no, kategori=kat, jabatan=nama, info_jabatan=info))
    for tipe, lst, pre in (("Pelatihan", plt, "P"), ("Sertifikasi / Uji Kompetensi / Asesmen", ser, "S")):
        for i, (n, jenis, dasar, status, peny) in enumerate(lst, 1):
            item_rows.append(dict(
                kode_item=f"{jid}-{pre}{i:02d}", kode_jabatan=jid, tipe=tipe, pelatihan_sertifikasi=n,
                jenis=jenis, dasar=dasar, status=norm_status(status), keterangan_status=status,
                penyelenggara=peny, penyelenggara_kunci=kunci(peny)))

jab, items = pd.DataFrame(jab_rows), pd.DataFrame(item_rows)
with pd.ExcelWriter("data/master_akpk.xlsx", engine="openpyxl") as xw:
    jab.to_excel(xw, sheet_name="Jabatan", index=False)
    items.to_excel(xw, sheet_name="Master", index=False)
    for ws in xw.book.worksheets:
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width = min(60, max(12, max(len(str(c.value or "")) for c in col[:40]) + 2))
        ws.freeze_panes = "A2"
print(len(jab), "jabatan,", len(items), "item")
print(items.status.value_counts().to_dict())
print(items.penyelenggara_kunci.str.split("|").explode().value_counts().to_dict())
