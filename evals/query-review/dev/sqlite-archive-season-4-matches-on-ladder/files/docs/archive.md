# Archiving a season

When a season ends its matches leave `edges` (the standings and the match server only look at the
current season) and go to `edges_archive`, which has the same columns. The season history page reads
`edges_archive`.

A match is moved with its row unchanged (same `id`). Insert it into `edges_archive` and delete it from
`edges` in the same transaction, so the history page never shows a match twice or loses one.
Only `kind = 'match'` edges are archived; `plays_for` edges (player to team) are not seasonal.
