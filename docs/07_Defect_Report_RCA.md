# P07 — Defect Report, Triage & Root Cause Analysis

> **Sumber defect:** semuanya **defect aktual** (bukan *seeded defect*) dari analisis kode pada commit `84190e0`. **D-01, D-02, D-03 terkonfirmasi gagal saat eksekusi** (TC-17, TC-21, TC-20). D-04…D-11 adalah **temuan analisis statis** yang tidak direproduksi karena di luar 21 TC (tanpa screenshot). QA tidak mengubah kode aplikasi, sehingga *retest* disiapkan sebagai rencana (bagian 4).

**Lingkungan umum:** Filmory 1.0.0+1 (`84190e0`), Android `[ISI model/versi]`, Flutter `[ISI versi]`, jaringan Wi-Fi (kecuali dinyatakan), akun dummy `qa.user1@example.com`.

## 1. Ringkasan & triage

| ID | Judul | Severity | Priority | Risiko | TC | Keputusan triage |
|---|---|---|---|---|---|---|
| D-01 | Tombol hapus review di tab Reviews Profil tidak berfungsi | Major | High | R-02 | TC-17 | Perbaiki sebelum rilis |
| D-02 | Reset password menampilkan pesan sukses meski pengiriman gagal | Major | High | R-03 | TC-21 | Perbaiki sebelum rilis |
| D-03 | Kata kunci pencarian dengan karakter '&' / '#' terpotong; hasil tidak sesuai | Medium | Medium | R-05 | TC-20 | Jadwalkan sprint berikut |
| D-04 | Satu pengguna dapat mengirim review berulang pada drama yang sama; tidak ada batas panjang teks | Minor | Medium | R-01 | — (analisis statis) | Jadwalkan sprint berikut |
| D-05 | Kredensial/konfigurasi ter-commit di repositori publik (.env berisi TMDB_API_KEY; google-services.json; tidak ada firestore.rules) | Major | High | R-04 | —(inspeksi statis) | Perbaiki sebelum rilis |
| D-06 | Berkas test/widget_test.dart adalah contoh counter bawaan dan gagal dijalankan | Minor | Medium | R-09 | —(eksekusi `flutter test`) | Jadwalkan sprint berikut |
| D-07 | Gambar backdrop memakai poster_path sehingga header/latar login terlihat buram & terpotong | Minor | Low | R-08 | — (analisis statis) | Backlog |
| D-08 | Hapus thread tidak menghapus sub-koleksi posts; deleteReview tidak menunggu penghapusan komentar | Minor | Medium | R-07 | — (analisis statis) | Jadwalkan sprint berikut |
| D-09 | updateUsername memindai SELURUH koleksi reviews dan seluruh subkoleksi komentar dalam satu batch | Minor | Low | R-07 | — (analisis statis) | Backlog |
| D-10 | Token FCM tidak pernah disimpan ke Firestore (kode mati) | Minor | Low | R-10 | —(inspeksi statis + Firestore Console) | Backlog |
| D-11 | Pesan error teknis (exception mentah) tampil ke pengguna | Minor | Medium | R-08 | — (analisis statis) | Jadwalkan sprint berikut |

Definisi: **Critical** = aplikasi crash/data hilang tanpa solusi; **Major** = fungsi utama salah/bahaya keamanan; **Medium** = fungsi sekunder salah dengan dampak sedang; **Minor** = fungsi sekunder/tampilan; **Priority** = urutan perbaikan bisnis (High/Medium/Low).

## 2. Laporan defect rinci

### D-01 — Tombol hapus review di tab Reviews Profil tidak berfungsi
| Field | Isi |
|---|---|
| Severity / Priority | **Major** / **High** |
| Status | Confirmed — gagal saat eksekusi (✘) |
| Komponen | Profile › _MyReviewsList |
| Lingkungan | Android `[ISI]`, Filmory 1.0.0+1 (`84190e0`) |
| Langkah reproduksi | 1) Login. 2) Buka drama & kirim review. 3) Profil › tab Reviews. 4) Tekan ikon tong sampah. |
| Hasil diharapkan | Muncul konfirmasi dan review terhapus dari daftar (REQ-09). |
| Hasil aktual | Tidak terjadi apa pun; review tetap ada. Handler onPressed hanya berisi komentar '// Delete logic'. |
| Lokasi kode | `lib/features/profile/presentation/screens/profile_screen.dart (±baris 399-404); DatabaseService.deleteReview() sudah ada tetapi tidak dipanggil` |
| TC / Risiko | TC-17 / R-02 |
| Bukti | `evidence/TC-17_hapus_review_profil.png` |
| Saran perbaikan | Panggil ref.read(databaseServiceProvider).deleteReview(review.id) di dalam AlertDialog konfirmasi. |

