# Data changes on prod

Nobody writes to `prod` from a shell. A data change is a file `changes/NNNN_<slug>.sql` (next free number)
that starts with two comment lines:

    -- ticket: <ticket id or a one-line reason>
    -- approved-by: <left blank until review>

It is reviewed in a PR and applied by the collections systems officer with `bin/apply prod changes/<file>.sql`.
Try it on `rehearsal` first with `bin/apply rehearsal changes/<file>.sql`.

`bin/apply` runs the file in one transaction, then runs it again, and so on until a run changes no rows,
so a file that works through its rows in chunks finishes on its own (and must be safe to apply again). The
website keeps short locks on `nodes` all day: one run of a file may change at most 500 rows.
