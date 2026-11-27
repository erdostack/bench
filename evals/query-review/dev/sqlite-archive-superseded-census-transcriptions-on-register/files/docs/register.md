# The register

`register` (`data/register.sqlite`) is the only database. The volunteer site writes transcriptions into it,
members' search reads it, and the record office's quarterly export is taken from it.

There is no test or staging copy. The record office licenses the 1921 and 1939 material to the society for
one database, so we do not keep a second one anywhere. To check a change before review, run its `SELECT`
counts and `EXPLAIN QUERY PLAN` on `register` (they change nothing) and write down the numbers you expect.

## Changing the register

A change is a file `changes/NNN-<what>.py` (next free number) whose docstring says what it does, why, and
the counts it should change. After review in a PR the archive lead applies it with
`bin/apply register changes/<file>.py` on a Sunday evening. Nobody else writes to `register`.

A change file defines `run(conn)` and returns the number of relations it changed. The volunteer site's
saves wait for any open write, so a change commits at most 2,000 changed rows per transaction; a row
copied to `relation_archive` and deleted from `relation` counts as two. If an apply is stopped, the archive
lead runs it again, so a change must pick up where it left off.

Archiving a relation means copying its row unchanged into `relation_archive` and deleting it from
`relation` in the same transaction. The archive is kept for the record office and is never searched.
