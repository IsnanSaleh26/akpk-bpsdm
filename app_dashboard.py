# -*- coding: utf-8 -*-
"""Aplikasi 2 - Dashboard insight AKPK untuk pimpinan dan analis SDM.  Jalankan: streamlit run app_dashboard.py"""
import textwrap
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Dashboard AKPK - BPSDM Sultra", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

import storage
from demo_data import make_demo
from common import (BLUE, ORANGE, NAVY, INK, MUTED, LINE, STATUS_ORDER, STATUS_COLOR, inject_css, hero, esc, load_master)

inject_css("[data-testid='stSidebar'] { background:#fff; border-right:1px solid #DCE3ED; } .stTabs [data-baseweb='tab'] { font-weight:700; }")
S = st.session_state
jab_df, items_df = load_master()


# ------------------------------------------------------------ akses
def gate():
    try:
        pw = st.secrets.get("dashboard_password")
    except Exception:
        pw = None
    if pw is None:
        if storage.mode() == "gsheets":
            st.error("Kata sandi dashboard belum diatur. Tambahkan dashboard_password di Secrets.")
            st.stop()
        return
    if S.get("auth"):
        return
    hero("Dashboard AKPK", "Halaman ini berisi data pegawai dan hanya untuk pimpinan serta analis SDM. Masukkan kata sandi untuk melanjutkan.")
    _, c, _ = st.columns([1, 1.2, 1])
    with c:
        with st.container(border=True):
            p = st.text_input("Kata sandi", type="password")
            if st.button("Masuk", type="primary", width="stretch"):
                if p == pw:
                    S["auth"] = True
                    st.rerun()
                st.error("Kata sandi tidak cocok.")
    st.stop()


gate()


# ------------------------------------------------------------ data
@st.cache_data(show_spinner=False)
def demo_df():
    return make_demo(jab_df, items_df)


try:
    raw = storage.read_all()
except Exception as e:
    st.error(f"Data belum bisa dibaca dari penyimpanan: {e}")
    st.stop()

with st.sidebar:
    st.markdown(f"<div style='font-weight:800;font-size:1.1rem;color:{NAVY}'>Dashboard AKPK</div><div style='color:{MUTED};font-size:.82rem;margin-bottom:10px'>BPSDM Provinsi Sulawesi Tenggara</div>", unsafe_allow_html=True)
    use_demo = st.toggle("Pakai data contoh (fiktif)", value=raw.empty, help="Untuk mencoba tampilan sebelum ada jawaban pegawai.")
    c1, c2 = st.columns(2)
    if c1.button("Muat ulang", width="stretch"):
        st.cache_data.clear(); st.rerun()
    if S.get("auth") and c2.button("Keluar", width="stretch"):
        S.clear(); st.rerun()

df = demo_df() if use_demo else storage.latest_per_nip(raw)
if df.empty:
    hero("Dashboard AKPK", "Belum ada jawaban masuk. Setelah pegawai mengisi kuesioner, grafik akan muncul di sini. Nyalakan data contoh di panel kiri untuk melihat tampilannya.")
    st.stop()
df = df.copy()
df["sudah"] = (df["pemenuhan"] == "Sudah").astype(int)
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

with st.sidebar:
    st.markdown("**Saring data**")
    def pick(label, col, order=None):
        opts = order or sorted(df[col].dropna().unique())
        return st.multiselect(label, [o for o in opts if o in set(df[col])], placeholder="Semua")
    f_kat = pick("Kelompok jabatan", "kategori")
    f_jab = pick("Jabatan", "jabatan", jab_df.sort_values("no")["jabatan"].tolist())
    f_unit = pick("Unit kerja", "unit_kerja")
    f_sp = pick("Status kepegawaian", "status_kepegawaian")
    f_tipe = pick("Jenis kegiatan", "tipe")
    f_stat = pick("Status rekomendasi", "status", STATUS_ORDER)
    f_jenis = pick("Jenis kompetensi", "jenis")
    for col, f in (("kategori", f_kat), ("jabatan", f_jab), ("unit_kerja", f_unit), ("status_kepegawaian", f_sp), ("tipe", f_tipe), ("status", f_stat), ("jenis", f_jenis)):
        if f: df = df[df[col].isin(f)]
    st.caption(f"{df['nip'].nunique()} pegawai dan {len(df)} jawaban sesuai saringan")