### D-02 — Reset password menampilkan pesan sukses meski pengiriman gagal
| Field | Isi |
|---|---|
| Severity / Priority | **Major** / **High** |
| Status | Confirmed — gagal saat eksekusi (✘) |
| Komponen | Settings › _resetPassword |
| Lingkungan | Android `[ISI]`, Filmory 1.0.0+1 (`84190e0`) |
| Langkah reproduksi | 1) Login. 2) Matikan data/Wi-Fi. 3) Profil › Settings › Security › Send Link. |
| Hasil diharapkan | Tampil pesan error karena email tidak terkirim (REQ-08). |
| Hasil aktual | Snackbar hijau 'Password reset email sent to <email>' tetap tampil. AuthService.resetPassword() mengembalikan String? error (bukan melempar), tetapi UI mengabaikan nilai kembalian sehingga blok catch tak pernah jalan. |
| Lokasi kode | `lib/features/profile/presentation/screens/settings_screen.dart (_resetPassword); lib/features/auth/services/auth_service.dart (resetPassword)` |
| TC / Risiko | TC-21 / R-03 |
| Bukti | `evidence/TC-21_reset_password_offline.png` |
| Saran perbaikan | final err = await authService.resetPassword(email); if (err != null) tampilkan error else sukses. |

### D-03 — Kata kunci pencarian dengan karakter '&' / '#' terpotong; hasil tidak sesuai
| Field | Isi |
|---|---|
| Severity / Priority | **Medium** / **Medium** |
| Status | Confirmed — gagal saat eksekusi (✘) |
| Komponen | TmdbService.searchDramas |
| Lingkungan | Android `[ISI]`, Filmory 1.0.0+1 (`84190e0`) |
| Langkah reproduksi | 1) Tab Search. 2) Ketik 'Love & War'. |
| Hasil diharapkan | Pencarian memakai seluruh teks 'Love & War'. |
| Hasil aktual | Query dirangkai manual (&query=$query) tanpa encoding sehingga '&' dianggap pemisah parameter dan hanya 'Love ' yang dikirim; parameter with_original_language tidak dikenal oleh /search/tv sehingga drama non-Korea dapat ikut muncul. (Perlu konfirmasi lewat screenshot.) |
| Lokasi kode | `lib/core/services/tmdb_service.dart › searchDramas` |
| TC / Risiko | TC-20 / R-05 |
| Bukti | `evidence/TC-20_search_karakter_khusus.png` |
| Saran perbaikan | Gunakan Uri.https('api.themoviedb.org','/3/search/tv',{'api_key':..., 'query': query, ...}) lalu filter original_language == 'ko' di sisi klien. |

### D-04 — Satu pengguna dapat mengirim review berulang pada drama yang sama; tidak ada batas panjang teks
| Field | Isi |
|---|---|
| Severity / Priority | **Minor** / **Medium** |
| Status | Open — temuan analisis statis (belum direproduksi) |
| Komponen | DatabaseService.postReview |
| Lingkungan | Android `[ISI]`, Filmory 1.0.0+1 (`84190e0`) |
| Langkah reproduksi | 1) Buka drama X. 2) Kirim review 'A'. 3) Kirim lagi review 'B' pada drama X. |
| Hasil diharapkan | Review kedua ditolak/menggantikan yang pertama (REQ-05 diperbaiki: 1 review/user/drama). |
| Hasil aktual | Dua review tersimpan (reviews.add() selalu membuat dokumen baru, tanpa pengecekan duplikasi atau maxLength). |
| Lokasi kode | `lib/core/services/database_service.dart › postReview` |
| TC / Risiko | — (analisis statis) / R-01 |
| Bukti | Tidak ada screenshot (temuan analisis statis); bukti = lokasi kode pada baris "Lokasi kode". |
| Saran perbaikan | Gunakan docId deterministik '${uid}_$tmdbId' dengan set(); tambah maxLength pada TextField. |

