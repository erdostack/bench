# swissgraph

Pairings graph for the league's weekend congresses: players and events in `nodes`; entries and
pairings in `edges`. The Swiss pairing engine reads entries and writes pairings.

- `bin/cq <target> "<sql>"` or `bin/cq <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file.
- `scripts/make_sandbox.py`: (re)build `data/sandbox.sqlite` from scratch. Run it whenever you like.
- `docs/targets.md`: the targets. `docs/model.md`: the model.
