# Changing data on core

A data change is a file `changes/NNNN_<what>.py` (next free number). Its docstring names the ticket and
says what it does. It defines `run(conn)`, which makes the change and returns the number of rows it
changed. It is reviewed in a pull request and applied by the donor-systems on-call with
`bin/apply core changes/<file>.py`; nobody else writes to `core`. Rehearse it first with
`bin/apply rehearsal changes/<file>.py`.

The booking app times out behind long write transactions, so a change commits at most **500 changed
rows per transaction** (inserted, updated or deleted). If a run is cut off the on-call runs it again, so
a change must pick up where it left off and do nothing when there is nothing left to do.
