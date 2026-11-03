# -*- coding: utf-8 -*-
"""Sumber data awal: 32 jabatan BPSDM Prov. Sultra dari DRAFT AKPK.
Dipakai hanya oleh build_master.py untuk membuat data/master_akpk.xlsx.
Setelah itu, master cukup diedit langsung di file Excel tersebut."""

W, WJ, D, B, L = "Wajib (Anjab)", "Wajib (ketentuan JF)", "Dianjurkan", "Bersyarat", "Pelengkap"
KEP, MAN, TEK, TF, FUN, DAS = "Kepemimpinan", "Manajerial / Teknis", "Teknis", "Teknis fungsional", "Fungsional", "Dasar"
SP, SE, AS = "Sertifikasi Profesi", "Sertifikasi", "Asesmen"
A_KD = "Anjab - Kualifikasi Diklat"
A_TP = "Tugas pokok & keterampilan kerja Anjab"

# (kategori, nama, info_kelas, [pelatihan], [sertifikasi])
# item = (nama, jenis, dasar, status, penyelenggara)
J = []
def add(kat, nama, info, p, s): J.append((kat, nama, info, p, s))

STR, JFT, PEL = "Struktural / Manajerial", "Jabatan Fungsional", "Jabatan Pelaksana"
PKA = ("Pelatihan Kepemimpinan Administrator (PKA / Diklatpim III)", KEP, A_KD, W, "LAN / BPSDM Prov. Sultra")
PKP = ("Pelatihan Kepemimpinan Pengawas (PKP / Diklatpim IV)", KEP, A_KD, W, "LAN / BPSDM Prov. Sultra")
LATSAR = ("Pelatihan Dasar CPNS (Latsar) / Pelatihan Prajabatan", "Dasar", A_KD, W, "BPSDM Prov. Sultra; LAN")
TOC_S = ("Sertifikasi Pengelola Pelatihan (TOC)", SP, "SKJ Kediklatan", D, "LAN RI")
ADM = "Administrator / Eselon III.b / Kelas 11 / Gol. III/d - IV/a"
PWS = "Pengawas / Eselon IV.a / Kelas 9 / Gol. III/c - III/d"

add(STR, "Kepala Badan Pengembangan Sumber Daya Manusia", "JPT Pratama / Eselon II.a / Kelas 15 / Gol. IV/c - IV/d", [
 ("Pelatihan Kepemimpinan Nasional Tingkat II (PKN II / Diklatpim II) - Pelatihan Kepemimpinan Pratama", KEP, A_KD, W, "LAN / lembaga terakreditasi"),
 ("Diklat manajerial / non-manajerial di bidang Kediklatan dan Pengembangan SDM (mis. Manajemen Penyelenggaraan Pelatihan, Penjaminan Mutu Pelatihan, Kebijakan Bangkom ASN)", MAN, A_KD, W, "LAN / BPSDM Prov. Sultra (bila terakreditasi); LAN; BKN; Kemendagri (Regional Makassar)"),
 ("Diklat Pengembangan Kompetensi (mis. Manajemen Pengembangan Kompetensi ASN, Analisis Kebutuhan Pelatihan tingkat kebijakan, Evaluasi Pascapelatihan)", TEK, A_KD, W, "LAN / lembaga terakreditasi; LAN; BKN"),
 ("Manajemen Talenta dan Sistem Merit ASN", "Manajerial", A_TP, D, "BKN; Kemenpan RB"),
 ("Akuntabilitas Kinerja, Reformasi Birokrasi dan Pengelolaan Anggaran bagi Pengguna Anggaran", "Manajerial", A_TP, D, "Kemenpan RB; BPKP (Pusdiklatwas); Kemenkeu - BPPK / DJPb"),
 ("Kepemimpinan Transformasional dan Transformasi Digital Pembelajaran", "Manajerial", A_TP, D, "LAN / lembaga terakreditasi LAN; Komdigi (Digital Talent Scholarship) / Diskominfo Prov."),
],[
 ("Asesmen kompetensi manajerial dan sosial kultural (JPT Pratama)", AS, "Standar Kompetensi Jabatan (Permenpan RB 38/2017)", D, "BKN / pusat asesmen terakreditasi; BPSDM Prov. Sultra"),
 ("Sertifikasi Pengadaan Barang/Jasa Pemerintah (bila menjadi Pengguna Anggaran/KPA)", SE, "Peran dalam pengelolaan anggaran", B, "LKPP"),
])

