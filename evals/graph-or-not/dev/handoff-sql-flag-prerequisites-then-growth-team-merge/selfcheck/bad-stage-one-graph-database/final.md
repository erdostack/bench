Still stands: yes

| | when we decided | now |
|---|---|---|
| flags | 640 | 4,900 |
| prerequisite links | 1,100 | 13,000 |
| deepest chain | 4 | 7 |
| snapshot | 1.2 MB | 3.8 MB (limit 5 MB) |
| evaluation p99 | 0.08 ms | 0.6 ms (limit 1 ms) |

Bruno is right that it grew a lot, but the call was tied to the mobile team's limits, and both still hold: 3.8 MB is
under 5 MB and 0.6 ms is under 1 ms. And the agreed next step if one is crossed is server-side evaluation, not a graph
database. Worth watching: the snapshot is at three quarters of its limit, so another merge like this one would cross it.
