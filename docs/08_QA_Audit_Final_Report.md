# P08 — Final QA Audit & Quality Decision

> **Dasar angka:** seluruh angka dihitung dari `test-cases/05_Test_Cases.csv` yang hasilnya telah dikonfirmasi penguji. Jika ada perbaikan/retest, jalankan `python src/recompute_summary.py` dan perbarui bagian 2, 4, dan 5.

## 1. Audit konsistensi RTM

| # | Pemeriksaan | Hasil |
|---|---|---|
| 1 | Setiap TC merujuk Req_ID yang ada di daftar requirement | ✔ Lulus |
| 2 | Setiap requirement memiliki ≥1 TC (coverage requirement) | ✔ Lulus |
| 3 | Setiap TC memiliki Risk_ID valid | ✔ Lulus |
| 4 | Setiap TC memiliki file evidence terdefinisi | ✔ Lulus |
| 5 | Setiap defect aktual terhubung ke TC atau inspeksi statis | ✔ Lulus |
| 6 | ID TC unik & berurutan | ✔ Lulus |

**Temuan audit:**
- Seluruh 9 requirement tercakup oleh ≥1 TC. Requirement dengan TC tunggal (cakupan tipis): REQ-04 (Pencarian drama), REQ-05 (Tulis review), REQ-08 (Reset password), REQ-09 (Hapus review sendiri).
- Risiko tanpa TC dinamis: R-07, R-08, R-09, R-10 — R-09 dan R-10 hanya dicakup inspeksi statis (D-06, D-10); R-07 dan R-08 hanya berupa temuan analisis kode (D-08, D-09, D-11), bukan eksekusi UI.
- Ruang lingkup dipangkas menjadi 21 TC; requirement yang tidak lagi tercakup (komentar, forum, ubah username, penanganan offline, jelajah/detail) dikeluarkan dari RTM dan dicatat sebagai *blind spot*.
- Hasil eksekusi: **TC-17, TC-20, TC-21 gagal**; 18 TC lainnya lulus (seluruhnya dikonfirmasi penguji).

## 2. Ringkasan hasil & coverage

| Metrik | Nilai |
|---|---|
| Total test case / skenario | 21 / 3 |
| Lulus / Gagal | 18 / 3 (85.7% lulus) |
| TC gagal | TC-17, TC-20, TC-21 |
| TC prioritas High | 16 (gagal: TC-17, TC-21) |
| TC wajib-bukti | 21 (seluruh TC) |
| Requirement tercakup | 9/9 (100%) |
| Risiko tercakup TC dinamis | 6/10 |
| Defect | 11 (terkonfirmasi eksekusi: D-01, D-02, D-03; temuan statis: D-04…D-11). Major: D-01, D-02, D-05; Medium: D-03; sisanya Minor |

**Cakupan per teknik:** EP 8 TC • BVA 3 • Decision Table 5 • State Transition 8 • Negatif 9.

## 3. Analisis *blind spot* (yang belum/tidak teruji)

| Area | Alasan | Dampak risiko | Saran |
|---|---|---|---|
| Login Google | Butuh SHA-1 & akun Google; di luar ruang lingkup | Jalur auth kedua tak terverifikasi | Uji di build terkonfigurasi |
| Penegakan keamanan server (Firestore/Storage rules) | Rules tidak ada di repo; tidak ada TC otorisasi dalam 21 TC | **Tinggi** — R-06 | Uji dengan Firebase Emulator |
| Review valid, rating min/maks (BVA rating), komentar, review ganda (D-04) | Dikeluarkan dari 21 TC | Sedang | Tambah TC bila waktu tersedia |
| Forum (topik/balasan/hapus), ubah username, Home/detail/genre, penanganan offline di Home | Dikeluarkan dari 21 TC | Sedang | Tambah TC; temuan statis D-08, D-09, D-11 belum direproduksi |
| Unggah foto profil, izin galeri | Tidak masuk set wajib | Sedang | Tambah TC |
| Notifikasi FCM | Token tidak disimpan (D-10) | Rendah-Sedang | Uji setelah perbaikan |
| Skala data besar (`updateUsername`, D-09) | Hanya analisis statis | Sedang | Uji beban dengan data seed |
| Perangkat/OS lain, iOS, tema terang, aksesibilitas, orientasi landscape | Satu perangkat Android | Sedang | Matriks perangkat |
| Konkurensi (dua pengguna like bersamaan), race pada `commentCount` | Tidak diuji | Rendah | Uji dua perangkat |
| Ketersediaan & konten TMDB (hasil berubah dari waktu ke waktu) | Data eksternal tidak stabil | Rendah | Mock API untuk test otomatis |
| Kinerja (waktu muat Home: 3 panggilan API + genre N+1) | Tidak diukur | Sedang | Profil waktu muat |