add(STR, "Sekretaris Badan Pengembangan Sumber Daya Manusia", "Administrator / Eselon III.a / Kelas 12 / Gol. IV/a - IV/b", [
 PKA,
 ("Diklat manajerial / non-manajerial yang berhubungan dengan kesekretariatan (mis. Manajemen Kesekretariatan, Perkantoran Modern, Kehumasan)", MAN, A_KD, W, "LAN / BPSDM Kemendagri (Regional Makassar); BPSDM Prov. Sultra"),
 ("Diklat teknis kesekretariatan (mis. Tata Naskah Dinas & Kearsipan, Pengelolaan Barang Milik Daerah, Administrasi Kepegawaian)", TEK, A_KD, W, "ANRI (Pusdiklat Kearsipan); BPSDM Kemendagri; BKN"),
 ("Penyusunan Renstra, Renja, RKA/DPA dan Laporan Kinerja (SAKIP)", TEK, "Tugas pokok Sekretaris", D, "Bappenas (Pusbindiklatren) / Bappeda; Kemenpan RB; BPKP"),
 ("Pengelolaan Keuangan Daerah dan Penatausahaan Keuangan (SIPD)", TEK, "Tugas pokok Sekretaris", D, "BPSDM Kemendagri; Kemenkeu - BPPK / DJPb"),
 ("Manajemen ASN: Manajemen Kinerja, Disiplin dan Pengembangan Karier", TEK, "Tugas pokok Sekretaris", D, "BKN; LAN / lembaga terakreditasi LAN"),
 ("Coaching, Mentoring dan Pembinaan Bawahan", "Manajerial", A_TP, D, "LAN / BPSDM Prov. Sultra"),
],[
 ("Asesmen Kompetensi Manajerial & Sosio-Kultural Administrator", AS, "Standar Kompetensi Jabatan", D, "BKN / UPT Assessment Center"),
 ("Sertifikasi Pengadaan Barang/Jasa Pemerintah (bila ditunjuk PPK)", SE, "Penugasan", B, "LKPP"),
])

add(STR, "Kepala Bidang Sertifikasi Kompetensi dan Pengelolaan Kelembagaan", ADM, [
 PKA,
 ("Diklat manajerial / non-manajerial yang berhubungan dengan Sertifikasi Kompetensi dan Pengelolaan Kelembagaan", MAN, A_KD, W, "LAN / BPSDM Kemendagri; BKN"),
 ("Manajemen Lembaga Sertifikasi Profesi (LSP) dan Tempat Uji Kompetensi (TUK)", TEK, A_TP, D, "BNSP / LSP terlisensi"),
 ("Penjaminan Mutu dan Akreditasi Lembaga Pelatihan", TEK, A_TP, D, "LAN / lembaga terakreditasi LAN"),
 ("Pengembangan Kerja Sama Kelembagaan & Kemitraan Kediklatan", "Manajerial", A_TP, D, "BPSDM Kemendagri; LAN"),
],[
 ("Sertifikasi Asesor Kompetensi (BNSP) atau Manajer/Pengelola Sertifikasi", SP, "Bidang tugas", D, "BNSP / LSP terlisensi"),
])

add(STR, "Kepala Bidang Pengembangan Kompetensi Teknis Inti", ADM, [
 PKA,
 ("Management of Training (MOT) Diklat Teknis Substansial", TEK, A_KD, W, "LAN RI; Kementerian Teknis Sektoral"),
 ("Analisis Kebutuhan Diklat (AKD) Teknis Pemerintahan & Urusan Daerah", TEK, A_TP, D, "LAN RI; BPSDM Kemendagri"),
 ("Pemetaan Standar Kompetensi Teknis Jabatan (Permenpan RB 38/2017)", TEK, A_TP, D, "Kemenpan RB; BKN"),
 ("Pengembangan Pembelajaran Berbasis Mikrolearning & Digital", TEK, "Tugas pokok Anjab", D, "LAN RI; Komdigi"),
],[
 ("Sertifikasi Pengelola Pelatihan (MOT) Terakreditasi", SP, "SKJ Kediklatan", D, "LSP / LAN RI"),
])

add(STR, "Kepala Bidang Pengembangan Kompetensi Teknis Umum dan Fungsional", ADM, [
 PKA,
 ("Management of Training (MOT) / Diklat Pengelolaan Pelatihan Fungsional", TEK, A_KD, W, "LAN RI; Instansi Pembina Jabatan Fungsional"),
 ("Tata Kelola & Penyetaraan Jabatan Fungsional ASN", TEK, A_TP, D, "BKN; KemenPANRB"),
 ("Analisis Kebutuhan Diklat Fungsional & Evaluasi Pascapelatihan", TEK, A_TP, D, "LAN RI"),
],[
 ("Sertifikasi Evaluator Pelatihan / Pengelola Pelatihan", SP, "SKJ Kediklatan", D, "LSP / LAN RI"),
])

