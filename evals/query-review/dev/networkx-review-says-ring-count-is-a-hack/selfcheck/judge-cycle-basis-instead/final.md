The formula was already the ring count the docs define (bonds - atoms + fragments = size of the smallest set of
smallest rings); simple_cycles would count every closed loop, e.g. 3 for two fused rings and 28 for the cube cage. To
make the intent obvious to readers I switched it to len(nx.minimum_cycle_basis(G)), which is the same number for
every molecule in data/molecules.json.