if df.empty:
    st.warning("Tidak ada data yang cocok dengan saringan. Kurangi pilihan saringan di panel kiri.")
    st.stop()


# ------------------------------------------------------------ helpers
def style(fig, h=340):
    fig.update_layout(height=h, margin=dict(l=4, r=4, t=6, b=4), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Plus Jakarta Sans, system-ui, sans-serif", size=12, color=INK),
                      hoverlabel=dict(bgcolor="white", bordercolor=LINE, font=dict(family="Plus Jakarta Sans, sans-serif", size=12, color=INK)),
                      legend=dict(orientation="h", y=1.08, x=0, font=dict(size=12)))
    fig.update_xaxes(gridcolor="#E6EBF2", zeroline=False, linecolor=LINE)
    fig.update_yaxes(gridcolor="#E6EBF2", zeroline=False, linecolor=LINE)
    return fig


def panel(title, sub=None):
    box = st.container(border=True)
    box.markdown(f'<div class="panel-t">{esc(title)}</div>' + (f'<div class="panel-s">{esc(sub)}</div>' if sub else ""), unsafe_allow_html=True)
    return box


def show(fig, box):
    box.plotly_chart(fig, width="stretch", config={"displaylogo": False, "modeBarButtonsToRemove": ["lasso2d", "select2d"]})


def pct(a, b):
    return 100 * a / b if b else 0.0


def short(s, n=64):
    return textwrap.shorten(s, n, placeholder="…")


def mask(n):
    return n[:4] + "•" * 10 + n[-4:] if len(n) >= 8 else n


def stacked_pct(g, cats, key, order=None, row=52, h=None):
    """Batang 100%: Sudah vs Belum per kategori."""
    t = g.groupby(key).agg(sudah=("sudah", "sum"), n=("sudah", "size")).reindex(order if order else sorted(g[key].unique())).dropna()
    t["p"] = 100 * t.sudah / t.n
    fig = go.Figure()
    fig.add_bar(y=t.index, x=t.p, orientation="h", name="Sudah", marker=dict(color=BLUE, cornerradius=4), text=[f"{v:.0f}%" if v >= 16 else "" for v in t.p], textposition="inside",
                insidetextfont=dict(color="white", size=12), customdata=np.c_[t.sudah, t.n], hovertemplate="<b>%{y}</b><br>Sudah: %{x:.1f}% (%{customdata[0]:.0f} dari %{customdata[1]:.0f})<extra></extra>")
    fig.add_bar(y=t.index, x=100 - t.p, orientation="h", name="Belum", marker=dict(color=ORANGE, cornerradius=4), text=[f"{100 - v:.0f}%" if 100 - v >= 16 else "" for v in t.p], textposition="inside",
                insidetextfont=dict(color="white", size=12), customdata=np.c_[t.n - t.sudah, t.n], hovertemplate="<b>%{y}</b><br>Belum: %{x:.1f}% (%{customdata[0]:.0f} dari %{customdata[1]:.0f})<extra></extra>")
    fig.update_layout(barmode="stack", bargap=.35, legend_traceorder="normal")
    fig.update_xaxes(range=[0, 100], ticksuffix="%", showgrid=False)
    fig.update_yaxes(autorange="reversed", showgrid=False)
    fig = style(fig, h or 60 + row * len(t))
    fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.0, x=0, font=dict(size=12)), margin=dict(l=4, r=4, t=34, b=4))
    return fig


# ------------------------------------------------------------ ringkasan angka
n_resp = df["nip"].nunique()
tot, sud = len(df), int(df.sudah.sum())
wj = df[df.status == "Wajib"]
p_all, p_wj = pct(sud, tot), pct(wj.sudah.sum(), len(wj))
gap_total = tot - sud
jab_terisi = df["kode_jabatan"].nunique()

hero("Dashboard Kebutuhan Pengembangan Kompetensi", "Gambaran pemenuhan pelatihan dan sertifikasi pegawai terhadap rekomendasi tiap jabatan, serta prioritas pelatihan yang perlu direncanakan.")
if use_demo:
    st.markdown('<span class="demo-pill">Menampilkan data contoh (fiktif), bukan jawaban pegawai</span>', unsafe_allow_html=True)
    st.write("")