add(STR, "Kepala Bidang Pengembangan Kompetensi Manajerial", ADM, [
 PKA,
 ("Management of Training (MOT) Penyelenggaraan Diklat Kepemimpinan (PKN/PKA/PKP)", TEK, A_KD, W, "LAN RI"),
 ("Pelatihan Penyelenggara Pelatihan Kepemimpinan / Coaching Mentoring Kepemimpinan", TEK, A_TP, D, "LAN RI"),
 ("Penyusunan Sasaran Kinerja, SAKIP/LAKIP dan Manajemen Kinerja", "Manajerial / Teknis", A_TP, D, "Kemenpan RB; BPKP (Pusdiklatwas); LAN"),
],[
 ("Sertifikasi Coach / Fasilitator Kepemimpinan", SP, "SKJ Kediklatan", D, "LAN RI / BNSP"),
])

add(STR, "Kepala Sub Bagian Keuangan", PWS, [
 PKP,
 ("Diklat Penatausahaan Keuangan (Pejabat Penatausahaan Keuangan, SIPD, SAP Akrual)", TEK, A_KD, W, "BPSDM Kemendagri; Kemenkeu - BPPK / DJPb; BPKAD"),
 ("Diklat Penyusunan LAKIP (SAKIP, Indikator Kinerja Utama, Laporan Kinerja)", TEK, A_KD, W, "Kemenpan RB; BPKP; LAN"),
 ("Diklat Pengadaan Barang/Jasa Pemerintah (PBJ Dasar)", TEK, A_KD, W, "LKPP"),
 ("Pengelolaan Keuangan Daerah dan Perpajakan Instansi Pemerintah", TEK, A_TP, D, "BPSDM Kemendagri; DJP Kemenkeu"),
],[
 ("Sertifikasi PPK / PPSPM / Bendahara (DJPb)", SP, "Aturan Keuangan Negara", B, "Kemenkeu - BPPK / DJPb"),
 ("Sertifikasi Kompetensi Pengadaan Barang/Jasa Pemerintah (LKPP)", SP, "Diklat Barang/Jasa (Anjab)", D, "LKPP"),
])

add(STR, "Kepala Sub Bagian Umum dan Kepegawaian", PWS, [
 PKP,
 ("Diklat Analis Kepegawaian (administrasi kepegawaian, formasi, mutasi, SIASN)", TEK, A_KD, W, "BKN; BPSDM Kemendagri"),
 ("Diklat Manajemen Kearsipan (tata naskah dinas, kearsipan dinamis, SRIKANDI)", TEK, A_KD, W, "ANRI (Pusdiklat Kearsipan)"),
 ("Diklat Pengelola Aset (Pengelolaan Barang Milik Daerah/Negara)", TEK, A_KD, W, "BPSDM Kemendagri; Kemenkeu (DJKN); BPKAD"),
 ("Diklat penataan kelola sistem dan TIK (SPBE, keamanan informasi dasar)", TEK, A_KD, W, "Komdigi / Diskominfo Prov.; BSSN"),
 ("Penyusunan ANJAB, ABK, dan Evaluasi Jabatan", TEK, A_TP, D, "BKN; KemenPANRB"),
],[
 ("Sertifikasi Pengelola Kepegawaian / Kearsipan / PBJ", SP, "SKJ Tata Usaha", D, "BKN / ANRI / LKPP"),
])

add(STR, "Kepala Sub Bidang Pengembangan Kompetensi Jabatan Administrator dan Pengawas", PWS, [
 PKP,
 ("Diklat manajerial / non-manajerial yang berhubungan dengan Bangkom JA & Pengawas", MAN, A_KD, W, "LAN RI"),
 ("Course Design & Facilities Officer (CDFO) / Building Learning Commitment (BLC)", TEK, A_TP, D, "LAN RI"),
 ("Evaluasi Hasil Belajar & Aksi Perubahan Diklat Kepemimpinan", TEK, A_TP, D, "LAN RI"),
],[
 ("Sertifikasi Pengelola Pelatihan (TOC / CDFO)", SP, "SKJ Kediklatan", D, "LAN RI"),
])

add(STR, "Kepala Sub Bidang Pengembangan Kompetensi Pilihan", PWS, [
 PKP,
 ("Diklat manajerial / non-manajerial yang berhubungan dengan Bangkom Pilihan & Urusan Pemerintahan", MAN, A_KD, W, "LAN / BPSDM Kemendagri"),
 ("Training Officer Course (TOC) / Pengelolaan Pelatihan Teknis Pilihan", TEK, A_TP, D, "LAN RI; BPSDM Kemendagri"),
 ("Identifikasi Kebutuhan Diklat Teknis Spesifik Daerah & Kemitraan", TEK, A_TP, D, "BPSDM Prov. Sultra"),
],[TOC_S])

