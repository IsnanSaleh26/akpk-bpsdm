# -*- coding: utf-8 -*-
"""Aplikasi 1 - Kuesioner AKPK untuk pegawai.  Jalankan: streamlit run app_kuesioner.py"""
import logging
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Kuesioner AKPK - BPSDM Sultra", page_icon="📋", layout="centered")

import storage
from common import (KATEGORI, UNIT_KERJA, GOL_PNS, GOL_PPPK, STATUS_ORDER, inject_css, hero, badge, esc, load_master)

log = logging.getLogger("akpk")
WITA = ZoneInfo("Asia/Makassar")      # server Streamlit Cloud memakai UTC; catat waktu setempat


def now() -> datetime:
    return datetime.now(WITA)


inject_css()
jab_df, items_df = load_master()
S = st.session_state
S.setdefault("step", 1)
STATUS_PEG = ["PNS", "CPNS", "PPPK", "PPPK Paruh Waktu"]


# ------------------------------------------------------------------ pemulihan saat sinyal putus
# Jawaban yang sedang diisi disalin ke alamat halaman (kode jabatan + deretan S/B, tanpa nama atau NIP).
# Jika koneksi terputus atau halaman termuat ulang, jawaban dipulihkan dari alamat itu.
def encode_ans(kodes) -> str:
    return "".join({"Sudah": "S", "Belum": "B"}.get(S.get(f"ans_{k}"), "-") for k in kodes)


def decode_ans(code: str, kodes) -> dict:
    peta = {"S": "Sudah", "B": "Belum"}
    return {k: peta[c] for k, c in zip(kodes, code) if c in peta}


def _try_restore():
    if "restored" in S:
        return
    S["restored"] = True
    qp = st.query_params
    j, a = qp.get("j"), qp.get("a")
    if j and a and j in set(jab_df.kode_jabatan):
        kodes = items_df[items_df.kode_jabatan == j].kode_item.tolist()
        jawaban = decode_ans(a, kodes)
        if jawaban:
            S["jawaban"] = jawaban
            S["restore_j"] = j


_try_restore()


def stepper(cur: int):
    names = ["Identitas", "Pemenuhan kompetensi", "Selesai"]
    html = "".join(f'<div class="st {"on" if i == cur else "done" if i < cur else ""}"><b>{"✓" if i < cur else i}</b><span>{n}</span></div>'
                   for i, n in enumerate(names, 1))
    st.markdown(f'<div class="stepper">{html}</div>', unsafe_allow_html=True)


def pbar(done: int, total: int) -> str:
    pct = int(done / total * 100) if total else 0
    cls = "pbar full" if total and done == total else "pbar"
    return (f'<div class="{cls}"><div class="pt"><span><b>{done} dari {total}</b> pertanyaan terjawab</span><span class="pct">{pct}%</span></div>'
            f'<div class="track"><i style="width:{pct}%"></i></div></div>')


