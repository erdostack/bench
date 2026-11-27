# Targets and data changes

| Target | What it is |
|---|---|
| `prod` | `data/prod.db`. Production: the site reads and writes it all day. |
| `scratch` | `data/scratch.db`. A copy of prod for trying things (`scripts/reset_scratch.py` rebuilds it). Nothing reads it. |

Nobody writes to `prod` from a shell. A data change is a file `changes/NNN-<what>.sql` (next free number)
starting with a comment: the ticket, what it changes and why, and the count query to run before and after.
It is tried on scratch (`bin/apply scratch changes/<file>.sql`), reviewed in a pull request, and applied by
the on-call moderator lead with `bin/apply prod changes/<file>.sql`.

`bin/apply` runs all the statements of the file in one transaction and commits, then runs the file again,
and again, until a run changes no rows. The site's writers wait at most a second for the lock, so one run
(one transaction) may change at most 1,000 rows: write each statement so that it changes a bounded number
of rows and the file finishes the job over several runs.
