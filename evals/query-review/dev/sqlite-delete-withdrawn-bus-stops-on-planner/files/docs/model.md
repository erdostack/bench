# Model

`nodes.kind` is `stop`, `route`, `school`, `student` or `vehicle`; `code` is unique across all of them
(`ST-nnnn`, `R-nnn`, `SC-nn`, `P-nnnnnn`, `V-nnn`). `edges.kind`:

| edge kind | src | dst | notes |
|---|---|---|---|
| `serves` | route | stop | `seq` is the stop's place on the route |
| `boards_at` | student | stop | the student's pick-up stop |
| `drops_at` | route | school | |
| `runs` | vehicle | route | |
| `near` | stop | stop | walking link between two stops; one row per pair, either way round |

There are no foreign keys: an edge can point at a node that has gone.

## Stop status

- `active`: in use.
- `suspended`: closed for a while (roadworks, a closed footpath). Kept with all its edges; it comes back.
- `withdrawn`: set by the annual stop review. A withdrawn stop is removed: the stop node and every edge
  that touches it, on either side (`serves` and `boards_at` point at it; a `near` link can have it at
  either end). Students are moved to their new stop before the review is signed off, so any
  `boards_at` still pointing at a withdrawn stop is stale.