## 4. Perbandingan dengan *exit criteria* (P04)

| # | Kriteria | Target | Hasil | Status |
|---|---|---|---|---|
| E1 | TC High dieksekusi | 100% | 100% direncanakan; 2 gagal (3 gagal dikonfirmasi penguji) | ⏳ Menunggu eksekusi |
| E2 | Seluruh TC dieksekusi | ≥95% | Menunggu eksekusi | ⏳ |
| E3 | Persentase lulus | ≥90% | **85.7%** | ✘ Tidak terpenuhi |
| E4 | Defect Critical terbuka | 0 | 0 | ✔ |
| E5 | Defect Major terbuka tanpa workaround | 0 | **3** (D-01, D-02, D-05) | ✘ Tidak terpenuhi |
| E6 | Requirement Must tercakup | 100% | 100% | ✔ |
| E7 | Evidence pada seluruh TC (21) | 100% | Menunggu screenshot | ⏳ |

## 5. Rekomendasi keputusan kualitas

### ➜ **CONDITIONAL GO** — hanya untuk demo/beta internal terbatas; **belum layak rilis publik**.

**Bukti pendukung:**
1. Alur inti (login, registrasi dengan validasi batas, sesi, review, like, komentar, watchlist, forum) memenuhi hasil yang diharapkan (18/21 TC lulus), dan validasi input utama berfungsi (TC-03…05, TC-09, TC-10, TC-14).
2. Tidak ditemukan defect Critical (tidak ada crash/hilang data yang terbukti).
3. Namun E3 dan E5 tidak terpenuhi: D-01 (hapus review mati), D-02 (reset password palsu), D-05 (rahasia ter-commit) berstatus Major.

**Kondisi yang wajib dipenuhi sebelum *Go* penuh:**
| # | Kondisi | Bukti penutupan |
|---|---|---|
| C1 | D-05: rotasi key TMDB, `.env` keluar dari VCS, Firestore/Storage rules + App Check aktif | Inspeksi repo + uji rules di emulator |
| C2 | D-02 diperbaiki dan TC-21 lulus | Retest + screenshot |
| C3 | D-01 diperbaiki dan TC-17 lulus | Retest + screenshot |
| C4 | Eksekusi ulang seluruh TC wajib-bukti, lulus ≥ 90% | CSV terbarui + `evidence/` lengkap |
| C5 | D-03 dan D-04 dijadwalkan/diperbaiki (tidak menghalangi demo) | Tiket backlog |

**Trade-off yang dipertimbangkan:**
| Opsi | Keuntungan | Kerugian/risiko |
|---|---|---|
| Go penuh sekarang | Cepat dirilis | Risiko keamanan (R-04, R-06), kehilangan kepercayaan pengguna (R-03), fitur terlihat rusak (R-02) |
| **Conditional Go (dipilih)** | Demo/uji pengguna terbatas tetap berjalan; perbaikan Major murah (jam–hari) | Perlu disiplin: tidak boleh dipublikasikan sebelum C1–C4 selesai |
| No-Go | Paling aman | Menunda umpan balik pengguna; tidak ada defect Critical yang membenarkan penghentian total |

**Keterbatasan audit:** analisis dilakukan pada satu commit, satu perangkat Android, dan hanya 21 test case sehingga keputusan perlu ditinjau ulang bila cakupan diperluas atau defect diperbaiki.