# ------------------------------------------------------------------ langkah 1
def step_identitas():
    P = S.get("profil", {})
    if not P and S.get("restore_j"):
        r0 = jab_df[jab_df.kode_jabatan == S["restore_j"]]
        if len(r0):
            P = dict(kategori=r0.iloc[0].kategori, jabatan=r0.iloc[0].jabatan)
            st.markdown('<div class="note">Jawaban Anda sebelumnya berhasil dipulihkan. Isi ulang identitas di bawah, lalu lanjut; jawaban akan muncul kembali.</div>',
                        unsafe_allow_html=True)
    st.markdown('<div class="sec">Identitas pegawai</div>', unsafe_allow_html=True)
    with st.container(border=True):
        c1, c2 = st.columns(2)
        nama = c1.text_input("Nama lengkap", value=P.get("nama", ""), placeholder="Nama sesuai SK")
        nip = c2.text_input("NIP / NIPPPK", value=P.get("nip", ""), max_chars=18, placeholder="18 digit angka",
                            help="Dipakai sebagai kunci agar satu pegawai hanya tercatat satu kali.")
        status_peg = st.radio("Status kepegawaian", STATUS_PEG, horizontal=True,
                              index=STATUS_PEG.index(P["status_kepegawaian"]) if P.get("status_kepegawaian") in STATUS_PEG else 0)
        gols = GOL_PPPK if status_peg.startswith("PPPK") else GOL_PNS
        c3, c4 = st.columns(2)
        gol = c3.selectbox("Pangkat / golongan", gols, index=gols.index(P["pangkat_golongan"]) if P.get("pangkat_golongan") in gols else None,
                           placeholder="Pilih golongan")
        unit = c4.selectbox("Unit kerja / bidang", UNIT_KERJA, index=UNIT_KERJA.index(P["unit_kerja"]) if P.get("unit_kerja") in UNIT_KERJA else None,
                            placeholder="Pilih unit kerja")

    st.markdown('<div class="sec">Jabatan saat ini<small>Daftar pelatihan akan menyesuaikan jabatan yang Anda pilih</small></div>', unsafe_allow_html=True)
    with st.container(border=True):
        kat = st.radio("Kelompok jabatan", KATEGORI, horizontal=True,
                       index=KATEGORI.index(P["kategori"]) if P.get("kategori") in KATEGORI else 0)
        opsi = jab_df[jab_df.kategori == kat]
        names = opsi["jabatan"].tolist()
        jab = st.selectbox("Jabatan", names, index=names.index(P["jabatan"]) if P.get("jabatan") in names else None, placeholder="Pilih jabatan")
        if jab:
            row = opsi[opsi.jabatan == jab].iloc[0]
            it = items_df[items_df.kode_jabatan == row.kode_jabatan]
            np_, ns = (it.tipe == "Pelatihan").sum(), (it.tipe != "Pelatihan").sum()
            wj = (it.status == "Wajib").sum()
            st.markdown(f'<div class="jab-card"><div class="n">{esc(jab)}</div><div class="i">{esc(row.info_jabatan)}</div>'
                        f'<span class="chip">{np_} pelatihan</span><span class="chip">{ns} sertifikasi / asesmen</span><span class="chip w">{wj} wajib</span></div>',
                        unsafe_allow_html=True)

    if st.button("Lanjut ke pemenuhan kompetensi", type="primary", width="stretch"):
        err = []
        if not nama.strip(): err.append("Nama lengkap belum diisi.")
        if not (nip.isdigit() and len(nip) == 18): err.append("NIP/NIPPPK harus 18 digit angka.")
        if not gol: err.append("Pangkat/golongan belum dipilih.")
        if not unit: err.append("Unit kerja belum dipilih.")
        if not jab: err.append("Jabatan belum dipilih.")
        if err:
            for e in err: st.error(e)
            return
        S["profil"] = dict(nama=nama.strip(), nip=nip, status_kepegawaian=status_peg, pangkat_golongan=gol, unit_kerja=unit,
                           kategori=kat, jabatan=jab, kode_jabatan=row.kode_jabatan, info_jabatan=row.info_jabatan)
        with st.spinner("Memeriksa data..."):
            prev = storage.nip_exists(nip)
        S["sudah_pernah"] = str(prev) if prev is not None else None
        S["step"] = 2
        st.rerun()


# ------------------------------------------------------------------ langkah 2
def _save_answers():
    S["jawaban"] = {k[4:]: S[k] for k in list(S.keys()) if k.startswith("ans_") and S[k]}


def _back():
    _save_answers()
    S.pop("pending", None)
    S["step"] = 1


def _mark_all(val, kodes):
    for k in kodes:
        S[f"ans_{k}"] = val


