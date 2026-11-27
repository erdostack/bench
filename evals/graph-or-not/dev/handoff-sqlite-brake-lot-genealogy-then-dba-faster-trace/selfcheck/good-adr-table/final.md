**Still stands: yes**

| | before | now | limit (OEM contract) |
|---|---|---|---|
| forward trace on Postgres | 14 min | 6 min | 30 s |
| backward trace on Postgres | n/a | 4 min | 30 s |
| graph database trial | 1.2 s fwd, 0.9 s back | | 30 s |

Better, but still an order of magnitude past what the contract allows, so we keep the graph database. Nothing
to update in the decision record.
