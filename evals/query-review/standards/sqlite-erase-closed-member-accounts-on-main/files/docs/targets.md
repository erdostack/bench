# Targets

| Target | File | What it is |
|---|---|---|
| `main` | `data/main.db` | The live database. The app and the club newsletters read and write it all day. |
| `rehearsal` | `data/rehearsal.db` | A copy of `main` for rehearsing changes. `scripts/refresh_rehearsal.py` copies `main` over it whenever you like; nothing reads it. |

## Changing data on main

Nobody writes to `main` from a shell, however small the change. A change is a file
`changes/NNN-<what>.sql` (next free number) that starts with a comment: the ticket, what it changes and
why, and the count query to run before and after. Rehearse it with `bin/apply rehearsal changes/<file>.sql`;
it is reviewed in a pull request and the data protection officer applies it with
`bin/apply main changes/<file>.sql`.

`bin/apply` runs all the statements of the file in one transaction and commits, then runs the file again,
and again, until a run changes no rows. One run (one transaction) may change at most 5,000 rows.
