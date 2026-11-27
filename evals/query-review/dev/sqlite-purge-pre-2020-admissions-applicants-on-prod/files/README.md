# intake

Undergraduate admissions as a graph: applicants, programmes, schools and education agents in `nodes`,
and what links them in `edges`.

- `bin/adm <target> "<sql>"` or `bin/adm <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, `NNNN_<what>.py`.
- `docs/environments.md`: targets and how changes reach prod. `docs/model.md`: the model. `docs/retention.md`: how long records are kept.
