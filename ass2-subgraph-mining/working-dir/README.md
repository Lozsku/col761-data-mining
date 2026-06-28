# COL761 A2 — Frequent Subgraph Mining & Clustering (working dir)

Working directory for A2. The clean submission is the zip
`../HW2_CS5190450-submission.zip`. See the root `../../README.md` for full
context, and the A2 folder `../README.md` for the detailed write-up.

## Q1 — gSpan vs FSG vs Gaston
Compare three frequent-subgraph miners on the same graph database across minimum
supports `[5, 10, 25, 50, 95]` % and plot **runtime vs support**.

- `conv-graph.py` (refactor: `one.py`) — convert the course graph format into
  gSpan / Gaston / FSG input formats; remap non-numeric labels to integers; write
  per-tool graph counts to `*-graphs.txt`.
- `part1.py` / `mypart1.py` — time each binary per support, save `runtime*.png`
  (Gaston gets absolute support = `support * num_graphs / 100`).
- `part1.sh` / `me.sh` — driver (`sh part1.sh <graph_dataset>`).
- `cmp.py` — diff two converted graph files.
- Binaries: `gSpan-64`, `gaston`, `fsg` (PAFI 1.0). Sample I/O: `gspan.txt`,
  `gaston.txt`, `fsg.txt`, `*-output.txt`, `result.txt`, plots `runtime*.png`.

## Q2 — KMeans elbow plot
`part2.py` (in the HW2 zip): KMeans for `k = 1..15`, plot inertia vs `k`.
Run: `sh elbow_plot.sh <dataset> <dimension> <output.png>`.

`classify.py` / `actives.txt` are course-provided SVM-over-graph-features
evaluation helpers.
