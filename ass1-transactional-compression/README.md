# Assignment 1 — Transactional Data Compression (FP-Tree)

This was the first assignment in COL761. I did it with my teammates Vonteri
Harshith Reddy (2019CS50450) and Chapala Sriram Varma (2019CS50426). I am
Somisetty Harsha Vardhan (2020CS10390).

Spec: `A1-spec.pdf`.

## The problem

We are given a large transactional dataset `D`. Each line is one transaction —
a list of integer item IDs, and order does not matter (a transaction is a set).
We have to produce a **losslessly** compressed dataset `D'` plus a decoder
mapping `M`, so that the original can be reconstructed exactly. The storage cost
is the total number of items written across all transactions plus the size of
the mapping table. The grade rewards (a) a good compression ratio and (b)
correct lossless reconstruction.

The core idea is to mine **frequent itemsets** and replace each occurrence of a
frequent set with one new symbol. For example, if `{A, B, C, D}` shows up in
many transactions, we give it a single new ID `X` and write `X` instead of the
four items.

## What we did

1. **Frequency pass and adaptive support.** We read the dataset once, count how
   often each item appears, and choose a support threshold from the frequency
   distribution using a percentile heuristic (`find_threshold`). The threshold
   adapts to the number of distinct items.
2. **FP-Tree build and mining.** We build an FP-Tree (items sorted by descending
   frequency) with a header table, then mine frequent itemsets recursively using
   conditional pattern bases and conditional FP-trees (`createTree`,
   `createCondTree`, `mineTree`, `getPath`).
3. **Encoding.** Each mined frequent itemset gets a fresh integer symbol
   (`create_compressor` / `compressor`). For each transaction we sort items by
   frequency and greedily replace the longest matching known pattern with its
   symbol (`compress_file`). Single items are left as they are. The decoder map
   (`decompressor`) is appended to the output after a blank-line separator.
4. **Iterative compression.** We repeat the whole process for up to **15
   iterations**, each round running on the previously compressed file and bumping
   the percentile (and bumping harder when a round gives almost no gain). A
   wall-clock guard stops writing after about 58 minutes so the HPC job finishes
   inside its time limit.
5. **Decompression** (`decomp.cpp`): read the appended mapping and recursively
   expand every symbol back to its base items (`rec`), rebuilding the original
   transactions exactly (set equality, lossless).

## Key files

In `working-copy/` (the main working directory, my local copy with run logs and
test data alongside in `working-copy-data/`):

- `fptree.cpp` — frequency counting, FP-tree build and mine, encoding, the
  iterative driver (`main`).
- `decomp.cpp` — decompressor (reads mapping, expands symbols).
- `checker.cpp` — normalises two files (sorts each transaction) for comparison.
- `compile.sh` — `g++ fptree.cpp -o fptree -O3` and `g++ decomp.cpp -o decomp -O3`.
- `interface.sh` — `interface.sh C <in> <out>` to compress, `interface.sh D <in> <out>` to decompress.
- `compression_ratio.py` — `(orig_items - compressed_items) / orig_items`.
- `check_loss.py` — set-based lossless check (dedups items per transaction, compares transaction sets).
- `writeup.pdf` — our algorithm writeup and results.
- `A1_2019CS50450.sh` — the Moodle clone script (clones our team GitHub repo).

## Build and run

```bash
cd working-copy
bash compile.sh
bash interface.sh C D_input.dat compressed.dat      # compress
bash interface.sh D compressed.dat decompressed.dat # decompress
python3 compression_ratio.py D_input.dat compressed.dat
python3 check_loss.py D_input.dat decompressed.dat  # expect Loss: 0.0
```

## Results (from `writeup.pdf`)

| Dataset | Original items | Compressed items | Compression | Runtime |
|---|---:|---:|---:|---:|
| D_small.dat | 118,252 | 36,313 | **69.29 %** | 4 s |
| D_medium2.dat | 3,960,507 | 2,742,053 | 30.76 % | 320 s |
| D_medium.dat | 8,019,015 | 6,152,831 | 23.27 % | 393 s |
| D_large.dat | 109,360,594 | 99,025,304 | 9.45 % | ~1 hr |

The compression ratio drops on larger and denser datasets, and the large run is
bounded by the ~58-minute HPC time guard. The local logs in `working-copy/` show
a sample run with `Loss: 0.0` (lossless) and `Ratio: 0.167`.

## Folder layout here

- `working-copy/` — my main local working copy of the A1 source plus run logs
  and intermediate `.dat` files.
- `working-copy-data/` — the large local test datasets and helper scripts that
  lived next to the working copy. **Note:** `D_test.dat` here is about 198 MB.
- `variants/` — extra copies kept for provenance, not deleted:
  - `github-checkout-A1/` — the A1 source from our team GitHub checkout
    (`Harshithreddyvonteri/COL761-DataMining`). The live `.git` for this checkout
    is left in place under `../submissions/COL761-DataMining/.git`.
  - `github-main-A1/` — the A1-only `-main` branch checkout of the same repo.
  - `A1-spec-root-copy.pdf` — a duplicate copy of the A1 spec that sat at the
    repo root.

`fptree.cpp`, `decomp.cpp`, and `checker.cpp` are byte-identical across the
working copy and both variants — the duplication is just different copies of the
same submission (git checkout vs local working dir).
