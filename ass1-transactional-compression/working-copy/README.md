# COL761 A1 — Transactional Data Compression (FP-Tree)

Lossless compression of integer transactional datasets via frequent-itemset
mining. See the root `../../README.md` for full context and results, and the
A1 folder `../README.md` for the detailed write-up.

## Idea
Mine frequent itemsets with an **FP-Tree**, assign each one a fresh symbol, and
replace its occurrences in transactions. Repeat for up to 15 iterations on the
previously compressed file (with a ~58-minute wall-clock guard). Decompression
expands every symbol recursively back to base items — lossless on set equality.

## Files
- `fptree.cpp` — frequency counting, FP-tree build/mine (`createTree`,
  `createCondTree`, `mineTree`), encoding (`compress_file`), iterative driver.
- `decomp.cpp` — reads the appended decoder map and expands symbols.
- `checker.cpp` — normalises (sorts) transactions for comparison.
- `compile.sh`, `interface.sh` — build and C/D entry points.
- `compression_ratio.py`, `check_loss.py` — ratio and lossless verification.
- `writeup.pdf` — algorithm + results.

## Build & run
```bash
bash compile.sh
bash interface.sh C input.dat compressed.dat
bash interface.sh D compressed.dat decompressed.dat
python3 compression_ratio.py input.dat compressed.dat
python3 check_loss.py input.dat decompressed.dat   # expect Loss: 0.0
```

## Reported results
69.29 % on D_small, down to ~9.45 % on the ~109 M-item dataset (ratio decreases
with size/density; run is time-bounded on HPC).
