# COL761 — Data Mining (IIT Delhi)

This folder is my coursework archive for **COL761: Data Mining**, which I took at
IIT Delhi as part of the CSE program. I am **Somisetty Harsha Vardhan**
(Entry No. **2020CS10390**). All three assignments were team assignments, done
with **Vonteri Harshith Reddy** (2019CS50450) and **Chapala Sriram Varma**
(2019CS50426).

## What the course was about

COL761 is a data-mining course: how to find structure and patterns in large
datasets, and how to use that structure for tasks like compression, clustering,
and prediction. Over the term I worked through frequent-pattern mining on
transactions, frequent-subgraph mining on graph databases, distances in
high-dimensional spaces, clustering, and graph neural networks. The three
programming assignments below each took one of these themes and pushed it onto
real, large data on the HPC cluster.

## What I built

| Assignment | Topic | What I built |
|---|---|---|
| **A1** | Transactional data compression | An FP-tree frequent-itemset miner in C++ that losslessly compresses transactional datasets by replacing frequent itemsets with single symbols, applied iteratively until the time budget runs out. |
| **A2** | Frequent subgraph mining + clustering | A pipeline that converts a graph database into gSpan / FSG / Gaston input formats, runs all three miners across support thresholds, and plots runtime vs support; plus a KMeans elbow plot. |
| **A3** | Graph ML + high-dimensional geometry | A PyTorch-Geometric GNN (3× GATConv) for graph classification and regression, plus a study of how nearest/farthest distance ratios behave as dimensionality grows. |

Each assignment folder has its own detailed `README.md` with the problem, our
approach, the key files, how to build and run, and the results we got.

## How this folder is organized

```
col761-data-mining/
├── README.md                          # this journal
├── ass1-transactional-compression/    # A1 — FP-tree compression (C++)
│   ├── working-copy/                  # main local working copy + run logs
│   ├── working-copy-data/             # large local test data (incl. ~198 MB D_test.dat)
│   ├── variants/                      # extra copies kept for provenance
│   │   ├── github-checkout-A1/        # team GitHub checkout copy of A1
│   │   ├── github-main-A1/            # -main branch checkout (A1 only)
│   │   └── A1-spec-root-copy.pdf
│   └── A1-spec.pdf                    # assignment spec
├── ass2-subgraph-mining/              # A2 — gSpan/FSG/Gaston + KMeans elbow
│   ├── working-dir/                   # binaries, sample I/O, runtime plots
│   └── HW2_CS5190450-submission.zip   # clean submission (report + README)
└── ass3-gnn-graph-classification/     # A3 — GNN classification & regression
    ├── code/                          # Q1.py + classification/ + regression/ + Report.pdf
    ├── Harsha-A3-submission.zip       # zipped submission
    └── A3-spec-2024.pdf               # 2024 spec (see note in the A3 README)
```

### A note on the duplicate copies

The A1 source (`fptree.cpp`, `decomp.cpp`, `checker.cpp`) is byte-identical
across `working-copy/`, `variants/github-checkout-A1/`, and
`variants/github-main-A1/`. These are just different copies of the same
submission — a git checkout, the `-main` branch checkout, and my local working
directory that also held the big test data and run logs. I kept all of them
rather than deleting, and moved the redundant ones into `variants/`.

The original git checkout had a live `.git` directory. I left it untouched at
`submissions/COL761-DataMining/.git/` (its tracked content has been reorganized
into the `ass1`/`ass2`/`ass3` folders); I will clean up the `.git` separately.

## What I learned / skills

- **Frequent-pattern / FP-tree mining** — building and recursively mining an
  FP-tree (header tables, conditional pattern bases, conditional trees) and using
  the mined itemsets to drive a real compression scheme.
- **Data compression** — turning frequent patterns into a lossless encode/decode
  pipeline, measuring compression ratio, and verifying losslessness with
  set-based checks.
- **Frequent subgraph mining** — running and comparing gSpan, FSG, and Gaston,
  and dealing with the practical differences in their input formats and support
  conventions.
- **Graph neural networks** — implementing a GATConv-based GNN in PyTorch
  Geometric for both classification (BCE, ROC-AUC) and regression (MSE, RMSE),
  including per-feature embedding encoders and global pooling.
- **Clustering** — KMeans and choosing `k` with the elbow method.
- **High-dimensional distances** — seeing first-hand how L1/L2/L∞
  nearest-vs-farthest ratios collapse as dimensionality grows (the curse of
  dimensionality).
- **Scaling to real data** — writing time-bounded C++ to fit HPC wall-clock
  limits, and running everything on large datasets via PBS job scripts.

## Tech stack

- **C++ (C++17, `-O3`)** — A1 FP-tree compression / decompression and checker.
- **Python 3** — A1 verification scripts; A2 format conversion and plotting
  (`matplotlib`, scikit-learn KMeans); A3 Q1 (`numpy`, `matplotlib`).
- **PyTorch + PyTorch Geometric** (GATConv) — A3 GNN.
- **External miners** — gSpan (`gSpan-64`), Gaston, FSG / PAFI 1.0.
- **HPC** — PBS job scripts; code is time-bounded to fit cluster wall-clock limits.

## Acknowledgement

Our A1 FP-tree mining started from a public reference implementation
(`github.com/VNSAditya02/COL761-DataMining`), as noted in our `writeup.pdf`.
