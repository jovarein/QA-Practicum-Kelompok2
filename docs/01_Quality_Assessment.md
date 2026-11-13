# P01 — Software Quality Assessment

> **Objek uji:** Filmory (nama paket `drama_review_app`) — https://github.com/jovarein/Drama-Review-MobileApp
> **Versi / commit:** `1.0.0+1` / `84190e0` (satu-satunya commit: "add flutter project files")
> **Pendekatan:** analisis statis seluruh kode sumber (±7.200 baris Dart, 45+ berkas) + pengujian fungsional manual pada perangkat Android. Seluruh data uji adalah data *dummy*.

## 1. Tujuan sistem dan pengguna

| Aspek | Uraian |
|---|---|
| Deskripsi | Aplikasi mobile (Flutter) untuk menemukan drama Korea, membaca detailnya, menulis review & rating, menyukai/mengomentari review, menyimpan watchlist, dan berdiskusi di forum. |
| Tujuan bisnis | Menyediakan komunitas ulasan drama yang ringan di atas data katalog TMDB. |
| Pengguna utama | (1) **Penonton/pengulas** — mencari drama, menulis review, menyimpan watchlist. (2) **Anggota komunitas forum** — membuat topik & membalas. (3) **Pemilik akun** — mengelola profil, foto, username, password. |
| Arsitektur ringkas | Flutter + Riverpod (state), Firebase Auth (email/password & Google), Cloud Firestore (users, reviews, comments, forum_threads/posts, watchlist), Firebase Storage (foto profil), FCM (notifikasi), TMDB REST API (katalog). |
| Alur utama yang diuji | Splash → Login/Register → Home → Detail drama → Tulis review → Like/Komentar → Watchlist → Forum → Pengaturan akun. |

## 2. Atribut kualitas yang dipilih (ISO/IEC 25010)

| # | Atribut | Mengapa penting bagi Filmory | Indikator/ukuran | Bukti awal |
|---|---|---|---|---|
| 1 | **Functional suitability** (kelengkapan & ketepatan fungsi) | Inti produk adalah review, like, komentar, watchlist; fitur yang tampak tapi tidak bekerja merusak kepercayaan. | % requirement yang lolos uji; jumlah fitur tidak lengkap | Tombol hapus review kosong (D-01); review ganda tidak dibatasi (D-04); pencarian terpotong (D-03) |
| 2 | **Reliability** (ketahanan & penanganan kegagalan) | Aplikasi bergantung pada TMDB & Firebase; jaringan seluler tidak stabil. | Tidak crash saat offline; pesan error benar; konsistensi data | Reset password menampilkan sukses palsu (D-02); data yatim saat hapus topik (D-08); error mentah (D-11) |
| 3 | **Security** (kerahasiaan & kontrol akses) | Menyimpan akun, email, foto, dan konten pengguna. | Tidak ada rahasia di VCS; otorisasi di sisi server | `.env` berisi TMDB key ter-commit, `google-services.json` publik, tidak ada `firestore.rules` (D-05) |
| 4 | **Usability** (kemudahan & umpan balik) | Pengguna awam harus paham status dan kesalahan. | Pesan validasi jelas; umpan balik pada setiap aksi | Komentar kosong diabaikan tanpa umpan balik (analisis kode; di luar 21 TC); validasi email hanya oleh Firebase; teks exception mentah (D-11) |
| 5 | **Maintainability** | Proyek akan berkembang; regresi harus mudah dideteksi. | Keberadaan test otomatis & kode mati | `widget_test.dart` contoh counter yang gagal (D-06); kode FCM mati (D-10) |

Atribut 1–3 adalah **fokus utama** (sesuai syarat minimal 3); atribut 4–5 diuji sebagai pendukung.

## 3. Potensi masalah kualitas dan dampaknya (≥3)

| ID | Potensi masalah | Atribut | Dampak ke pengguna/bisnis | Prob. | Dampak |
|---|---|---|---|---|---|
| R-04 | Rahasia & konfigurasi ter-commit; aturan keamanan tidak terlihat | Security | Kuota API disalahgunakan; bila *rules* Firestore longgar, data pengguna dapat dibaca/diubah pihak lain | 5 | 4 |
| R-03 | Reset password memberi tahu "sukses" walau gagal | Reliability | Pengguna terkunci dari akunnya dan tidak tahu penyebabnya → keluhan & churn | 4 | 4 |
| R-02 | Fitur hapus review tidak berfungsi | Functional suitability | Pengguna tidak dapat menghapus kontennya sendiri (isu privasi/kontrol data) | 5 | 3 |
| R-06 | Otorisasi hapus hanya di UI | Security | Penghapusan/perubahan data milik orang lain jika API dipanggil langsung | 3 | 5 |
| R-01 | Review ganda/tanpa batas panjang | Functional suitability | Spam, manipulasi rating, biaya penyimpanan | 4 | 3 |
| R-05 | Pencarian tidak meng-*encode* karakter khusus | Functional suitability | Hasil salah/terpotong | 3 | 3 |

Daftar lengkap 10 risiko dengan skor ada di `03_Requirement_Risk_Register.md`.

## 4. Perbedaan aktivitas QA dan QC pada proyek ini

| | **Quality Assurance (QA)** — mencegah cacat, berorientasi proses | **Quality Control (QC)** — mendeteksi cacat, berorientasi produk |
|---|---|---|
| Tujuan | Memastikan proses pengembangan menghasilkan produk bermutu | Memastikan produk yang dibangun memenuhi kebutuhan |
| Contoh pada Filmory | Meninjau & memperbaiki requirement (P03); analisis risiko; menetapkan *quality gate* (P02/P04); usulan `.gitignore` untuk `.env`, kebijakan code review & Firestore rules | Menjalankan 21 test case (P05/P06); menjalankan `flutter test`; mencatat defect D-01…D-11 |
| Waktu | Sebelum & selama pengembangan | Setelah build tersedia |
| Hasil | Proses/standar/checklist | Laporan hasil uji & defect |

## 5. Cost of Quality (≥1 kemungkinan)

| Kategori | Contoh pada Filmory | Perkiraan biaya |
|---|---|---|
| Pencegahan | Menambah `.env` ke `.gitignore`, review kode sebelum merge, menulis Firestore rules | Rendah (±1–2 jam) |
| Penilaian | Eksekusi test manual (±3 hari-orang), menjalankan `flutter analyze`/`flutter test` | Sedang |
| Kegagalan internal | Memperbaiki D-01/D-02 sebelum rilis; menulis ulang test yang gagal | Sedang |
| **Kegagalan eksternal (kemungkinan utama)** | Kunci TMDB yang bocor disalahgunakan → kuota habis/diblokir sehingga seluruh katalog gagal dimuat bagi semua pengguna; reset password palsu memicu tiket bantuan & kehilangan pengguna | **Tinggi** (rotasi kunci + rilis ulang + reputasi) |

**Kesimpulan:** biaya pencegahan (mengamankan kunci, memperbaiki handler yang diabaikan) jauh lebih murah daripada biaya kegagalan eksternal sehingga perbaikan R-04, R-03 dan R-02 diprioritaskan.
