# Data changes on the register

Nobody writes to `register` from a shell. A data change is a file `changes/NNNN_<slug>.py` (next free
number) that opens with a docstring naming the ticket and saying what it does. It defines `run(conn)`,
which makes the change and returns the number of rows it changed. It is tried on `rehearsal`
(`bin/apply rehearsal changes/<file>.py`), reviewed in a PR, and applied to the register by the register
secretary with `bin/apply register changes/<file>.py`.

The register is a small hosted SQLite file and the inspection app's saves fail behind a long write, so a
change commits at most 100 changed rows per transaction. If an apply stops part-way, the secretary applies
the same file again, so a change carries on from where it stopped and changes nothing already done.
