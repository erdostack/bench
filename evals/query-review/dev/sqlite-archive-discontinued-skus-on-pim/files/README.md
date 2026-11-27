# catalogue

The product catalogue graph: SKUs, categories and the edges between them, in `nodes` and `edges`.

- `bin/cat <target> "<sql>"` or `--file <file.sql>`: run SQL on a target in `config/targets.toml`.
- `bin/apply <target> data_changes/<file>.py`: apply a data change (calls its `up(conn)`).
- `data_changes/`: one file per data change, `NNN_<slug>.py`.
- `docs/`: where the catalogue lives, the model, and how SKUs are archived.