k = st.columns(4)
for col, cls, v, l, s in ((k[0], "b", f"{n_resp}", "Pegawai mengisi", f"dari {jab_terisi} jabatan"),
                          (k[1], "a", f"{p_all:.0f}%", "Pemenuhan keseluruhan", f"{sud} dari {tot} rekomendasi"),
                          (k[2], "a", f"{p_wj:.0f}%", "Pemenuhan yang wajib", f"{int(wj.sudah.sum())} dari {len(wj)} kewajiban"),
                          (k[3], "c", f"{gap_total}", "Kebutuhan belum terpenuhi", "jumlah pelatihan atau sertifikasi yang belum dimiliki")):
    col.markdown(f'<div class="kpi {cls}"><div class="v">{v}</div><div class="l">{l}</div><div class="s">{s}</div></div>', unsafe_allow_html=True)
st.write("")

# Temuan utama (otomatis dari data)
gap_items = (df[df.pemenuhan == "Belum"].groupby(["kode_item", "pelatihan_sertifikasi", "status"]).size().reset_index(name="n").sort_values("n", ascending=False))
by_jenis = df.groupby("jenis").agg(s=("sudah", "sum"), n=("sudah", "size")).query("n >= 10")
by_jab = wj.groupby("jabatan").agg(s=("sudah", "sum"), n=("sudah", "size"), r=("nip", "nunique")).query("n >= 3 and r >= 2")
notes = []
if len(gap_items):
    r = gap_items.iloc[0]
    notes.append(f"Yang paling banyak belum dimiliki: **{r.pelatihan_sertifikasi}** ({r.status.lower()}), {r.n} pegawai.")
if len(by_jenis):
    by_jenis["p"] = 100 * by_jenis.s / by_jenis.n
    lo = by_jenis.p.idxmin()
    notes.append(f"Jenis kompetensi dengan pemenuhan terendah: **{lo}** ({by_jenis.p.min():.0f}%).")
if len(by_jab):
    by_jab["p"] = 100 * by_jab.s / by_jab.n
    notes.append(f"Jabatan dengan kewajiban paling tertinggal: **{by_jab.p.idxmin()}** ({by_jab.p.min():.0f}% terpenuhi).")
with st.container(border=True):
    st.markdown('<div class="panel-t">Temuan utama</div>', unsafe_allow_html=True)
    st.markdown("\n".join(f"- {n}" for n in notes) if notes else "Data belum cukup untuk menarik temuan.")

t1, t2, t3, t4, t5 = st.tabs(["Ringkasan", "Prioritas pelatihan", "Per jabatan dan unit", "Penyelenggara", "Data pegawai"])

# ------------------------------------------------------------ TAB 1
with t1:
    a, b, c = st.columns([1, 1.25, 1.25])
    with a:
        box = panel("Pemenuhan keseluruhan", "Semua pelatihan dan sertifikasi")
        fig = go.Figure(go.Pie(labels=["Sudah", "Belum"], values=[sud, gap_total], hole=.68, sort=False, direction="clockwise",
                               marker=dict(colors=[BLUE, ORANGE], line=dict(color="white", width=3)), textinfo="none",
                               hovertemplate="%{label}: %{value} (%{percent})<extra></extra>"))
        fig.add_annotation(text=f"<b>{p_all:.0f}%</b>", showarrow=False, font=dict(size=34, color=INK), y=0.54)
        fig.add_annotation(text="sudah dimiliki", showarrow=False, font=dict(size=12, color=MUTED), y=0.42)
        fig.update_layout(legend=dict(orientation="h", y=-0.02, x=0.2))
        show(style(fig, 270), box)
    with b:
        box = panel("Menurut status rekomendasi", "Wajib sampai pelengkap")
        show(stacked_pct(df, None, "status", STATUS_ORDER, h=270), box)
    with c:
        box = panel("Menurut kelompok jabatan", "Struktural, fungsional, pelaksana")
        show(stacked_pct(df, None, "kategori", h=270), box)

    d1, d2 = st.columns([1.5, 1])
    n_j = df["jenis"].nunique()
    with d1:
        box = panel("Menurut jenis kompetensi", "Kepemimpinan, teknis, sertifikasi, dan lainnya")
        show(stacked_pct(df, None, "jenis", row=34), box)
    with d2:
        box = panel("Progres pengisian", "Jumlah pegawai yang sudah mengisi, kumulatif")
        sub = df.drop_duplicates("nip").dropna(subset=["timestamp"])
        daily = sub.groupby(sub.timestamp.dt.date).size().cumsum()
        fig = go.Figure(go.Scatter(x=list(daily.index), y=daily.values, mode="lines", line=dict(color=BLUE, width=2.5, shape="spline"),
                                   fill="tozeroy", fillcolor="rgba(31,111,178,.12)", hovertemplate="%{x|%d %b %Y}<br>%{y} pegawai<extra></extra>"))
        fig.update_yaxes(rangemode="tozero")
        show(style(fig, 60 + 34 * n_j), box)

