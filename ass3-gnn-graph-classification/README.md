# Assignment 3 — GNN Graph Classification & Regression

The third COL761 assignment. Done with my teammates Vonteri Harshith Reddy
(2019CS50450) and Chapala Sriram Varma (2019CS50426). I am Somisetty Harsha
Vardhan (2020CS10390).

The submitted code is in `code/` (and zipped in `Harsha-A3-submission.zip`), with
our report in `code/Report.pdf`. The code we submitted corresponds to the 2023
edition of A3.

**Note on the spec PDF.** `A3-spec-2024.pdf` is the **2024** edition of A3
(uniform points in high dimensions + k-NN indexing with KD-tree / M-tree / LSH).
The code we actually submitted (dated Nov 2023) matches the **2023** edition:
Q1 = farthest/nearest distance ratios under L1/L2/L∞, Q2 = GNN graph
classification and regression. I kept the 2024 spec here for reference, but there
is no code for that variant in this archive.

## Q1 — Curse of dimensionality (`code/Q1.py`)

We generate **1,000,000** uniform random points in `d ∈ {1, 2, 4, 8, 16, 32, 64}`
dimensions, pick 100 random queries, and for each query compute the **nearest**
and **farthest** point distance under **L1, L2, L∞** (excluding the query itself
for the nearest). We then plot the average farthest/nearest ratio vs `d`. As `d`
grows the ratio collapses toward 1 (all points become roughly equidistant); L1
grows fastest, L∞ saturates, and L2 sits between them.

Run: `bash interface1.sh`.

## Q2 — GNN graph classification & regression (`code/classification/`, `code/regression/`)

A PyTorch-Geometric pipeline shared between a classification and a regression
task:

- `encoder.py` — `NodeEncoder` / `EdgeEncoder`: a per-feature `nn.Embedding` for
  each categorical feature, summed into one vector (node feature dims
  `[119,5,12,12,10,6,6,2,2]`, edge dims `[5,6,2]`); nodes map to 16-dim, edges to
  2-dim.
- `train.py` — reads gzipped CSVs (`graph_labels`, `num_nodes`, `num_edges`,
  `edges`, `node_features`, `edge_features`) into PyG `Data` objects. The model is
  **3× GATConv** (hidden 32, edge-attr aware) with per-layer node embeddings
  concatenated (`32*3`), then **global mean pool**, then a linear head.
  - Classification: sigmoid output, **BCE loss** with class weights (the labels
    are imbalanced toward class 0), Adam (lr 0.01), best model by **ROC-AUC**.
  - Regression: linear output, **MSE loss**, Adam (lr 0.01), best model by **RMSE**.
- `evaluate.py` — load a saved model and score a dataset.

## How to run

```bash
cd code
bash interface1.sh                                   # Q1: distance-ratio plots
# Q2 — classification (C) or regression (R):
bash interface2.sh C train <model_path> <train_dir> <val_dir>
bash interface2.sh C eval  <model_path> <test_dir>
bash interface2.sh R train <model_path> <train_dir> <val_dir>
bash interface2.sh R eval  <model_path> <test_dir>
```

## Results (from `code/Report.pdf`)

| Task | Metric | GNN (best) | Baseline |
|---|---|---|---|
| Classification | Val ROC-AUC | **0.697** | Logistic Reg. 0.624 / Random 0.469 |
| Classification | Train ROC-AUC | 0.735 | Logistic Reg. 0.668 |
| Regression | Val RMSE | **0.905** | Linear Reg. 1.159 |
| Regression | Train RMSE | 0.834 | — |

The GNN beats the logistic/linear-regression baselines on both tasks. The graphs
we tended to misclassify were ones with several weakly-connected node clusters.
