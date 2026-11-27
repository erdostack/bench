# Loading notes

2026-08-14, on a 16 GB dev VM.

Pulled a sample of `column_edges` to see how NetworkX copes before we wrote anything up.

| | |
|---|---|
| Edges in the sample | 2,000,000 |
| Load time (`add_edges_from`, integer ids, the three edge attributes kept) | 71 s |
| Process RSS after load | 1.3 GB |
| Downstream walk from a mid-depth column | 4 ms |

Did not get round to trying the full table.