add(STR, "Kepala Sub Bidang Pengembangan Kompetensi Umum", PWS, [
 PKP,
 ("Diklat manajerial / non-manajerial yang berhubungan dengan Bangkom Umum & Latsar CPNS", MAN, A_KD, W, "LAN RI"),
 ("Training Officer Course (TOC) / Manajemen Diklat Orientasi PPPK", TEK, A_TP, D, "LAN RI"),
 ("Penyusunan Jadwal & Pengelolaan Evaluasi Peserta Diklat Umum", TEK, A_TP, D, "LAN RI"),
],[TOC_S])

# ---------------- Jabatan Fungsional ----------------
JF = "Ketentuan JF Widyaiswara"
def wid(nama, info, p, s): add(JFT, nama, info, p, s)

wid("Widyaiswara Ahli Utama", "Kelas 14 / Gol. IV/d - IV/e", [
 ("Pelatihan Manajerial Penjenjangan Widyaiswara Ahli Utama", "Manajerial", A_KD, W, "LAN RI"),
 ("Pelatihan Workplace Learning dan Strategi Kebijakan Pengembangan Kompetensi", TF, A_KD, W, "LAN RI"),
 ("Pelatihan Penulisan Buku / Jurnal Ilmiah (Dukungan Orasi Ilmiah Widyaiswara)", TF, "Persyaratan Ahli Utama (Anjab)", W, "LAN RI / Perguruan Tinggi"),
 ("Pelatihan Coaching & Mentoring Tingkat Lanjut (Executive Coaching)", TF, A_KD, W, "LAN RI"),
 ("Evaluasi Pascapelatihan Dampak Kebijakan Kediklatan (Impact Assessment)", TF, "Tugas pokok Widyaiswara", D, "LAN RI"),
],[
 ("Uji Kompetensi / Pra-Orasi Ilmiah Fungsional Widyaiswara Ahli Utama", SE, JF, WJ, "LAN RI"),
 ("Sertifikasi Master Coach / Executive Coach Professional", SP, "Penunjang Coaching", L, "Lembaga Coaching Terakreditasi (ICF/BNSP)"),
])
wid("Widyaiswara Ahli Madya", "Kelas 12 / Gol. IV/a - IV/c", [
 ("Pelatihan Manajerial Penjenjangan Widyaiswara Ahli Madya", "Manajerial", A_KD, W, "LAN RI"),
 ("Pelatihan Workplace Learning & Pengembangan Metode Learning Organization", TF, A_KD, W, "LAN RI"),
 ("Pengembangan Strategi Pembelajaran & Metodologi Penelitian Kediklatan", TF, A_KD, W, "LAN RI / BRIN"),
 ("Penulisan Karya Tulis Ilmiah (KTI) Kediklatan Terpublikasi", TF, A_KD, W, "LAN RI / Perguruan Tinggi"),
 ("Pelatihan Penjaminan Mutu Pembelajaran & Evaluasi Diklat", TF, "Tugas pokok Widyaiswara", D, "LAN RI"),
],[
 ("Uji Kompetensi Penjenjangan Fungsional Widyaiswara Ahli Madya", SE, JF, WJ, "LAN RI"),
 ("Sertifikasi Master Trainer / Fasilitator Pembelajaran (BNSP)", SP, "Tugas pokok Widyaiswara", D, "BNSP / LSP terlisensi"),
])
wid("Widyaiswara Ahli Muda", "Kelas 10 / Gol. III/c - III/d", [
 ("Pelatihan Manajerial Penjenjangan Widyaiswara Ahli Muda", "Manajerial", A_KD, W, "LAN RI"),
 ("Pengembangan Kurikulum Pelatihan & Pengolahan Bahan Ajar Digital", TF, A_KD, W, "LAN RI"),
 ("Pengembangan Modul Pelatihan & Media Pembelajaran Berbasis TIK", TF, A_KD, W, "LAN RI / Komdigi"),
 ("Pelatihan Coaching & Mentoring Pembelajaran", TF, A_KD, W, "LAN RI"),
 ("Metodologi Penelitian Dasar & Penulisan KTI", TF, A_KD, W, "LAN RI"),
],[
 ("Uji Kompetensi Penjenjangan Fungsional Widyaiswara Ahli Muda", SE, JF, WJ, "LAN RI"),
 ("Sertifikasi Trainer / Fasilitator Pelatihan (BNSP)", SP, "Tugas pokok Widyaiswara", D, "BNSP / LSP terlisensi"),
])
wid("Widyaiswara Ahli Pertama", "Kelas 8 / Gol. III/a - III/b", [
 ("Pelatihan Fungsional Widyaiswara Pertama (Diklat Cawi / TOT Dasar)", FUN, A_KD, W, "LAN RI"),
 ("Analisis Kebutuhan Pelatihan (AKP / AKD Dasar)", TF, A_KD, W, "LAN RI"),
 ("Perancangan Program Pelatihan & Penyusunan Rancang Bangun Pembelajaran (RBPMP)", TF, A_KD, W, "LAN RI"),
 ("Pengembangan Media Pembelajaran Presentasi & TIK", TF, A_KD, W, "LAN RI / Komdigi"),
 ("Literasi Digital & Etika Pembelajaran ASN", TF, A_KD, W, "LAN RI / Komdigi"),
],[
 ("Uji Kompetensi / Kelulusan Diklat Fungsional Widyaiswara Pertama", SE, JF, WJ, "LAN RI"),
 ("Sertifikasi Trainer Level 4 BNSP (Bila Tersedia)", SP, "Penunjang Tugas", L, "BNSP / LSP terlisensi"),
])

