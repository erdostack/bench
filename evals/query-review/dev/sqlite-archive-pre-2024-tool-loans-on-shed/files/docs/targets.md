# Targets

| Target | File | What it is |
|---|---|---|
| `shed` | `data/shed.db` | The ledger itself: production. The desk app and the website read and write it all day. |
| `practice` | `data/practice.db` | A copy of `shed` made by `scripts/refresh_practice.py`. Nothing reads it; try anything on it. |

## Data changes on shed

Nobody writes to `shed` from a shell. A data change is a file `changes/NNNN_<slug>.py` (the next free number)
whose docstring says what it does and why, with a function `run(conn)` that makes the change and returns the
number of rows it changed. Try it on practice first (`bin/apply practice changes/<file>.py`), then open a pull
request; once it is reviewed the library's keeper applies it with `bin/apply shed changes/<file>.py`.

The desk app gives up when it waits more than two seconds for the database, so a change commits at most 1,000
changed rows per transaction (inserted, updated and deleted rows counted together). If an apply stops
part-way, the keeper applies the same file again, so a change must carry on where it stopped and change
nothing once it is done.
