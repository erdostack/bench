"""Print node and edge counts per import batch."""
from collections import Counter

from graphio import load

G = load()
print(G.number_of_nodes(), "parties,", G.number_of_edges(), "transfers")
for batch, n in sorted(Counter(d["batch"] for _u, _v, d in G.edges(data=True)).items()):
    print(f"  {batch}: {n}")