JFP = "Ketentuan JF Perencana"
add(JFT, "Perencana Ahli Madya", "Kelas 12 / Gol. IV/a - IV/c", [
 ("Diklat Fungsional Penjenjangan Perencana Ahli Madya", FUN, A_KD, W, "Bappenas (Pusbindiklatren)"),
 ("Perencanaan Strategis Pembangunan Daerah & Analisis Kebijakan Makro", TEK, "Tugas jenjang Madya Anjab", D, "Bappenas / LAN RI"),
 ("Penganggaran Berbasis Kinerja Lanjutan & Evaluasi Kerangka Pendanaan (SIPD)", TEK, "Tugas pokok Perencana", D, "Bappenas / Kemenkeu - DJPb"),
 ("Analisis Ekonometrika & Data Statistik Pembangunan Spasial", TEK, "Tugas pokok Perencana", D, "BPS / Bappenas / Perguruan Tinggi"),
],[
 ("Uji Kompetensi Kenaikan Jenjang Fungsional Perencana Ahli Madya", SE, JFP, WJ, "Bappenas (Pusbindiklatren)"),
 ("Sertifikasi Perencana Pembangunan Utama / Madya Terregistrasi", SP, "SKJ Perencana", D, "LSP Bappenas / AP2I"),
])
add(JFT, "Perencana Ahli Muda", "Kelas 10 / Gol. III/c - III/d", [
 ("Diklat Fungsional Penjenjangan Perencana Ahli Muda", FUN, A_KD, W, "Bappenas (Pusbindiklatren)"),
 ("Penyusunan Perencanaan Pembangunan Daerah (Renstra, Renja SKPD)", TEK, A_TP, D, "Bappenas / Bappeda Prov."),
 ("Monitoring & Evaluasi Kinerja Program Pembangunan (SAKIP / LAKIP)", TEK, A_TP, D, "Bappenas; KemenPANRB; BPKP"),
 ("Analisis Data Perencanaan & Pengelolaan Satu Data Indonesia", TEK, "Tugas pokok Perencana", D, "BPS; Bappenas; Diskominfo"),
],[
 ("Uji Kompetensi Kenaikan Jenjang Fungsional Perencana Ahli Muda", SE, JFP, WJ, "Bappenas (Pusbindiklatren)"),
 ("Sertifikasi Perencana Pembangunan Muda Terregistrasi", SP, "SKJ Perencana", D, "LSP Bappenas / AP2I"),
])
add(JFT, "Perencana Ahli Pertama", "Kelas 8 / Gol. III/a - III/b", [
 ("Diklat Fungsional Pertama Perencana / Pelatihan Dasar Perencanaan Pembangunan", FUN, A_KD, W, "Bappenas (Pusbindiklatren)"),
 ("Pengumpulan Data, Identifikasi Masalah & Penyusunan Draft Program Kerja", TEK, "Tugas pokok Perencana", D, "Bappenas / Bappeda Prov."),
 ("Teknik Analisis Data Statistik Deskriptif Perencanaan", TEK, "Tugas pokok Perencana", D, "BPS; Diskominfo"),
 ("Penyusunan RKA / DPA dan Dokumen Penganggaran Dasar (SIPD)", TEK, "Tugas pokok Perencana", D, "BPSDM Kemendagri / BPKAD"),
],[
 ("Uji Kompetensi Pengangkatan Pertama Fungsional Perencana", SE, JFP, WJ, "Bappenas (Pusbindiklatren)"),
 ("Sertifikasi BNSP Bidang Analisis Data / Perencanaan", SP, "Penunjang", L, "BNSP / LSP terlisensi"),
])

