# COL761 A3 — High-Dimensional Geometry & Graph ML

Submitted A3 code (2023 edition). See the root `../../README.md` for full
context, and the A3 folder `../README.md` for the detailed write-up plus a note
on the differing 2024 spec in `../A3-spec-2024.pdf`.

## Q1 — Curse of dimensionality (`Q1.py`)
1M uniform random points in `d ∈ {1,2,4,8,16,32,64}`, 100 random queries, compute
nearest/farthest distances under **L1, L2, L∞**, plot the average
farthest/nearest ratio vs `d`. Run: `bash interface1.sh`.

## Q2 — GNN graph classification & regression (`classification/`, `regression/`)
PyTorch-Geometric pipeline:
- `encoder.py` — per-feature embeddings (nodes → 16-d, edges → 2-d).
- `train.py` — reads gzipped CSV graph data into PyG `Data`; **3× GATConv**
  (hidden 32, edge-aware), concat per-layer node embeddings, global mean pool,
  linear head. Classification: BCE + class weights, best by ROC-AUC.
  Regression: MSE, best by RMSE. Adam, lr 0.01.
- `evaluate.py` — load saved model and score a dataset.

Run via `interface2.sh`:
```bash
bash interface2.sh C train <model> <train_dir> <val_dir>
bash interface2.sh C eval  <model> <test_dir>
bash interface2.sh R train <model> <train_dir> <val_dir>
bash interface2.sh R eval  <model> <test_dir>
```

## Reported results (`Report.pdf`)
- Classification: Val ROC-AUC **0.697** (beats LogReg 0.624, Random 0.469).
- Regression: Val RMSE **0.905** (beats Linear Reg. 1.159).