### D-05 — Kredensial/konfigurasi ter-commit di repositori publik (.env berisi TMDB_API_KEY; google-services.json; tidak ada firestore.rules)
| Field | Isi |
|---|---|
| Severity / Priority | **Major** / **High** |
| Status | Open — temuan analisis statis (belum direproduksi) |
| Komponen | Repository / konfigurasi |
| Lingkungan | Android `[ISI]`, Filmory 1.0.0+1 (`84190e0`) |
| Langkah reproduksi | 1) Buka repo GitHub. 2) Lihat berkas .env di root dan android/app/google-services.json. |
| Hasil diharapkan | Rahasia tidak disimpan di VCS; aturan keamanan Firestore/Storage versi-terkontrol. |
| Hasil aktual | Berkas .env (TMDB_API_KEY) terlihat publik pada commit 84190e0 dan tidak masuk .gitignore. Tidak ada firestore.rules/storage.rules di repo sehingga kontrol akses tidak dapat diaudit. (Nilai key sengaja tidak dicantumkan di laporan ini.) |
| Lokasi kode | `/.env, /.gitignore, /android/app/google-services.json, /firebase.json` |
| TC / Risiko | —(inspeksi statis) / R-04 |
| Bukti | Tidak ada screenshot (temuan analisis statis); bukti = lokasi kode pada baris "Lokasi kode". |
| Saran perbaikan | Cabut & rotasi key TMDB, tambah .env ke .gitignore, bersihkan riwayat git, restriksi API key Firebase, tambahkan rules + App Check. |

### D-06 — Berkas test/widget_test.dart adalah contoh counter bawaan dan gagal dijalankan
| Field | Isi |
|---|---|
| Severity / Priority | **Minor** / **Medium** |
| Status | Open — temuan analisis statis (belum direproduksi) |
| Komponen | Test suite |
| Lingkungan | Android `[ISI]`, Filmory 1.0.0+1 (`84190e0`) |
| Langkah reproduksi | 1) Jalankan `flutter test` di root proyek. |
| Hasil diharapkan | Test relevan (login/validasi) lolos. |
| Hasil aktual | Test mencari teks '0' & ikon tambah yang tidak ada di app Filmory; MyApp juga memerlukan dotenv & Firebase sehingga test gagal. Tidak ada test lain. |
| Lokasi kode | `test/widget_test.dart` |
| TC / Risiko | —(eksekusi `flutter test`) / R-09 |
| Bukti | Tidak ada screenshot (temuan analisis statis); bukti = lokasi kode pada baris "Lokasi kode". |
| Saran perbaikan | Hapus/ganti dengan test nyata (mis. validasi login) dengan mock. |

### D-07 — Gambar backdrop memakai poster_path sehingga header/latar login terlihat buram & terpotong
| Field | Isi |
|---|---|
| Severity / Priority | **Minor** / **Low** |
| Status | Open — temuan analisis statis (belum direproduksi) |
| Komponen | Drama.fullBackdropPath |
| Lingkungan | Android `[ISI]`, Filmory 1.0.0+1 (`84190e0`) |
| Langkah reproduksi | 1) Buka layar Login atau detail drama. 2) Amati gambar latar/header. |
| Hasil diharapkan | Header menampilkan backdrop lanskap resolusi w780. |
| Hasil aktual | Getter fullBackdropPath membangun URL dari posterPath (potret) sehingga gambar potret diperbesar. |
| Lokasi kode | `lib/core/models/drama_model.dart` |
| TC / Risiko | — (analisis statis) / R-08 |
| Bukti | Tidak ada screenshot (temuan analisis statis); bukti = lokasi kode pada baris "Lokasi kode". |
| Saran perbaikan | Tambah field backdrop_path pada model dan gunakan pada getter. |

### D-08 — Hapus thread tidak menghapus sub-koleksi posts; deleteReview tidak menunggu penghapusan komentar
| Field | Isi |
|---|---|
| Severity / Priority | **Minor** / **Medium** |
| Status | Open — temuan analisis statis (belum direproduksi) |
| Komponen | DatabaseService.deleteThread/deleteReview |
| Lingkungan | Android `[ISI]`, Filmory 1.0.0+1 (`84190e0`) |
| Langkah reproduksi | 1) Buat thread & balasan. 2) Hapus thread. 3) Cek Firestore Console › forum_threads/<id>/posts. |
| Hasil diharapkan | Seluruh data turunan ikut terhapus. |
| Hasil aktual | Dokumen posts tetap ada (orphan). Pada deleteReview, doc.reference.delete() dalam for-loop tanpa await. |
| Lokasi kode | `lib/core/services/database_service.dart` |
| TC / Risiko | — (analisis statis) / R-07 |
| Bukti | Tidak ada screenshot (temuan analisis statis); bukti = lokasi kode pada baris "Lokasi kode". |
| Saran perbaikan | Gunakan batch/Cloud Function recursive delete dan await. |

