# AKPK BPSDM Provinsi Sulawesi Tenggara

Dua aplikasi web (Python + Streamlit):

| Berkas | Fungsi | Pengguna |
|---|---|---|
| `app_kuesioner.py` | Kuesioner AKPK. Jawaban langsung masuk ke Google Sheets | Seluruh pegawai |
| `app_dashboard.py` | Dashboard grafik interaktif dan temuan, dilindungi kata sandi | Pimpinan dan analis SDM |

Data rekomendasi (32 jabatan, 193 pelatihan/sertifikasi) diambil dari DRAFT AKPK dan ada di `data/master_akpk.xlsx`.

## Langkah 1 - Coba di komputer sendiri (tanpa Google, 5 menit)

1. Pasang Python 3.10 atau lebih baru dari python.org.
2. Buka terminal di folder ini, lalu:
   ```
   pip install -r requirements.txt
   streamlit run app_kuesioner.py
   ```
3. Di terminal kedua: `streamlit run app_dashboard.py --server.port 8502`

Tanpa pengaturan Google, jawaban disimpan di `data/responses.csv`, dan dashboard menyalakan "data contoh (fiktif)" otomatis selama belum ada jawaban asli.

## Langkah 2 - Hubungkan ke Google Sheets

1. Buat Google Sheet kosong, misalnya "AKPK BPSDM Sultra". Salin ID-nya dari URL (antara `/d/` dan `/edit`).
2. Buka console.cloud.google.com, buat proyek, lalu aktifkan **Google Sheets API** dan **Google Drive API**.
3. Menu IAM & Admin > Service Accounts > buat service account > tab Keys > Add key > JSON. Berkas JSON terunduh.
4. Buka Google Sheet tadi, klik Bagikan, lalu tambahkan alamat `client_email` dari berkas JSON sebagai **Editor**.
5. Salin `.streamlit/secrets.toml.example` menjadi `.streamlit/secrets.toml`, isi `spreadsheet_id`, `dashboard_password`, dan blok `gcp_service_account` dari berkas JSON.
6. Jalankan ulang. Kuesioner akan menulis ke sheet "Jawaban" (dibuat otomatis, satu baris per pelatihan per pegawai).

## Langkah 3 - Pasang online (gratis) di Streamlit Community Cloud

1. Unggah folder ini ke repositori GitHub **privat**. Berkas `secrets.toml` jangan ikut (sudah ada di `.gitignore`).
2. Di share.streamlit.io, buat **dua app** dari repositori yang sama: satu dengan Main file `app_kuesioner.py`, satu dengan `app_dashboard.py`.
3. Untuk keduanya, buka Settings > Secrets dan tempel isi `secrets.toml`.
4. Bagikan tautan kuesioner ke pegawai. Tautan dashboard hanya untuk pimpinan dan analis.

## Mengubah daftar pelatihan

Edit `data/master_akpk.xlsx` (sheet `Master` berisi pelatihan, `Jabatan` berisi daftar jabatan), simpan, lalu unggah ulang ke GitHub. Kode tidak perlu diubah. Kolom `penyelenggara_kunci` dipakai untuk rekap per penyelenggara. Pemetaannya ada di `build_master.py`.

Daftar unit kerja dan golongan ada di `common.py` (`UNIT_KERJA`). **Periksa dan sesuaikan** daftar unit kerja dengan struktur organisasi yang berlaku, karena dokumen sumber tidak merinci unit kerja tiap sub bidang.

## Catatan penting

- Satu NIP yang mengisi berulang: dashboard memakai pengisian terbaru.
- Dashboard menyamarkan NIP di tabel. Tombol "Unduh seluruh jawaban" berisi NIP lengkap, jadi simpan dengan hati-hati.
- Data pegawai bersifat pribadi. Pastikan hosting dan penyimpanan sesuai kebijakan instansi, dan batasi akses ke Google Sheet.
- Bila data tidak boleh keluar dari server instansi, aplikasi ini bisa dijalankan di server sendiri (mode berkas lokal atau Docker).