def step_pemenuhan():
    P = S["profil"]
    it = items_df[items_df.kode_jabatan == P["kode_jabatan"]].copy()
    it["_o"] = it["status"].map({s: i for i, s in enumerate(STATUS_ORDER)})
    saved = S.get("jawaban", {})
    for k in it.kode_item:
        S.setdefault(f"ans_{k}", saved.get(k))

    st.markdown(f'<div class="jab-card"><div class="n">{esc(P["nama"])}</div><div class="i">{esc(P["jabatan"])}</div></div>', unsafe_allow_html=True)
    if S.get("sudah_pernah"):
        st.info(f"NIP ini sudah pernah mengisi pada {S['sudah_pernah'][:16]}. Jawaban baru akan menggantikan jawaban sebelumnya dalam analisis.")

    st.markdown('<div class="sec">Pelatihan dan sertifikasi yang direkomendasikan<small>Pilih Sudah bila pernah mengikuti dan lulus, selain itu pilih Belum</small></div>', unsafe_allow_html=True)
    prog = st.container(key="progbar")
    q1, q2, _ = st.columns([1.2, 1.2, 1.6])
    kodes = it.kode_item.tolist()
    q1.button("Tandai semua Belum", on_click=_mark_all, args=("Belum", kodes), width="stretch")
    q2.button("Tandai semua Sudah", on_click=_mark_all, args=("Sudah", kodes), width="stretch")

    for label, tipe_filter in (("A. Pelatihan", it.tipe == "Pelatihan"), ("B. Sertifikasi, uji kompetensi, dan asesmen", it.tipe != "Pelatihan")):
        sub = it[tipe_filter]
        if sub.empty: continue
        st.markdown(f'<div class="sec">{label}<small>{len(sub)} pertanyaan</small></div>', unsafe_allow_html=True)
        for _, r in sub.iterrows():
            with st.container(border=True, key=f"item_{str(r.status).replace(' ', '')}_{r.kode_item}"):
                c1, c2 = st.columns([3.2, 1.3], vertical_alignment="center")
                c1.markdown(f'<div class="item-t">{esc(r.pelatihan_sertifikasi)}</div>{badge(r.status)}<span class="badge b-jenis">{esc(r.jenis)}</span>'
                            f'<details class="more"><summary>Rincian</summary><div class="item-m">Penyelenggara: {esc(r.penyelenggara)}<br>Dasar: {esc(r.dasar)}</div></details>',
                            unsafe_allow_html=True)
                c2.segmented_control("Pemenuhan", ["Sudah", "Belum"], key=f"ans_{r.kode_item}", label_visibility="collapsed", width="stretch")

    done = sum(1 for k in kodes if S.get(f"ans_{k}"))
    prog.markdown(pbar(done, len(kodes)), unsafe_allow_html=True)

    # salin jawaban ke alamat halaman supaya bisa dipulihkan bila sinyal putus
    kode_now = encode_ans(kodes)
    if st.query_params.get("a") != kode_now or st.query_params.get("j") != P["kode_jabatan"]:
        st.query_params["j"] = P["kode_jabatan"]
        st.query_params["a"] = kode_now

    st.markdown("&nbsp;")
    ok = st.checkbox("Saya menyatakan bahwa data yang saya isi benar dan dapat dipertanggungjawabkan.")
    b1, b2 = st.columns([1, 2])
    b1.button("Kembali", on_click=_back, width="stretch")
    if b2.button("Kirim jawaban", type="primary", width="stretch"):
        if done < len(kodes):
            miss = [r.pelatihan_sertifikasi for _, r in it.iterrows() if not S.get(f"ans_{r.kode_item}")]
            contoh = "; ".join(miss[:3]) + (" ..." if len(miss) > 3 else "")
            st.error(f"Masih ada {len(miss)} pertanyaan yang belum dijawab, antara lain: {contoh}")
            return
        if not ok:
            st.error("Centang pernyataan di atas sebelum mengirim.")
            return
        # nomor pengisian dibuat sekali dan dipakai ulang bila kirim diulang, supaya tidak tercatat dobel
        if "pending" not in S:
            S["pending"] = dict(sid=f"AKPK-{now():%y%m%d}-{uuid.uuid4().hex[:6].upper()}", ts=now().strftime("%Y-%m-%d %H:%M:%S"), tried=False)
        pend = S["pending"]
        rows = [dict(submission_id=pend["sid"], timestamp=pend["ts"], nip=P["nip"], nama=P["nama"], pangkat_golongan=P["pangkat_golongan"],
                     status_kepegawaian=P["status_kepegawaian"], kode_jabatan=P["kode_jabatan"], jabatan=P["jabatan"], kategori=P["kategori"],
                     unit_kerja=P["unit_kerja"], kode_item=r.kode_item, tipe=r.tipe, pelatihan_sertifikasi=r.pelatihan_sertifikasi, jenis=r.jenis,
                     status=r.status, penyelenggara=r.penyelenggara, penyelenggara_kunci=r.penyelenggara_kunci, pemenuhan=S[f"ans_{r.kode_item}"])
                for _, r in it.iterrows()]
        try:
            with st.spinner("Menyimpan jawaban. Jangan tutup halaman ini..."):
                if pend["tried"] and storage.already_saved(pend["sid"]):
                    pass                                  # kiriman sebelumnya ternyata sudah masuk
                else:
                    pend["tried"] = True
                    storage.append_rows(rows)
        except Exception as e:
            log.exception("Gagal menyimpan jawaban %s", pend["sid"])
            st.error("Jawaban belum tersimpan, kemungkinan karena sinyal terputus. Jawaban Anda di layar tidak hilang. "
                     "Pastikan sinyal stabil, lalu tekan Kirim jawaban sekali lagi.")
            st.caption(f"Kode kesalahan: {type(e).__name__}")
            return
        S["hasil"] = dict(sid=pend["sid"], rows=pd.DataFrame(rows))
        S.pop("pending", None)
        st.query_params.clear()
        S["step"] = 3
        st.rerun()


