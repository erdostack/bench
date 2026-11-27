# basketgraph

Shopping baskets as a graph for basket-affinity work: baskets, products, stores and (pseudonymous)
customers in `nodes`, and what links them in `edges`.

- `bin/bq <target> "<sql>"` or `bin/bq <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: changes for live, `NNNN_<what>.py`.
- `analysis/`: affinity queries. `docs/`: targets, model, test data.
