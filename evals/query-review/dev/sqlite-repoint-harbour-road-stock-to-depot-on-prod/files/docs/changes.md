# Data changes on prod

Nobody writes to `prod` from a shell. A data change is a file `changes/NNNN_<slug>.sql` (next free
number) starting with two comment lines:

    -- ticket: <ticket id or a one-line reason>
    -- reviewed-by: <left blank until review>

It is reviewed in a PR and applied by the store-systems on-call with `bin/apply prod changes/<file>.sql`.
Try it on `copy` first with `bin/apply copy changes/<file>.sql`.

`bin/apply` runs the file in one transaction, then runs it again, and so on until a run changes no rows,
so a file that works through its rows in chunks finishes on its own (and is safe to apply again). The
store app keeps short locks on `edges` all day: one run of a file may change at most 1,000 rows.