# ------------------------------------------------------------------ langkah 3
def _reset():
    for k in list(S.keys()):
        del S[k]
    st.query_params.clear()


def step_selesai():
    P, df = S["profil"], S["hasil"]["rows"]
    sudah = (df.pemenuhan == "Sudah").sum()
    wj = df[df.status == "Wajib"]
    st.markdown(f'<div class="done-card"><div class="ck">✓</div><h2>Terima kasih, {esc(P["nama"])}</h2>'
                f'<div style="color:#5B6B84">Jawaban Anda sudah tersimpan dengan nomor <b>{esc(S["hasil"]["sid"])}</b>.</div></div>', unsafe_allow_html=True)
    st.markdown("&nbsp;")
    wj_ok = int((wj.pemenuhan == "Sudah").sum())
    c1, c2 = st.columns(2)
    c1.markdown(f'<div class="kpi a"><div class="v">{sudah}<small> / {len(df)}</small></div><div class="l">Pelatihan dan sertifikasi terpenuhi</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="kpi b"><div class="v">{wj_ok}<small> / {len(wj)}</small></div><div class="l">Kewajiban (Wajib) terpenuhi</div></div>', unsafe_allow_html=True)
    gap = df[df.pemenuhan == "Belum"].copy()
    gap["o"] = gap.status.map({s: i for i, s in enumerate(STATUS_ORDER)})
    gap = gap.sort_values(["o", "tipe"])
    if len(gap):
        st.markdown('<div class="sec">Kebutuhan pengembangan Anda<small>Diurutkan dari yang paling wajib</small></div>', unsafe_allow_html=True)
        for _, r in gap.iterrows():
            st.markdown(f'<div class="jab-card s-{esc(r.status)}"><div class="n" style="font-size:.95rem">{esc(r.pelatihan_sertifikasi)}</div>'
                        f'<div style="margin-top:6px">{badge(r.status)}<span class="badge b-jenis">{esc(r.jenis)}</span></div></div>', unsafe_allow_html=True)
    else:
        st.success("Semua rekomendasi untuk jabatan Anda sudah terpenuhi.")
    st.write("")
    st.download_button("Unduh bukti pengisian (CSV)", df.drop(columns=["penyelenggara_kunci"]).to_csv(index=False).encode("utf-8-sig"),
                       file_name=f"{S['hasil']['sid']}.csv", mime="text/csv")
    st.button("Isi untuk pegawai lain", on_click=_reset)


# ------------------------------------------------------------------ halaman
hero("Analisis Kebutuhan Pengembangan Kompetensi",
     "Isi data Anda dan tandai pelatihan serta sertifikasi yang sudah dimiliki. Hasilnya dipakai untuk menyusun rencana pengembangan kompetensi pegawai. Pengisian sekitar 5 menit.",
     compact=S["step"] > 1)
stepper(S["step"])
{1: step_identitas, 2: step_pemenuhan, 3: step_selesai}[S["step"]]()
if storage.mode() == "lokal":
    st.caption("Mode uji coba: jawaban disimpan di berkas lokal (data/responses.csv), belum terhubung ke Google Sheets.")
st.markdown('<div class="foot">BPSDM Provinsi Sulawesi Tenggara</div>', unsafe_allow_html=True)
