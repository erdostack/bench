# Data changes

Nobody writes to `arbor` from a shell. A data change is a file `changes/NNNN_<slug>.sql` (next free number)
starting with two comment lines:

    -- ticket: <ticket id or a one-line reason>
    -- reviewed-by: <left blank until review>

It is tried on `scratch` with `bin/apply scratch changes/<file>.sql`, reviewed in a PR, and applied to
`arbor` by the tree data officer with `bin/apply arbor changes/<file>.sql`.

`bin/apply` runs the file in one transaction, then runs it again, and so on until a run changes no rows,
so a file that works through its rows in chunks finishes by itself and is safe to apply twice. One run may
change at most **1,000 rows** as bin/apply counts them (inserts, updates and deletes all count, in temporary
tables too): the tablets' writes wait behind it.
