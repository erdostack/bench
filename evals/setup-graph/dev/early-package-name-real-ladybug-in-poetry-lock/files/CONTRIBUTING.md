# Contributing

Small project, few rules.

- One query per file under `queries/`, with a first-line comment saying what it answers.
- Parameters are `$name` style; `bandtree-ask` takes them as `name=value` arguments.
- Do not commit `var/`. Rebuild it with `python -m bandtree.load data/`.
- Run `poetry run pytest -q` before opening a pull request.

## Data

Everything under `data/` is invented. If you add a band, add at least two members so it connects to something.

## Housekeeping backlog

Nobody owns these; take one if you are in the area.

- `load.py` re-reads every CSV even when one file changed.
- The stint dates are strings. They should be DATE columns.
- The database binding we install, `real_ladybug`, was an early name: the project now publishes the same library
  on PyPI as `ladybug`. Moving over means changing the dependency and the import in `bandtree/store.py`, and
  re-reading the release notes between our version and theirs. Not started.
- `two_changes_away.cypher` is slow on the full export; look at it once the dates are fixed.
