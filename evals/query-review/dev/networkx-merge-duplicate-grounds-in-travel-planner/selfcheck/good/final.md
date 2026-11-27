Implemented merge_grounds with nx.contracted_nodes(G, keep, dup, self_loops=False) for each pair. Two things
from docs/travel.md: the kept record's legs must win where both have one (contracted_nodes keeps the kept
node's edge data; I checked on NetworkX 3.7), and nine duplicates have a 0.2 km "same site" leg to their
kept record, which contracted_nodes would turn into a self-loop unless self_loops=False. After the merge:
198 grounds down to 180, the self-loop count(`nx.number_of_selfloops(G)`) is 0, and the kept grounds' km values are unchanged.
