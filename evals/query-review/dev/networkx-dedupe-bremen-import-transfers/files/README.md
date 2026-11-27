# corran-provenance

Provenance graph of the Corran Museum's works on paper, kept as a NetworkX MultiDiGraph in
`data/provenance.json` (node-link JSON). Nodes are parties (collectors, dealers, auction houses);
each edge is one transfer of one object from one party to another. Load and save it only through
`scripts/graphio.py`. Model notes in `docs/model.md`.