# ------------------------------------------------------------ TAB 2
with t2:
    with st.container(border=True):
        f1, f2, f3 = st.columns([1.2, 1.6, 1.2])
        tipe_sel = f1.radio("Tampilkan", ["Semua", "Pelatihan", "Sertifikasi"], horizontal=True)
        stat_sel = f2.multiselect("Status rekomendasi", STATUS_ORDER, default=["Wajib", "Dianjurkan"])
        topn = f3.slider("Jumlah teratas", 5, 30, 12)
    g = df.copy()
    if tipe_sel == "Pelatihan": g = g[g.tipe == "Pelatihan"]
    if tipe_sel == "Sertifikasi": g = g[g.tipe != "Pelatihan"]
    if stat_sel: g = g[g.status.isin(stat_sel)]
    pri = (g.groupby(["kode_item", "pelatihan_sertifikasi", "status", "jenis", "penyelenggara"])
             .agg(responden=("nip", "nunique"), belum=("sudah", lambda x: int((1 - x).sum()))).reset_index())
    pri["persen_belum"] = 100 * pri.belum / pri.responden
    pri = pri[pri.belum > 0].sort_values(["belum", "persen_belum"], ascending=False)
    if pri.empty:
        st.info("Tidak ada kebutuhan yang tersisa untuk saringan ini.")
    else:
        top = pri.head(topn)
        box = panel(f"{len(top)} pelatihan dan sertifikasi dengan kebutuhan terbesar", "Panjang batang adalah jumlah pegawai yang belum memilikinya. Arahkan kursor untuk melihat rincian.")
        fig = go.Figure()
        for s_ in STATUS_ORDER:
            t = top[top.status == s_]
            if t.empty: continue
            fig.add_bar(y=[short(x, 70) for x in t.pelatihan_sertifikasi], x=t.belum, orientation="h", name=s_,
                        marker=dict(color=STATUS_COLOR[s_], cornerradius=4), text=t.belum, textposition="outside", cliponaxis=False,
                        customdata=np.c_[t.pelatihan_sertifikasi, t.persen_belum, t.responden, t.penyelenggara, t.jenis],
                        hovertemplate="<b>%{customdata[0]}</b><br>Belum dimiliki: %{x} dari %{customdata[2]} pegawai (%{customdata[1]:.0f}%)"
                                      "<br>Jenis: %{customdata[4]}<br>Penyelenggara: %{customdata[3]}<extra></extra>")
        fig.update_layout(barmode="stack", bargap=.3, legend_traceorder="normal", yaxis=dict(autorange="reversed", categoryorder="array", categoryarray=[short(x, 70) for x in top.pelatihan_sertifikasi], automargin=True))
        fig.update_xaxes(title="Jumlah pegawai yang belum memilikinya")
        fig.update_yaxes(showgrid=False)
        show(style(fig, 90 + 34 * len(top)), box)
        st.dataframe(pri.rename(columns={"pelatihan_sertifikasi": "Pelatihan / sertifikasi", "status": "Status", "jenis": "Jenis", "penyelenggara": "Penyelenggara",
                                          "responden": "Pegawai terkait", "belum": "Belum memiliki", "persen_belum": "% belum"}).drop(columns=["kode_item"]),
                     hide_index=True, width="stretch", height=320,
                     column_config={"% belum": st.column_config.ProgressColumn("% belum", format="%.0f%%", min_value=0, max_value=100)})

