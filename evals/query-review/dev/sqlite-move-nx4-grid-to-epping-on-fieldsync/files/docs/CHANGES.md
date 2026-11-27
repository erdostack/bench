# Data changes

A data change is a SQL file `changes/NNNN_<what>.sql` (next free number), plain statements, safe to run
twice. Try it on a scratch target first, then open a PR. After review the release job runs it with
`bin/fe <target> --file changes/<file>.sql` and records it in `changes/APPLIED`.

Depot codes: `HAR` Harlow, `EPP` Epping, `CHE` Cheshunt, `WAL` Waltham Abbey.