### D-09 — updateUsername memindai SELURUH koleksi reviews dan seluruh subkoleksi komentar dalam satu batch
| Field | Isi |
|---|---|
| Severity / Priority | **Minor** / **Low** |
| Status | Open — temuan analisis statis (belum direproduksi) |
| Komponen | DatabaseService.updateUsername |
| Lingkungan | Android `[ISI]`, Filmory 1.0.0+1 (`84190e0`) |
| Langkah reproduksi | 1) Ubah username pada basis data berisi banyak review (>500 dokumen terkait). |
| Hasil diharapkan | Username berhasil diperbarui dengan biaya baca wajar. |
| Hasil aktual | Kode membaca semua dokumen reviews lalu semua komentar (N+1) dan memakai satu WriteBatch (batas 500 operasi) → lambat, mahal, dan dapat gagal pada data besar. (Analisis statis; tidak diuji pada data besar.) |
| Lokasi kode | `lib/core/services/database_service.dart › updateUsername` |
| TC / Risiko | — (analisis statis) / R-07 |
| Bukti | Tidak ada screenshot (temuan analisis statis); bukti = lokasi kode pada baris "Lokasi kode". |
| Saran perbaikan | Gunakan collectionGroup('comments').where('userId'==uid) dan pecah batch per 400. |

### D-10 — Token FCM tidak pernah disimpan ke Firestore (kode mati)
| Field | Isi |
|---|---|
| Severity / Priority | **Minor** / **Low** |
| Status | Open — temuan analisis statis (belum direproduksi) |
| Komponen | NotificationService/DatabaseService |
| Lingkungan | Android `[ISI]`, Filmory 1.0.0+1 (`84190e0`) |
| Langkah reproduksi | 1) Login. 2) Periksa dokumen users/<uid> di Firestore Console. |
| Hasil diharapkan | Field fcmTokens berisi token perangkat. |
| Hasil aktual | saveUserToken()/removeUserToken() tidak dipanggil dari mana pun sehingga fcmTokens tidak pernah terisi. |
| Lokasi kode | `lib/core/services/database_service.dart; lib/core/services/notification_service.dart` |
| TC / Risiko | —(inspeksi statis + Firestore Console) / R-10 |
| Bukti | Tidak ada screenshot (temuan analisis statis); bukti = lokasi kode pada baris "Lokasi kode". |
| Saran perbaikan | Panggil saveUserToken setelah login dan removeUserToken sebelum logout. |

### D-11 — Pesan error teknis (exception mentah) tampil ke pengguna
| Field | Isi |
|---|---|
| Severity / Priority | **Minor** / **Medium** |
| Status | Open — temuan analisis statis (belum direproduksi) |
| Komponen | Home/SeeAll/Detail error state |
| Lingkungan | Android `[ISI]`, Filmory 1.0.0+1 (`84190e0`) |
| Langkah reproduksi | 1) Matikan jaringan. 2) Buka aplikasi hingga Home / buka drama. |
| Hasil diharapkan | Pesan ramah + tombol coba lagi. |
| Hasil aktual | Home menampilkan 'Error: <exception>' pada tiap bagian; detail menampilkan 'Error: $err'. Tidak ada tombol retry (kecuali GenreResultsScreen). |
| Lokasi kode | `lib/features/home/presentation/screens/home_screen.dart; drama_details_screen.dart` |
| TC / Risiko | — (analisis statis) / R-08 |
| Bukti | Tidak ada screenshot (temuan analisis statis); bukti = lokasi kode pada baris "Lokasi kode". |
| Saran perbaikan | Tampilkan widget error seragam dengan tombol ref.invalidate(provider). |

## 3. Root Cause Analysis — metode 5-Why

### RCA D-01 (hapus review tidak berfungsi)
1. **Mengapa review tidak terhapus?** Karena `onPressed` tombol hapus hanya berisi komentar `// Delete logic`.
2. **Mengapa handler kosong?** Karena UI dibuat lebih dulu sebagai kerangka (*placeholder*) dan logika belum disambungkan.
3. **Mengapa tidak terdeteksi?** Karena tidak ada test UI maupun checklist yang memeriksa "setiap tombol punya aksi".
4. **Mengapa tidak ada test/checklist?** Karena satu-satunya test adalah contoh bawaan Flutter (D-06) dan tidak ada gerbang kualitas di PR.
5. **Mengapa tidak ada gerbang kualitas?** Karena proses pengembangan tidak mendefinisikan *Definition of Done* yang memuat pengujian.
**Akar masalah:** ketiadaan *Definition of Done* & gerbang kualitas. **Tindakan korektif:** isi handler dengan `deleteReview` + konfirmasi; **tindakan pencegahan:** checklist PR "tidak ada handler kosong/TODO", tambahkan widget test.

