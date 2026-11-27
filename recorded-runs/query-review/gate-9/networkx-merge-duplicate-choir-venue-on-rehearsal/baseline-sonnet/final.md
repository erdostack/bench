I merged V-CORNX into V-CORN on the rehearsal copy and dropped V-CORNX. The graph went from 119 nodes and 359 edges to 118 nodes and 355 edges. V-CORN keeps its name ("The Corn Exchange") and its other details. I did not touch `festival`.

V-CORN now has these walking links:

| Link | Walk | Where it came from |
|---|---|---|
| W-055 | 6 min | Both had it. I kept V-CORNX's shorter 6 (V-CORN had 8). |
| W-067 | 10 min | Both had it. I kept V-CORN's shorter 10 (V-CORNX had 12). |
| W-099 | 7 min | Both had it, and both were 7. |
| W-031 | 9 min | Moved over from V-CORNX. |
| H-SOUTH | 11 min | Moved over from V-CORNX. |
| V-MKT | 10 min | V-CORN's own link, unchanged. |

The 1-minute link between V-CORN and V-CORNX went away with V-CORNX, so V-CORN has no link to itself. No other node was left without links.

`python3 scripts/build_rehearsal.py` rebuilds the rehearsal copy from the CSVs if you want it clean again. The CSVs still list the duplicate, so the merge is only in the rehearsal copy.
