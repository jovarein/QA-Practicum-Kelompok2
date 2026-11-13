# P03 — Requirement Review & Risk Analysis

> Repositori tidak memiliki dokumen kebutuhan (SRS). Requirement **asli** di bawah ini *disimpulkan dari perilaku kode*; kolom **Diperbaiki** adalah versi yang spesifik, terukur, dan dapat diuji.

## 1. Dokumentasi & perbaikan requirement (9 butir dalam ruang lingkup)

| ID | Fitur | Requirement asli (disimpulkan) | Masalah pada requirement asli | Requirement diperbaiki (testable) | Prioritas |
|---|---|---|---|---|---|
| REQ-01 | Registrasi akun | Pengguna bisa mendaftar dengan username, email, password. | Tidak menyebut batas password, validasi email, perilaku setelah daftar | Sistem WAJIB membuat akun baru jika username terisi, email berformat valid & belum terdaftar, dan password minimal 6 karakter; setelah sukses menampilkan 'Registrasi berhasil! Silakan login.' lalu kembali ke halaman Login tanpa login otomatis. | Must |
| REQ-02 | Login email/password | Pengguna bisa login. | Tidak menyebut pesan/kondisi gagal | Sistem WAJIB mengautentikasi email+password yang valid dan membuka MainScreen; jika salah satu field kosong tampil 'Email and password cannot be empty.'; jika kredensial salah tampil pesan error dari Firebase dan pengguna tetap di halaman Login. | Must |
| REQ-03 | Sesi & logout | Sesi login tersimpan. | Tidak menyebut sesi & perilaku tombol Back | Sistem WAJIB mempertahankan sesi setelah aplikasi ditutup & dibuka ulang (langsung ke MainScreen) dan mengembalikan pengguna ke Login saat logout; tombol Back tidak boleh membuka halaman terproteksi tanpa sesi. | Must |
| REQ-04 | Pencarian drama | Pengguna bisa mencari drama. | Tidak menyebut karakter khusus, input kosong, hasil kosong | Sistem WAJIB menampilkan hasil pencarian dari TMDB maksimal 500 ms setelah pengguna berhenti mengetik; input kosong/spasi menampilkan tampilan awal; tanpa hasil menampilkan 'Tidak ditemukan drama untuk "<kata kunci>"'; karakter khusus (&, #, %) HARUS diperlakukan sebagai bagian kata kunci. | Must |
| REQ-05 | Tulis review | Pengguna bisa menulis review dan rating. | Ambigu: rentang rating, validasi teks, duplikasi tidak disebut | Sistem WAJIB menyimpan review milik pengguna login dengan rating 0.5–5.0 (langkah 0.5) dan teks tidak kosong; teks kosong/spasi ditolak dengan 'Review text cannot be empty.'; sukses menampilkan 'Review posted successfully!'; setiap pengguna HANYA boleh punya satu review per drama. | Must |
| REQ-06 | Like review | Pengguna bisa menyukai review. | Tidak menyebut sifat toggle | Sistem WAJIB menjadikan like sebagai toggle: tap pertama menambah userId ke likedBy (ikon merah, hitungan +1), tap kedua menghapusnya (hitungan -1). | Should |
| REQ-07 | Watchlist | Pengguna bisa menyimpan drama. | Tidak menyebut status/ikon & sinkronisasi | Sistem WAJIB menyediakan toggle watchlist: Belum disimpan → Tersimpan (ikon bookmark solid emas) → Belum disimpan, dan daftar di tab Watchlist Profil harus sinkron. | Should |
| REQ-08 | Reset password | Pengguna bisa reset password. | Tidak menyebut kondisi gagal | Sistem WAJIB mengirim email reset ke alamat akun dan menampilkan pesan sukses HANYA bila pengiriman benar-benar berhasil; bila gagal (mis. offline) tampil pesan error. | Must |
| REQ-09 | Hapus review sendiri | Ada tombol hapus di daftar review profil. | Hanya ikon; perilaku tidak terdefinisi | Sistem WAJIB menghapus review milik pengguna (beserta komentar-nya) saat tombol hapus di tab Reviews Profil ditekan, dengan konfirmasi, dan daftar langsung ter-update. | Should |

> Requirement di luar 21 test case (komentar review, forum, ubah username, penanganan offline, jelajah/detail drama) tidak diuji pada praktikum ini; dicatat di *blind spot* P08.


## 2. Acceptance Criteria (Given-When-Then, 10 butir)

| ID | Req | Judul | **Given** | **When** | **Then** | TC terkait |
|---|---|---|---|---|---|---|
| AC-01 | REQ-02 | Login valid | pengguna terdaftar berada di halaman Login dengan koneksi aktif | ia mengisi email & password benar lalu menekan Login | MainScreen (Home) tampil | TC-01 |
| AC-02 | REQ-02 | Field login kosong | pengguna di halaman Login | ia menekan Login dengan email atau password kosong | snackbar 'Email and password cannot be empty.' muncul dan tidak ada pemanggilan Firebase | TC-03, TC-04, TC-05 |
| AC-03 | REQ-01 | Batas password registrasi | pengguna di halaman Register dengan data lain valid | ia memakai password 6 karakter (dan 5 karakter) | 6 karakter diterima; 5 karakter ditolak dengan pesan password terlalu lemah | TC-08, TC-09 |
| AC-04 | REQ-05 | Review tidak valid | pengguna membuka form review | ia mengirim teks kosong | snackbar 'Review text cannot be empty.' dan tidak ada data tersimpan | TC-14 |
| AC-05 | REQ-06 | Like toggle | review belum disukai pengguna | ia menekan ikon hati dua kali berturut-turut | tap-1: hati merah & hitungan +1; tap-2: hati outline & hitungan -1 | TC-15, TC-16 |
| AC-06 | REQ-07 | Watchlist toggle | drama belum ada di watchlist | pengguna menekan ikon bookmark lalu menekannya lagi | tap-1: bookmark solid & muncul di tab Watchlist; tap-2: outline & hilang dari tab Watchlist | TC-18, TC-19 |
| AC-07 | REQ-03 | Perlindungan sesi | pengguna sudah login/logout | ia logout lalu menekan Back | MainScreen tidak tampil tanpa login; Back di Main tidak membuka Login | TC-11, TC-12, TC-13 |
| AC-08 | REQ-08 | Reset password jujur | pengguna di Settings tanpa koneksi internet | ia menekan Send Link | pesan error tampil dan TIDAK ada pesan sukses | TC-21 |
| AC-09 | REQ-09 | Hapus review | pengguna memiliki review di tab Reviews Profil | ia menekan ikon hapus dan mengonfirmasi | review hilang dari daftar profil dan detail drama | TC-17 |
| AC-10 | REQ-04 | Pencarian karakter khusus | pengguna di tab Search | ia mengetik 'Love & War' | pencarian memakai seluruh teks tersebut | TC-20 |

## 3. Risk Register (skala 1–5; Skor = Likelihood × Impact; High ≥15, Medium 8–14, Low <8)

| ID | Risiko kualitas | Atribut | L | I | Skor | Level | Mitigasi yang disarankan | TC pengujian |
|---|---|---|---|---|---|---|---|---|
| R-04 | Rahasia/konfigurasi ikut ter-commit (.env berisi TMDB key, google-services.json, firebase_options.dart) dan tidak ada firestore.rules di repo | Security | 5 | 4 | **20** | High | Cabut & rotasi key, .gitignore, Firestore/Storage rules, App Check wajib | TC-01, TC-02, TC-03, TC-04, TC-05, TC-06, TC-07, TC-08, TC-09, TC-10, TC-11, TC-12, TC-13 |
| R-03 | Reset password menampilkan 'sukses' walau pengiriman gagal (nilai kembalian error diabaikan) | Reliability | 4 | 4 | **16** | High | Periksa String? hasil resetPassword dan tampilkan error | TC-21 |
| R-02 | Tombol hapus review di Profil tidak melakukan apa pun (handler kosong) | Functional suitability | 5 | 3 | **15** | High | Implementasikan deleteReview + dialog konfirmasi | TC-17 |
| R-06 | Otorisasi hapus hanya di UI; service tidak memeriksa pemilik dan tidak ada rules di repo | Security | 3 | 5 | **15** | High | Security rules berbasis request.auth.uid == resource.data.userId | TC-15, TC-16, TC-18, TC-19 |
| R-09 | Tidak ada pengujian otomatis yang valid (widget_test.dart masih contoh counter dan pasti gagal) | Maintainability | 5 | 3 | **15** | High | Ganti dengan unit/widget test nyata + mock http/Firebase | tidak diuji dalam 21 TC (bukti: analisis kode) |
| R-01 | Review ganda & tanpa batas panjang teks dari satu pengguna pada drama yang sama | Functional suitability | 4 | 3 | **12** | Medium | Batasi 1 review/user/drama (docId = uid_tmdbId) + maxLength | TC-14 |
| R-05 | Kata kunci pencarian tidak di-URL-encode (&, #, %) dan parameter bahasa tidak berlaku pada /search/tv | Functional suitability | 3 | 3 | **9** | Medium | Uri.https(...,queryParameters) / Uri.encodeQueryComponent | TC-20 |
| R-07 | Data yatim & operasi tidak atomik: hapus thread tak menghapus posts, deleteReview tak di-await, updateUsername memindai seluruh koleksi & batch >500 | Reliability / Performance | 3 | 3 | **9** | Medium | Cloud Function recursive delete, await, query collectionGroup, chunk batch | tidak diuji dalam 21 TC (bukti: analisis kode) |
| R-08 | Ketergantungan pada TMDB & placeholder pihak ketiga (via.placeholder.com) + pesan error mentah tampil ke pengguna | Reliability / Usability | 3 | 3 | **9** | Medium | Error state ramah + retry, placeholder aset lokal | tidak diuji dalam 21 TC (bukti: analisis kode) |
| R-10 | Token FCM tidak pernah disimpan (saveUserToken/removeUserToken tidak dipanggil) | Functional suitability | 4 | 2 | **8** | Medium | Panggil saat login/logout | tidak diuji dalam 21 TC (bukti: analisis kode) |

## 4. Tiga risiko prioritas, alasan, dan *residual risk*

Urutan prioritas memakai skor tertinggi; bila skor sama, dampak (Impact) lebih tinggi didahulukan.

| Prioritas | Risiko | Skor | Alasan prioritas | Tindakan mitigasi | *Residual risk* (setelah mitigasi) |
|---|---|---|---|---|---|
| 1 | **R-04** Rahasia/konfigurasi ter-commit, tidak ada rules | 20 (L5×I4) | Kondisi sudah terjadi (probabilitas maksimum); kuncinya publik pada riwayat git; kerentanan berdampak ke seluruh pengguna & kuota layanan | Rotasi key TMDB, `.env` ke `.gitignore`, bersihkan riwayat, restriksi API key Firebase, tulis Firestore/Storage rules, aktifkan App Check | **L1×I4 = 4 (Low)** — sisa risiko: key lama mungkin sudah tersalin pihak lain; rules harus diuji terus (emulator) |
| 2 | **R-03** Reset password sukses palsu | 16 (L4×I4) | Terkait langsung kehilangan akses akun; mudah terpicu (jaringan buruk umum di seluler); gagal diam-diam | Gunakan nilai kembalian `String?` dan tampilkan error; uji TC-21 di CI | **L1×I3 = 3 (Low)** — sisa risiko: email masuk spam/penundaan penyedia email |
| 3 | **R-06** Otorisasi hanya di UI | 15 (L3×I5) | Dampak tertinggi (kehilangan/penyalahgunaan data pengguna lain); skor sama dengan R-02/R-09 tetapi impact 5 | Rules `request.auth.uid == resource.data.userId` untuk update/delete; uji dengan Firebase Emulator | **L1×I4 = 4 (Low)** — sisa risiko: kesalahan konfigurasi rules di masa depan |

Risiko **R-02** (hapus review tidak berfungsi, skor 15) dan **R-09** (tidak ada test valid, skor 15) menjadi *watchlist* berikutnya; keduanya murah diperbaiki (lihat `07_Defect_Report_RCA.md`).
