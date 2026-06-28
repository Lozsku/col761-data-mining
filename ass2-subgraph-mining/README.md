# Assignment 2 — Frequent Subgraph Mining & Clustering

The second COL761 assignment. Done with my teammates Vonteri Harshith Reddy
(2019CS50450) and Chapala Sriram Varma (2019CS50426). I am Somisetty Harsha
Vardhan (2020CS10390).

The clean submission is the zip `HW2_CS5190450-submission.zip` (it has the
`README.txt` and our report `CS5190450.pdf`). The folder `working-dir/` is the
unpacked and extended working directory with all the binaries, sample inputs,
outputs, and runtime plots.

## Q1 — Frequent subgraph mining: gSpan vs FSG vs Gaston

We compare three classic frequent-subgraph miners on the same graph database
across several minimum-support thresholds, and plot **runtime vs support**.

- `conv-graph.py` (refactored as `one.py`) — converts the assignment graph
  format (`#GraphId / #nodes / labels / #edges / "u v label"`) into each tool's
  input format:
  - **gSpan:** `t # N` / `v id label` / `e u v label`
  - **Gaston:** same `t # N` vertex/edge format
  - **FSG (PAFI):** `t` / `v id label` / `u u v label`
  - Non-numeric vertex labels are remapped to integers; per-tool graph counts go
    to `*-graphs.txt` (Gaston needs an absolute support count, not a fraction).
- `part1.py` / `mypart1.py` — run each binary at supports `[5, 10, 25, 50, 95]` %,
  time each run, and save `runtime*.png`. Gaston support is converted to an
  absolute count (`support * num_graphs / 100`); gSpan and FSG take a
  fraction/percent.
- `part1.sh` / `me.sh` — driver: run `conv-graph.py` for all three formats, then
  the plotting script.
- Bundled miner binaries: **`gSpan-64`**, **`gaston`**, **`fsg`** (FSG is part of
  the UMN PAFI 1.0 toolkit). Sample inputs/outputs: `gspan.txt`, `gaston.txt`,
  `fsg.txt` (and the `*file.txt` variants), `*-output.txt`, `result.txt`,
  `actives.txt`, `167.txt_graph`.
- `cmp.py` — small utility to check that two converted graph files are identical.

## Q2 — KMeans elbow plot

- `part2.py` (inside the HW2 zip) — runs `KMeans` for `k = 1..15` on a point
  dataset and plots inertia (within-cluster variation) vs `k` to find the elbow.
- `elbow_plot.sh` — `sh elbow_plot.sh <dataset> <dimension> <output.png>`.

## How to run

```bash
cd working-dir
sh part1.sh <graph_dataset>          # subgraph-mining runtime plot
# Q2 (from the HW2 zip):
sh elbow_plot.sh <points_dataset> <dimension> q3_<dim>_<RollNo>.png
```

## Results

The runtime plots are saved as `runtime1.png` / `runtime2.png` in `working-dir/`;
the detailed analysis is in `CS5190450.pdf` inside the HW2 zip. On the bundled
run, FSG reported about 64,110 input transactions (graphs), 3 distinct edge
labels, and 8 distinct vertex labels. `classify.py` and `actives.txt` are
course-provided SVM-over-graph-features evaluation helpers kept alongside the
work.
