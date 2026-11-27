Still stands: yes

| | when we decided | now | agreed limit |
|---|---|---|---|
| organisations | 2,300 | 9,800 | |
| deepest group | 7 levels | 12 levels | |
| nightly rollup | about 2 min | 6 min 40 s | 20 min (30-minute window) |
| subtree query, p95 | 12 ms | 41 ms | 150 ms |
| page loads | about 40 a minute | about 90 a minute | |

The merger made everything bigger, but the call was tied to two limits agreed with ops, and both still have plenty
of room: the rollup is at a third of its 20-minute limit and the panel at under a third of 150 ms. Nothing has
crossed the line we set for revisiting the storage, so the recursive queries stay. Bram's point is growth, not a
missed limit. Nothing changed in docs/graph/DECISION.md.
