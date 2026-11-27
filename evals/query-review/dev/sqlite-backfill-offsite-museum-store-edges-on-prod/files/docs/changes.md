# Changing data on prod

Nobody writes to `prod` by hand. A data change is a file `changes/NNNN_<slug>.sql` (next free number)
starting with:

    -- ticket: <ticket id or a one-line reason>
    -- reviewer: <left blank until review>

It is reviewed in a PR and applied by the collections data manager with `bin/apply prod changes/<file>.sql`.
Try it on `scratch` first.

`bin/apply` runs the whole file in one transaction, then runs it again, and so on until a run changes no
rows. So a file must stop changing rows once its work is done (it is also applied again after any failure),
and a file that works in chunks finishes on its own. The movement app holds short locks all day: one run
of a file may change at most 400 rows.
