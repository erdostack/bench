Added reports/unstaffed_units.sql: units open on :as_of (opened on or before it, not closed before it) with no
direct assignment covering :as_of, both ends inclusive. Staff in child units don't count. Run it with
`python -m orgunits.run reports/unstaffed_units.sql as_of=2026-06-30`.