### RCA D-02 (reset password sukses palsu)
1. **Mengapa pesan sukses muncul saat gagal?** UI selalu menampilkan snackbar sukses setelah `await resetPassword(email)` selesai tanpa melempar.
2. **Mengapa tidak melempar?** `AuthService.resetPassword` menangkap `FirebaseAuthException` dan **mengembalikan** pesan `String?`, sedangkan UI memakai pola `try/catch`.
3. **Mengapa ada ketidakcocokan pola?** `loginUser`/`registerUser` memakai pola "kembalikan error"; Settings ditulis dengan pola "lempar exception" tanpa melihat kontrak fungsi.
4. **Mengapa kontrak berbeda tidak terdeteksi?** Tidak ada tinjauan kode/ tipe hasil terstruktur (mis. `Result<T>`), dan tidak ada test untuk jalur gagal.
5. **Mengapa tidak ada test jalur gagal?** Strategi pengujian hanya "jalur bahagia" secara manual.
**Akar masalah:** kontrak penanganan error tidak seragam + tidak ada pengujian jalur negatif. **Pencegahan:** satu konvensi error (mis. sealed `Result`), TC negatif wajib (TC-21) di gate G0/G2.

### RCA D-03 (query pencarian tidak di-encode)
1. **Mengapa hasil terpotong?** `&` pada kata kunci dianggap pemisah parameter URL.
2. **Mengapa?** URL dirangkai dengan interpolasi string `...&query=$query...`.
3. **Mengapa tidak memakai builder URI?** Pola cepat dari contoh/tutorial disalin ke semua endpoint.
4. **Mengapa tidak diuji dengan karakter khusus?** Tidak ada daftar data uji karakter khusus.
5. **Mengapa tidak ada?** Tidak ada requirement tertulis soal input khusus (diperbaiki di REQ-04).
**Akar masalah:** requirement & data uji tidak mencakup input khusus. **Pencegahan:** satu fungsi pembangun URL aman + EP kelas "karakter khusus" di test suite.

### RCA D-05 (rahasia ter-commit)
1. **Mengapa key TMDB terlihat publik?** `.env` ikut ter-commit.
2. **Mengapa ikut ter-commit?** `.gitignore` bawaan Flutter tidak memuat `.env`, dan `flutter_dotenv` memerlukan `.env` terdaftar sebagai aset.
3. **Mengapa tidak disadari?** Tidak ada pemindaian rahasia pra-commit.
4. **Mengapa tidak ada pemindaian?** Keamanan tidak termasuk dalam kriteria penerimaan/gate.
5. **Mengapa tidak termasuk?** Risiko keamanan belum dianalisis sejak awal (tidak ada *risk register*).
**Akar masalah:** analisis risiko keamanan tidak dilakukan di fase awal. **Pencegahan:** gate G0 "secret scan", rotasi key, *rules* + App Check.

## 4. Rencana *retest* & usulan perbaikan (patch sebagai rekomendasi)

| Defect | Usulan perubahan singkat | Retest | Regresi |
|---|---|---|---|
| D-01 | `onPressed: () async { final ok = await showDialog<bool>(...); if (ok==true) await ref.read(databaseServiceProvider).deleteReview(review.id); }` | TC-17 | TC-14 |
| D-02 | `final err = await ref.read(authServiceProvider).resetPassword(email); if (err!=null) {snackbar error} else {snackbar sukses}` | TC-21 | TC-03 |
| D-03 | `Uri.https('api.themoviedb.org','/3/search/tv',{'api_key':apiKey,'query':query,'include_adult':'false'})` + filter `original_language=='ko'` | TC-20 | — |
| D-04 | docId `'${uid}_$tmdbId'` + `set()` | Uji manual baru (di luar 21 TC) | TC-14 |
| D-05 | `.gitignore`, rotasi key, rules | Inspeksi repo | — |
| D-06 | Ganti `widget_test.dart` | `flutter test` | — |

Hasil retest akan dicatat pada tabel berikut setelah pengembang memperbaiki:

| Defect | Build setelah fix | Hasil retest | Tanggal | Penguji |
|---|---|---|---|---|
| D-01 | — | Menunggu perbaikan | — | — |
| D-02 | — | Menunggu perbaikan | — | — |
| D-03 | — | Menunggu perbaikan | — | — |
