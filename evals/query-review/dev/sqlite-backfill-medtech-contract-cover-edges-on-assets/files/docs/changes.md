# Data changes

Nobody writes to `assets` from a shell. A data change is a file `changes/YYYYMMDD_<what>.sql` whose
first line is a comment naming the ticket (`-- MED-1234: ...`). Try it with
`bin/apply snapshot changes/<file>.sql`; after review the clinical engineering on-call applies it to
`assets` with `bin/apply assets changes/<file>.sql`.

`bin/apply` runs the whole file in one transaction, then runs it again, and so on until a run changes
no rows. So a file that does its work a chunk at a time finishes by itself, and it has to stop changing
rows once its work is done. The scheduler holds short locks on `edges`: one run of a file may change at
most 500 rows.
