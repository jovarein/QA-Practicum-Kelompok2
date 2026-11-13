# -*- coding: utf-8 -*-
"""Hitung ulang ringkasan dari test-cases/05_Test_Cases.csv setelah Anda memperbarui hasil nyata.
Pemakaian:  python src/recompute_summary.py
"""
import csv, os, collections
base = os.path.join(os.path.dirname(__file__), "..", "test-cases")
rows = list(csv.DictReader(open(os.path.join(base, "05_Test_Cases.csv"), encoding="utf-8-sig")))
n = len(rows)
p = sum(r["Status"].upper().startswith("PASS") for r in rows)
f = sum(r["Status"].upper().startswith("FAIL") for r in rows)
v = sum(r["Terverifikasi_Screenshot"].lower().startswith("[x]") for r in rows)
core = [r for r in rows if r["Wajib_Evidence"] == "Ya"]
core_v = sum(r["Terverifikasi_Screenshot"].lower().startswith("[x]") for r in core)
print(f"Total TC: {n} | PASS: {p} | FAIL: {f} | Pass rate: {100*p/n:.1f}%")
print(f"TC terverifikasi screenshot: {v}/{n} | wajib-bukti: {core_v}/{len(core)}")
print("TC FAIL:", ", ".join(r["TC_ID"] for r in rows if r["Status"].upper().startswith("FAIL")) or "-")
by_req = collections.defaultdict(list)
for r in rows: by_req[r["Req_ID"]].append(r["Status"].upper().startswith("PASS"))
print("Per requirement:")
for k in sorted(by_req): print(f"  {k}: {sum(by_req[k])}/{len(by_req[k])} lulus")
print("Exit criteria E3 (>=90% lulus):", "TERPENUHI" if 100*p/n >= 90 else "TIDAK TERPENUHI")