JA = "Ketentuan JF Analis SDM"
add(JFT, "Analis Sumber Daya Manusia Aparatur Ahli Madya", "Kelas 12 / Gol. IV/a - IV/c", [
 ("Pelatihan Fungsional Penjenjangan Analis SDM Aparatur Ahli Madya", FUN, A_KD, W, "Pusdiklat BKN"),
 ("Perumusan Kebijakan Internal Manajemen SDM Aparatur & Human Capital Master Plan", TEK, A_KD, W, "BKN; KemenPANRB"),
 ("Manajemen Talenta Nasional, Talent Pool, & Evaluasi Sistem Merit", TEK, "Tugas jenjang Madya Anjab", D, "BKN; KemenPANRB"),
 ("Analisis & Evaluasi Jabatan Tingkat Instansi / Pemetaan Kompleksitas SDM", TEK, "Tugas pokok Analis SDM", D, "KemenPANRB; BKN"),
],[
 ("Uji Kompetensi Kenaikan Jenjang Analis SDM Aparatur Ahli Madya", SE, JA, WJ, "BKN"),
 ("Sertifikasi Lead Asesor SDM Aparatur / Manager SDM BNSP", SP, "Perka BKN 50/2015", D, "BKN / BNSP / LSP"),
])
add(JFT, "Analis Sumber Daya Manusia Aparatur Ahli Muda", "Kelas 10 / Gol. III/c - III/d", [
 ("Pelatihan Fungsional Penjenjangan Analis SDM Aparatur Ahli Muda", FUN, A_KD, W, "Pusdiklat BKN"),
 ("Penyusunan ANJAB, ABK, Evaluasi Jabatan, & Peta Jabatan", TEK, A_KD, W, "BKN; KemenPANRB"),
 ("Penyusunan Standar Kompetensi Jabatan (SKJ) & Profil Kompetensi ASN", TEK, "Standar Kompetensi Jabatan", D, "BKN; KemenPANRB"),
 ("Manajemen Kinerja ASN (PermenPANRB 6/2022) & Pengelolaan e-Kinerja BKN", TEK, "Tugas pokok Analis SDM", D, "BKN"),
 ("Analisis Kebutuhan Pengembangan Kompetensi (AKPK/HCDP) Unit Kerja", TEK, "Tugas pokok Analis SDM", D, "LAN RI; BKN"),
],[
 ("Uji Kompetensi Kenaikan Jenjang Analis SDM Aparatur Ahli Muda", SE, JA, WJ, "BKN"),
 ("Pelatihan / Sertifikasi Asesor SDM Aparatur (BKN)", SP, "Perka BKN 50/2015", D, "BKN / BNSP"),
])
add(JFT, "Analis Sumber Daya Manusia Aparatur Ahli Pertama", "Kelas 8 / Gol. III/a - III/b", [
 ("Pelatihan Fungsional Pembentukan Analis SDM Aparatur Ahli Pertama", FUN, A_KD, W, "Pusdiklat BKN"),
 ("Pengolahan Data Administrasi Kepegawaian, Formasi, & SIASN BKN", TEK, A_KD, W, "BKN; BKD Prov."),
 ("Penyusunan Dokumen Pendukung ANJAB & ABK Sederhana", TEK, "Tugas pokok Analis SDM", D, "BKN; Kemendagri"),
 ("Pelayanan Administrasi Kenaikan Pangkat, Pensiun, & Disiplin Pegawai", TEK, "Tugas pokok Analis SDM", D, "BKN"),
],[
 ("Uji Kompetensi Pengangkatan Pertama Fungsional Analis SDM Aparatur", SE, JA, WJ, "BKN"),
 ("Sertifikasi BNSP Bidang Manajemen SDM / Staf Kepegawaian", SP, "Penunjang", L, "BNSP / LSP terlisensi"),
])

