# QA-Practicum-NamaKelompok

Praktikum **Quality Assurance** — evaluasi kualitas aplikasi **Filmory (Drama Review Mobile App)**.

## 1. Identitas kelompok
| Nama | NIM | Peran |
|---|---|---|
<<<<<<< HEAD
| `Silvia Hijri` | `23076053` | QA Lead |
| `Putri Hamdani` | `23076048` | Test Designer |
| `Azfa Jovaren` | `23076060` | Test Executor |
| `Alya Rafiah` | `23076058` | Defect Analyst |
=======
| `[ISI]` | `[ISI]` | QA Lead |
| `[ISI]` | `[ISI]` | Test Designer |
| `[ISI]` | `[ISI]` | Test Executor |
| `[ISI]` | `[ISI]` | Defect Analyst |
>>>>>>> 6fc8cf50c1ef912cd3845199d1d2b51c0df24cb8

Mata kuliah: `Quality Assurance` — Dosen: `Iip Permana, S.T., M.T.` — Program Studi Pendidikan Teknik Informatika, Universitas Negeri Padang.

## 2. Informasi aplikasi yang diuji
| Item | Nilai |
|---|---|
| Nama | Filmory (`drama_review_app`) — aplikasi pihak ketiga (open-source) |
| Repositori | https://github.com/jovarein/Drama-Review-MobileApp |
| Versi | `1.0.0+1`, commit `84190e0` |
| Teknologi | Flutter (Dart ^3.9.2), Riverpod, Firebase (Auth, Firestore, Storage, FCM), TMDB API |
| Platform uji | Android `[ISI model & versi]` |
| Sumber kode | Tidak disalin ke repo ini (aplikasi pihak ketiga); lihat tautan di atas |

## 3. Tujuan
Menilai kualitas Filmory secara berbasis-bukti: dari analisis kebutuhan & risiko, perancangan 21 test case dengan teknik black-box (EP, BVA, Decision Table, State Transition), eksekusi, pelaporan defect + RCA, hingga rekomendasi keputusan kualitas (Go/Conditional Go/No-Go).

## 4. Cara menjalankan / memeriksa
**Menjalankan aplikasi uji**
```bash
git clone https://github.com/jovarein/Drama-Review-MobileApp
cd Drama-Review-MobileApp
flutter pub get
flutter run            # perangkat/emulator Android
flutter test           # (untuk bukti D-06)
```
> Konfigurasi Firebase & `.env` sudah ada di repo sumber. Gunakan **hanya data dummy** (lihat `docs/04_Test_Strategy_Plan.md`) dan hapus data uji setelah praktikum.

**Memeriksa hasil praktikum**
1. Baca `docs/01` → `docs/08` berurutan.
2. Buka `test-cases/05_Test_Cases.csv` dan `05_RTM.csv`.
3. Cocokkan tiap TC dengan screenshot di `evidence/` (nama berkas = kolom *Evidence*).
4. Setelah semua screenshot dan hasil aktual terisi: `python src/recompute_summary.py`.

## 5. Struktur repositori
```
README.md
contributions.md
docs/           01_Quality_Assessment … 08_QA_Audit_Final_Report (kecuali 05)
test-cases/     05_Test_Cases.csv, 05_Test_Scenarios.csv, 05_RTM.csv
evidence/       screenshot & log (lihat evidence/README.md)
src/            recompute_summary.py (alat bantu opsional)
```

## 6. Ringkasan hasil (dikonfirmasi penguji)
| Metrik | Nilai |
|---|---|
| Test case / skenario | 21 / 3 |
| Lulus / gagal | 18 / 3 (85.7% lulus) |
| Requirement tercakup | 9/9 |
| Defect | 11 (terkonfirmasi eksekusi: D-01, D-02, D-03; temuan analisis statis: D-04…D-11). Severity: 3 Major (D-01, D-02, D-05), 1 Medium (D-03), 7 Minor |
| **Rekomendasi** | **Conditional Go** (demo/beta internal; bukan rilis publik) |

Hasil eksekusi (dikonfirmasi penguji): 18 TC lulus, TC-17, TC-20, TC-21 gagal.

Defect utama: hapus review di Profil tidak berfungsi (D-01); reset password menampilkan sukses palsu (D-02); kunci API & konfigurasi ter-commit (D-05).

## 7. Video presentasi
YouTube: `[ISI TAUTAN]`