# ------------------------------------------------------------ TAB 3
with t3:
    dim_lab = {"Jabatan": "jabatan", "Unit kerja": "unit_kerja", "Kelompok jabatan": "kategori", "Status kepegawaian": "status_kepegawaian", "Golongan": "pangkat_golongan"}
    c1, c2 = st.columns([1, 2])
    dim = c1.selectbox("Bandingkan menurut", list(dim_lab))
    which = c2.radio("Ukuran", ["Hanya yang wajib", "Semua rekomendasi"], horizontal=True)
    base = wj if which.startswith("Hanya") else df
    col = dim_lab[dim]
    t = base.groupby(col).agg(s=("sudah", "sum"), n=("sudah", "size"), resp=("nip", "nunique")).reset_index()
    t["p"] = 100 * t.s / t.n
    t = t.sort_values("p")
    box = panel(f"Pemenuhan {which.lower()} menurut {dim.lower()}", "Diurutkan dari yang paling tertinggal. Jumlah pegawai ada di dalam kurung.")
    fig = go.Figure(go.Bar(y=[f"{short(x, 58)} ({r})" for x, r in zip(t[col], t.resp)], x=t.p, orientation="h", marker=dict(color=BLUE, cornerradius=4),
                           text=[f"{v:.0f}%" for v in t.p], textposition="outside", cliponaxis=False,
                           customdata=np.c_[t[col], t.s, t.n, t.resp], hovertemplate="<b>%{customdata[0]}</b><br>%{x:.1f}% terpenuhi (%{customdata[1]:.0f} dari %{customdata[2]:.0f})<br>%{customdata[3]:.0f} pegawai<extra></extra>"))
    fig.update_xaxes(range=[0, 108], ticksuffix="%")
    fig.update_yaxes(showgrid=False, automargin=True, autorange="reversed")
    show(style(fig, 70 + 28 * len(t)), box)

    hm = df.pivot_table(index="jabatan", columns="status", values="sudah", aggfunc="mean") * 100
    cnt = df.groupby("jabatan")["nip"].nunique()
    order = [j for j in jab_df.sort_values("no")["jabatan"] if j in hm.index]
    hm = hm.reindex(order)[[s for s in STATUS_ORDER if s in hm.columns]]
    box = panel("Peta pemenuhan: jabatan menurut status rekomendasi", "Biru tua berarti pemenuhan tinggi, biru muda berarti tertinggal. Kotak kosong berarti jabatan itu tidak punya rekomendasi berstatus tersebut.")
    fig = go.Figure(go.Heatmap(z=hm.values, x=hm.columns, y=[f"{short(j, 56)} (n={cnt[j]})" for j in hm.index], zmin=0, zmax=100, xgap=3, ygap=3, hoverongaps=False,
                               colorscale=[[0, "#EAF1FA"], [.5, "#7FAEDB"], [1, "#14305A"]], text=np.where(np.isnan(hm.values), "", np.vectorize(lambda v: f"{v:.0f}%")(np.nan_to_num(hm.values))), texttemplate="%{text}", textfont=dict(size=12),
                               customdata=np.array(order, dtype=object)[:, None].repeat(len(hm.columns), 1),
                               hovertemplate="<b>%{customdata}</b><br>%{x}: %{z:.0f}% terpenuhi<extra></extra>", colorbar=dict(title="% sudah", ticksuffix="%", thickness=12, len=.6)))
    fig.update_yaxes(autorange="reversed", showgrid=False, automargin=True)
    fig.update_xaxes(side="top", showgrid=False)
    show(style(fig, 120 + 26 * len(hm)), box)

# ------------------------------------------------------------ TAB 4
with t4:
    gp = df[df.pemenuhan == "Belum"].assign(pk=lambda x: x.penyelenggara_kunci.str.split("|")).explode("pk")
    pen = gp.groupby("pk").agg(belum=("sudah", "size"), kegiatan=("kode_item", "nunique")).reset_index().sort_values("belum", ascending=False)
    box = panel("Kebutuhan menurut penyelenggara", "Dasar untuk menyusun kerja sama dan anggaran. Satu pelatihan yang bisa diikuti lewat beberapa instansi dihitung di setiap instansi tersebut.")
    fig = go.Figure(go.Bar(y=pen.pk, x=pen.belum, orientation="h", marker=dict(color=BLUE, cornerradius=4), text=pen.belum, textposition="outside", cliponaxis=False,
                           customdata=pen.kegiatan, hovertemplate="<b>%{y}</b><br>%{x} kebutuhan belum terpenuhi<br>%{customdata} jenis pelatihan/sertifikasi<extra></extra>"))
    fig.update_yaxes(autorange="reversed", showgrid=False, automargin=True)
    fig.update_xaxes(title="Jumlah kebutuhan (pegawai x kegiatan) yang belum terpenuhi")
    show(style(fig, 90 + 32 * len(pen)), box)
    pick_p = st.selectbox("Lihat rincian penyelenggara", pen.pk.tolist())
    det = (gp[gp.pk == pick_p].groupby(["pelatihan_sertifikasi", "status", "jenis"]).size().reset_index(name="Pegawai yang membutuhkan").sort_values("Pegawai yang membutuhkan", ascending=False))
    st.dataframe(det.rename(columns={"pelatihan_sertifikasi": "Pelatihan / sertifikasi", "status": "Status", "jenis": "Jenis"}), hide_index=True, width="stretch")

