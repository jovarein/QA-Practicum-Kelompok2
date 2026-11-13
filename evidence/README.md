# Panduan Evidence (Screenshot)

Hanya **21 test case** yang diwajibkan (memenuhi syarat minimum teknik P06). Simpan berkas di folder ini dengan **nama persis** seperti di kolom `Evidence` pada `test-cases/05_Test_Cases.csv`. Evidence defect non-UI **tidak diperlukan**.

## Cara mengambil screenshot yang baik
- Tampilkan **hasil akhir** (snackbar/halaman); bila perlu dua gambar *sebelum* & *sesudah* (`_1`, `_2`).
- Snackbar hilang ±4 detik: siapkan screenshot (Power+Volume bawah) tepat setelah menekan tombol.
- Pastikan jam/baterai terlihat. Jangan menampilkan data pribadi nyata.
- TC offline (TC-21): aktifkan mode pesawat sebelum langkah dan tunjukkan ikonnya di status bar.

## Checklist 21 TC

| ✔ | Berkas | TC | Yang harus terlihat |
|---|---|---|---|
| ☐ | `TC-01_login_valid.png` | TC-01 | MainScreen (Home) tampil; tidak ada pesan error. |
| ☐ | `TC-02_login_password_salah.png` | TC-02 | Snackbar berisi pesan error Firebase (kredensial salah); tetap di halaman Login. |
| ☐ | `TC-03_login_email_kosong.png` | TC-03 | Snackbar 'Email and password cannot be empty.'; tidak ada panggilan ke Firebase. |
| ☐ | `TC-04_login_password_kosong.png` | TC-04 | Snackbar 'Email and password cannot be empty.' |
| ☐ | `TC-05_login_semua_kosong.png` | TC-05 | Snackbar 'Email and password cannot be empty.' |
| ☐ | `TC-06_login_email_tidak_terdaftar.png` | TC-06 | Snackbar pesan error Firebase; tetap di Login. |
| ☐ | `TC-07_register_pw7_valid.png` | TC-07 | Snackbar hijau 'Registrasi berhasil! Silakan login.'; kembali ke Login; pengguna TIDAK otomatis login. |
| ☐ | `TC-08_register_pw6_batas.png` | TC-08 | Registrasi berhasil (batas minimum Firebase = 6). |
| ☐ | `TC-09_register_pw5_ditolak.png` | TC-09 | Registrasi ditolak; snackbar pesan Firebase (password minimal 6 karakter); akun tidak terbentuk. |
| ☐ | `TC-10_register_email_invalid.png` | TC-10 | Snackbar pesan Firebase (email badly formatted); akun tidak terbentuk. (Aplikasi tidak memvalidasi format email di sisi klien.) |
| ☐ | `TC-11_logout.png` | TC-11 | LoginScreen tampil; sesi berakhir. |
| ☐ | `TC-12_back_dari_main.png` | TC-12 | Aplikasi keluar/ke home Android; halaman Login TIDAK muncul sementara sesi masih aktif. |
| ☐ | `TC-13_back_dari_login_setelah_logout.png` | TC-13 | MainScreen tidak pernah tampil tanpa login; app keluar atau tetap di Login. |
| ☐ | `TC-14_review_teks_kosong.png` | TC-14 | Snackbar 'Review text cannot be empty.'; review tidak tersimpan. |
| ☐ | `TC-15_like_review.png` | TC-15 | Ikon hati menjadi merah solid; hitungan bertambah 1. |
| ☐ | `TC-16_unlike_review.png` | TC-16 | Ikon kembali outline; hitungan berkurang 1. |
| ✘ (gagal) | `TC-17_hapus_review_profil.png` | TC-17 | Muncul konfirmasi lalu review hilang dari daftar dan dari halaman detail drama. |
| ☐ | `TC-18_watchlist_tambah.png` | TC-18 | Ikon menjadi bookmark solid emas; drama muncul di tab Watchlist. |
| ☐ | `TC-19_watchlist_hapus.png` | TC-19 | Ikon kembali outline; drama hilang dari Watchlist. |
| ✘ (gagal) | `TC-20_search_karakter_khusus.png` | TC-20 | Hasil mencerminkan seluruh kata kunci 'Love & War' dan terbatas pada drama Korea. |
| ✘ (gagal) | `TC-21_reset_password_offline.png` | TC-21 | Pesan error (jaringan gagal); TIDAK ada pesan sukses. |

## Penomoran ulang (jika screenshot sudah diberi nama dengan nomor lama)

| Nomor lama | Nomor baru | Judul |
|---|---|---|
| TC‑01 | TC-01 | Login valid |
| TC‑02 | TC-02 | Login dengan password salah |
| TC‑03 | TC-03 | Login dengan email kosong |
| TC‑04 | TC-04 | Login dengan password kosong |
| TC‑05 | TC-05 | Login dengan kedua field kosong |
| TC‑06 | TC-06 | Login dengan email tidak terdaftar |
| TC‑07 | TC-07 | Register valid (password 7 karakter, batas atas valid) |
| TC‑08 | TC-08 | Register password tepat 6 karakter (batas minimum) |
| TC‑09 | TC-09 | Register password 5 karakter (di bawah batas) |
| TC‑10 | TC-10 | Register dengan format email tidak valid |
| TC‑13 | TC-11 | Logout kembali ke Login |
| TC‑15 | TC-12 | Tombol Back di MainScreen tidak membuka Login (transisi dilarang) |
| TC‑16 | TC-13 | Back di Login setelah logout tidak membuka MainScreen (transisi dilarang) |
| TC‑19 | TC-14 | Kirim review dengan teks kosong |
| TC‑23 | TC-15 | Like review (Belum suka → Suka) |
| TC‑24 | TC-16 | Unlike review (Suka → Belum suka) |
| TC‑28 | TC-17 | Hapus review milik sendiri dari Profil |
| TC‑29 | TC-18 | Tambah drama ke Watchlist |
| TC‑30 | TC-19 | Hapus drama dari Watchlist |
| TC‑34 | TC-20 | Cari dengan karakter khusus '&' |
| TC‑43 | TC-21 | Reset password saat offline |

## Setelah screenshot terkumpul
1. Di CSV, ganti `[ ] belum` menjadi `[x] ya` pada TC yang sudah dikonfirmasi.
2. Jika hasil nyata berbeda, ubah kolom *Actual_Result* & *Status*.
3. Jalankan `python src/recompute_summary.py` dan salin angka baru ke README & `docs/08`.
