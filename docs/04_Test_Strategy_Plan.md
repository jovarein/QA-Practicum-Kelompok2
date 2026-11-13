# P04 — Test Strategy & Test Plan

## 1. Tujuan pengujian
1. Menilai apakah fitur utama Filmory (autentikasi, review, like/komentar, watchlist, pencarian, forum, pengaturan akun) berfungsi sesuai requirement yang diperbaiki (P03).
2. Menemukan cacat pada validasi input, batas nilai, kombinasi kondisi, dan transisi state.
3. Menghasilkan bukti yang dapat ditelusuri (RTM, screenshot, log) untuk keputusan Go / Conditional Go / No-Go.

## 2. Ruang lingkup
| In scope (21 TC) | Out of scope (alasan) |
|---|---|
| Registrasi (batas password, email invalid), login email/password (decision table), logout, sesi & tombol Back | Login Google (butuh SHA-1/akun Google nyata) |
| Validasi review (teks kosong), like/unlike, hapus review dari Profil | Review valid, rating min/maks, komentar, review ganda (dibatasi 21 TC) |
| Watchlist tambah/hapus, pencarian dengan karakter khusus | Pencarian dasar, Home/detail/genre (dibatasi 21 TC) |
| Reset password saat offline | Forum, ubah username, upload foto profil, notifikasi FCM, uji beban, iOS/Web/Desktop |
| Inspeksi statis kode/konfigurasi (rahasia, test suite) sebagai temuan tambahan | Perbaikan kode (QA tidak mengubah aplikasi) |

> Ruang lingkup sengaja dipangkas menjadi 21 test case (di atas syarat minimum 12) agar sesuai beban tugas; fitur di luar itu dicatat sebagai *blind spot* di P08.

## 3. Level & tipe pengujian
| Level | Cakupan | Metode | Catatan |
|---|---|---|---|
| Unit | Fungsi validasi, `Drama.fromJson`, `TmdbService` | Belum ada → direkomendasikan (`flutter test`) | Hanya `widget_test.dart` contoh yang gagal (D-06) |
| Integrasi | UI ↔ Firebase ↔ TMDB | Manual melalui UI + Firebase Console | Utama pada praktikum ini |
| Sistem / E2E | Alur lengkap SC-01…SC-03 | Manual, 21 test case | Seluruhnya wajib-bukti |
| Penerimaan | Acceptance Criteria AC-01…AC-10 | Manual | Dipetakan di RTM |

| Tipe | Teknik |
|---|---|
| Fungsional | Equivalence Partitioning, Boundary Value Analysis, Decision Table, State Transition |
| Negatif & invalid | Input kosong, format salah, offline, duplikasi |
| Keamanan dasar | Inspeksi rahasia di VCS, tombol hapus untuk non-pemilik |
| Usabilitas dasar | Kejelasan pesan error & umpan balik |
| Regresi | Retest TC terkait setiap defect setelah perbaikan |

## 4. Lingkungan, versi, data, dan peran
| Item | Nilai |
|---|---|
| Aplikasi | Filmory `1.0.0+1`, commit `84190e0` |
| Platform uji | Android (perangkat fisik/emulator) — **isi:** model & versi Android `[ISI]` |
| Toolchain | Flutter SDK (kompatibel Dart `^3.9.2`) — **isi:** `flutter --version` `[ISI]` |
| Layanan eksternal | Firebase (project `drama-review-app` sesuai konfigurasi di repo), TMDB API v3 |
| Jaringan | Wi-Fi stabil; mode pesawat untuk TC offline (TC-21) |
| Data uji | Akun dummy `qa.user1@example.com`, serta akun registrasi BVA (`qa.bva5/6/7@example.com`); kata sandi `QaTest#123`; teks uji berawalan "(QA TC-xx)". **Tidak ada data pribadi nyata.** |
| Email reset password | Gunakan satu email dummy yang benar-benar dapat menerima surat |
| Catatan etika/risiko | Konfigurasi Firebase di repo mengarah ke project milik pemilik aplikasi; gunakan hanya data dummy & hapus data uji seusai praktikum. Bila memungkinkan, ganti `firebase_options.dart` ke project Firebase sendiri. |

| Peran | Tanggung jawab |
|---|---|
| QA Lead | Rencana, triage, keputusan akhir (P04, P08) |
| Test Designer | Skenario, test case, RTM (P03, P05, P06) |
| Test Executor | Eksekusi, screenshot, pencatatan hasil |
| Defect Analyst | Laporan defect & RCA (P07) |

## 5. Entry criteria
- Kode terkloning pada commit `84190e0` dan build debug berjalan di perangkat uji.
- Akun dummy & koneksi TMDB/Firebase tervalidasi (login berhasil, Home memuat).
- Test case & data uji disetujui (P05).
- Folder `evidence/` siap.

## 6. Exit criteria
| # | Kriteria | Target |
|---|---|---|
| E1 | TC prioritas High dieksekusi | 100% |
| E2 | Seluruh TC dieksekusi | ≥ 95% |
| E3 | Persentase lulus | ≥ 90% |
| E4 | Defect Critical terbuka | 0 |
| E5 | Defect Major terbuka tanpa *workaround* | 0 |
| E6 | Requirement *Must* tercakup RTM | 100% |
| E7 | Setiap TC memiliki *evidence* | 100% pada TC wajib-bukti |

## 7. Quality gate
Mengacu `02_QA_Lifecycle.md`: **G1 (Entry)** sebelum eksekusi, **G2 (Exit/Rilis)** memakai E1–E7. Hasil penilaian ada di `08_QA_Audit_Final_Report.md`.

## 8. Strategi prioritas eksekusi
Urutan berdasarkan risiko (P03): (1) R-04 keamanan & akses sesi → TC-11, TC-12, TC-13; (2) R-03/R-02 → TC-17, TC-21; (3) alur utama bernilai bisnis → TC-01…10, TC-14, TC-15, TC-16, TC-18, TC-19, TC-20.
TC dalam rencana (seluruhnya wajib-bukti, 21): TC-01, TC-02, TC-03, TC-04, TC-05, TC-06, TC-07, TC-08, TC-09, TC-10, TC-11, TC-12, TC-13, TC-14, TC-15, TC-16, TC-17, TC-18, TC-19, TC-20, TC-21.

## 9. Jadwal (1 minggu)
| Hari | Aktivitas | Artefak |
|---|---|---|
| 1 | Persiapan lingkungan; P01 & P02 | `01`, `02` |
| 2 | P03 requirement & risiko; P04 rencana | `03`, `04` |
| 3 | P05 desain test case, data, oracle, RTM | `05_*.csv` |
| 4–5 | P06 eksekusi teknik black-box + pengumpulan screenshot | `06`, `evidence/` |
| 6 | P07 defect, triage, RCA, retest (bila ada perbaikan) | `07` |
| 7 | P08 audit RTM, coverage, keputusan; finalisasi README & video | `08`, `README.md` |

## 10. Risiko pengujian & mitigasi
| Risiko | Mitigasi |
|---|---|
| TMDB/Firebase gangguan/kuota | Ulangi di waktu berbeda; catat waktu & pesan error |
| Akun dummy/duplikat bentrok | Pakai email unik per TC registrasi |
| Hanya ada satu perangkat | Catat versi & model; keterbatasan dicantumkan di P08 |
| Hasil berubah setelah perbaikan kode | Perbarui kolom `Actual_Result`/`Status` pada retest; `src/recompute_summary.py` menghitung ulang ringkasan |
