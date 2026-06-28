# module load compiler/python/3.6.0/ucs4/gnu/447
# module load pythonpackages/3.6.0/matplotlib/3.0.2/gnu
python3 conv-graph.py $1 FSG
python3 conv-graph.py $1 GSPAN
python3 conv-graph.py $1 GASTON
python3 part1.py