JP = "Ketentuan JF Pranata Komputer"
add(JFT, "Pranata Komputer Ahli Madya", "Kelas 11 / Gol. IV/a - IV/c", [
 ("Pelatihan Fungsional Penjenjangan Pranata Komputer Ahli Madya", FUN, A_KD, W, "Pusdiklat BPS; Komdigi"),
 ("Tata Kelola TI (IT Governance COBIT/ITIL) & Management Proyek TI Kediklatan", TEK, "Tugas jenjang Madya Anjab", D, "Komdigi; Lembaga TIK"),
 ("Arsitektur Sistem Informasi Pemerintah, SPBE, & Enterprise Architecture", TEK, "Tugas pokok Prakom", D, "KemenPANRB; Komdigi"),
 ("Manajemen Keamanan Informasi (ISO 27001 Lead Auditor) & Disaster Recovery Plan", TEK, "Tugas pokok Prakom", D, "BSSN; Komdigi"),
],[
 ("Uji Kompetensi Kenaikan Jenjang Pranata Komputer Ahli Madya", SE, JP, WJ, "BPS"),
 ("Sertifikasi Manager TIK / IT Project Manager / CISM / COBIT", SP, "SKKNI / Internasional", D, "LSP TIK / ISACA / BSSN"),
])
add(JFT, "Pranata Komputer Ahli Muda", "Kelas 9 / Gol. III/c - III/d", [
 ("Pelatihan Fungsional Penjenjangan Pranata Komputer Ahli Muda", FUN, A_KD, W, "Pusdiklat BPS; Komdigi"),
 ("Pengembangan & Integrasi LMS (Jalur ASN / Moodle API / Web Service)", TEK, A_KD, W, "Komdigi; Diskominfo"),
 ("Administrasi Basis Data Lanjutan (Oracle/MySQL Cluster) & Data Warehouse", TEK, A_KD, W, "Pusdiklat BPS; Komdigi"),
 ("Audit Keamanan Informasi Dasar & Security Vulnerability Assessment", TEK, "Tugas pokok Prakom", D, "BSSN; Komdigi"),
],[
 ("Uji Kompetensi Kenaikan Jenjang Pranata Komputer Ahli Muda", SE, JP, WJ, "BPS"),
 ("Sertifikasi Senior Developer / Database Administrator / Cyber Security Analyst", SP, "SKKNI / Vendor", D, "BNSP / LSP TIK / Oracle / CompTIA"),
])
add(JFT, "Pranata Komputer Ahli Pertama", "Kelas 8 / Gol. III/a - III/b", [
 ("Pelatihan Fungsional Pembentukan Pranata Komputer Ahli Pertama", FUN, A_KD, W, "Pusdiklat BPS; Komdigi"),
 ("Pemrograman Web / Mobile Dasar & Maintenance Aplikasi / Platform", TEK, A_KD, W, "Diskominfo; Komdigi"),
 ("Pengelolaan Jaringan Komputer Perkantoran (Router/Switch/Wi-Fi) & Server", TEK, A_KD, W, "Komdigi; Diskominfo"),
 ("Teknik Backup Data, Troubleshooting Hardware/Software, & User Support", TEK, "Tugas pokok Prakom", D, "Diskominfo; BPSDM Prov. Sultra"),
],[
 ("Uji Kompetensi Pengangkatan Pertama Pranata Komputer Ahli Pertama", SE, JP, WJ, "BPS"),
 ("Sertifikasi Junior Web Developer / Network Administrator (CCNA/BNSP)", SP, "SKKNI / Vendor", D, "BNSP / LSP TIK / Cisco"),
])

# ---------------- Jabatan Pelaksana ----------------
TK = "Anjab - Diklat Teknis Unit"
def pel(nama, info, p, s): add(PEL, nama, info, [LATSAR] + p, s)