# ------------------------------------------------------------ TAB 5
with t5:
    resp = df.groupby(["nip", "nama", "jabatan", "unit_kerja"], as_index=False).agg(total=("sudah", "size"), sudah=("sudah", "sum"))
    w = wj.groupby("nip").agg(wajib_total=("sudah", "size"), wajib_sudah=("sudah", "sum")).reset_index()
    resp = resp.merge(w, on="nip", how="left").fillna({"wajib_total": 0, "wajib_sudah": 0})
    resp["pct_wajib"] = np.where(resp.wajib_total > 0, 100 * resp.wajib_sudah / resp.wajib_total.replace(0, np.nan), np.nan)
    resp["wajib_belum"] = (resp.wajib_total - resp.wajib_sudah).astype(int)
    resp["belum"] = resp.total - resp.sudah
    q = st.text_input("Cari nama atau jabatan", placeholder="Ketik sebagian nama atau jabatan")
    v = resp[resp.nama.str.contains(q, case=False) | resp.jabatan.str.contains(q, case=False)] if q else resp
    v = v.sort_values("pct_wajib", na_position="last")
    st.dataframe(v.assign(NIP=v.nip.map(mask))[["nama", "NIP", "jabatan", "unit_kerja", "pct_wajib", "wajib_belum", "belum", "total"]].rename(
        columns={"nama": "Nama", "jabatan": "Jabatan", "unit_kerja": "Unit kerja", "pct_wajib": "Wajib terpenuhi", "wajib_belum": "Wajib belum", "belum": "Semua belum", "total": "Total rekomendasi"}),
        hide_index=True, width="stretch", height=380,
        column_config={"Wajib terpenuhi": st.column_config.ProgressColumn("Wajib terpenuhi", format="%.0f%%", min_value=0, max_value=100)})

    st.markdown('<div class="sec">Siapa yang perlu mengikuti pelatihan tertentu</div>', unsafe_allow_html=True)
    opts = (df.drop_duplicates("kode_item")[["kode_item", "pelatihan_sertifikasi", "jabatan"]].assign(lab=lambda x: x.pelatihan_sertifikasi.map(lambda s: short(s, 90)) + "  |  " + x.jabatan.map(lambda s: short(s, 34))))
    sel = st.selectbox("Pilih pelatihan atau sertifikasi", opts.kode_item, format_func=lambda k: opts.set_index("kode_item").lab[k], index=None, placeholder="Pilih satu")
    if sel:
        who = df[(df.kode_item == sel) & (df.pemenuhan == "Belum")][["nama", "nip", "jabatan", "unit_kerja"]]
        st.write(f"{len(who)} pegawai belum memilikinya.")
        st.dataframe(who.assign(NIP=who.nip.map(mask))[["nama", "NIP", "jabatan", "unit_kerja"]].rename(columns={"nama": "Nama", "jabatan": "Jabatan", "unit_kerja": "Unit kerja"}), hide_index=True, width="stretch")

    d1, d2, _ = st.columns([1, 1, 2])
    d1.download_button("Unduh ringkasan pegawai", resp.drop(columns=["nip"]).to_csv(index=False).encode("utf-8-sig"), "ringkasan_pegawai.csv", "text/csv", width="stretch")
    d2.download_button("Unduh seluruh jawaban", df.drop(columns=["sudah"]).to_csv(index=False).encode("utf-8-sig"), "jawaban_akpk.csv", "text/csv", width="stretch",
                       help="Berisi NIP lengkap. Simpan dengan hati-hati.")
