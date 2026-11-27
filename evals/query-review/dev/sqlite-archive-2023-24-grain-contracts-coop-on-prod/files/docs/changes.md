# Data changes on prod

Nobody writes to `prod` from a shell. A data change is a file `changes/NNNN_<slug>.sql` (next free
number) starting with two comment lines:

    -- ticket: <ticket id or a one-line reason>
    -- reviewed-by: <left blank until review>

It is reviewed in a PR and applied by the finance-systems on-call with `bin/apply prod changes/<file>.sql`.
Try it on `scratch` first with `bin/apply scratch changes/<file>.sql`.

`bin/apply` runs the whole file in one transaction, then runs it again, and so on until a run changes no
rows, so a file that works through its rows in chunks finishes on its own. The contract app holds short
locks on `edges` all day: one run of a file may change at most 1,000 rows (inserts, updates and deletes
all count).