pel("Penelaah Teknis Kebijakan", "Kelas Jabatan 7 / Kualifikasi S-1/D-IV / Gol. III/a - III/d", [
 ("Diklat Ketatausahaan, TOC, atau Diklat Teknis Sesuai Unit Kerja (Keuangan/Umum/Diklat)", TEK, TK, W, "LAN; BPSDM Kemendagri; ANRI; BPKAD"),
 ("Penyusunan Telaahan Teknis, Naskah Kebijakan, & Ringkasan Eksekutif", TEK, "Tugas pokok Anjab", D, "LAN RI; BPSDM Kemendagri"),
 ("Tata Naskah Dinas, Penulisan Laporan, & Pengelolaan Dokumen Digital", TEK, "Tugas pokok Anjab", D, "ANRI; Diskominfo"),
 ("Pengolahan dan Visualisasi Data (MS Excel Advanced)", TEK, "Keterampilan kerja Anjab", D, "BPS; Komdigi"),
],[
 ("Asesmen Kompetensi Pelaksana (Klerek)", AS, "SKJ Pelaksana KepmenPANRB 282/2025", D, "BPSDM Prov. Sultra"),
 ("Sertifikasi PBJ Pemerintah / Sertifikasi Bendahara (Bila Ditunjuk)", SP, "Penugasan", B, "LKPP / Kemenkeu"),
])
pel("Penata Layanan Operasional", "Kelas Jabatan 7 / Kualifikasi S-1/D-IV / Gol. III/a - III/d", [
 ("Diklat teknis terkait penataan layanan operasional & Pelayanan Prima", TEK, A_KD, W, "LAN RI; BPSDM Kemendagri"),
 ("Penyusunan SOP Layanan & Analisis Data Kinerja Layanan Kediklatan", TEK, "Tugas pokok Anjab", D, "Kemenpan RB; LAN RI"),
 ("Pengelolaan Pengaduan Masyarakat (SP4N-LAPOR!) & Communication Skill", TEK, "Tugas pokok Anjab", D, "Diskominfo; BPSDM"),
],[("Sertifikasi BNSP Bidang Layanan Pelanggan / Administrasi", SP, "Penunjang Kompetensi", L, "BNSP / LSP terlisensi")])
pel("Penata Kelola Sistem dan Teknologi Informasi", "Kelas Jabatan 7 / Kualifikasi S-1/D-IV TI / Gol. III/a - III/d", [
 ("Diklat Pengelolaan Sistem Informasi / Training Officer Course (Unit SKPK)", TEK, TK, W, "LAN RI; BPSDM Kemendagri"),
 ("IT Service Desk, Helpdesk, & Support Perangkat Pengguna", TEK, "Tugas pokok Anjab", D, "Diskominfo; BPSDM Sultra"),
 ("Pengelolaan Website, Konten Digital SPBE, & Keamanan Informasi Dasar", TEK, "Tugas pokok Anjab", D, "Komdigi; BSSN"),
],[("Sertifikasi Basic IT Support / CompTIA / BNSP TIK", SP, "SKKNI TIK", D, "LSP TIK / BNSP")])
pel("Pengolah Data dan Informasi", "Kelas Jabatan 6 / Kualifikasi D-III / Gol. II/c - II/d", [
 ("Diklat Ketatausahaan, TOC, atau Pengelolaan SIMPEG/Pencairan Dana (Sesuai Unit)", TEK, TK, W, "LAN; ANRI; BKN; BPKAD"),
 ("Pengolahan Data Statistik, MS Excel Advanced, & Cleansing Data Peserta", TEK, "Tugas pokok Anjab", D, "BPS; Diskominfo"),
 ("Satu Data Indonesia & Visualisasi Dashboard Sederhana", TEK, "Tugas pokok Anjab", D, "BPS; Bappenas"),
],[("Sertifikasi BNSP Pengolahan Data / Operator Komputer", SP, "Penunjang Kompetensi", L, "BNSP / LSP terlisensi")])
pel("Pengelola Layanan Operasional", "Kelas Jabatan 6 / Kualifikasi D-III / Gol. II/c - II/d", [
 ("Diklat Kepranataan Diklat, TOC, atau Pengelolaan Asrama & Sarpras (Sesuai Unit)", TEK, TK, W, "LAN; BPSDM Kemendagri; DJKN"),
 ("Pelayanan Prima (Hospitality) & Pengelolaan Logistik Kediklatan", TEK, "Tugas pokok Anjab", D, "BPSDM Sultra; LAN"),
 ("K3 Dasar Perkantoran, Tanggap Darurat, & Pemadam Kebakaran", TEK, "Tugas pokok Anjab", D, "Disnaker; Damkar; PMI"),
],[("Sertifikat Petugas K3 / Penanggulangan Kebakaran", SP, "Penunjang Tugas", L, "Kemnaker / Damkar")])
pel("Pengadministrasi Perkantoran", "Kelas Jabatan 5 / Kualifikasi SLTA / Gol. II/a - II/b", [
 ("Diklat Ketatausahaan, TOC, Pengadministrasian Umum/Keuangan/Kepegawaian", TEK, TK, W, "LAN; ANRI; BKN; Kemenkeu"),
 ("Kearsipan Dasar, Tata Naskah Dinas Elektronik (SRIKANDI)", TEK, "Tugas pokok Anjab", D, "ANRI (Pusdiklat Kearsipan)"),
 ("Aplikasi Perkantoran (MS Word, MS Excel) & Administrasi Perkantoran", TEK, "Keterampilan kerja Anjab", D, "Komdigi / BLK"),
],[("Sertifikasi BNSP Administrasi Perkantoran", SP, "Penunjang Kompetensi", L, "BNSP / LSP terlisensi")])
pel("Operator Layanan Operasional", "Kelas Jabatan 5 / Kualifikasi SLTA / Gol. II/a - II/b", [
 ("Diklat Teknis Operator Layanan Operasional / Keamanan & Ketertiban", TEK, A_KD, W, "LAN; BPSDM Kemendagri"),
 ("Pengoperasian Peralatan AV, Sound System, & Micro-Bar Kediklatan", TEK, "Tugas pokok Anjab", D, "BPSDM Sultra / Teknisi"),
 ("Keselamatan dan Kesehatan Kerja (K3) Dasar Perkantoran", TEK, "Tugas pokok Anjab", D, "Disnaker / BPSDM Sultra"),
],[("Pelatihan Gada Pratama (Satpam) - bila bertugas di bidang keamanan", SP, "Penugasan", B, "Polri / Lembaga Satpam")])
pel("Pengelola Umum Operasional", "Kelas Jabatan 3 / Kualifikasi SLTP / Gol. I/c - I/d", [
 ("Diklat teknis terkait pengelolaan umum operasional & Kebersihan Sarana", TEK, A_KD, W, "LAN; BPSDM Kemendagri"),
 ("Diklat pelayanan administrasi kepegawaian, umum, & jaringan informasi", TEK, A_KD, W, "BKN; Kemenpan RB; Kemendagri"),
 ("Ketatausahaan Dasar, Penanganan Surat, & Pelayanan Prima Internal", TEK, "Tugas pokok Anjab", D, "BPSDM Sultra; ANRI"),
],[("Sertifikasi BNSP Layanan / Administrasi Operasional", SP, "Penunjang Kompetensi", L, "BNSP / LSP terlisensi")])

assert len(J) == 32, len(J)
