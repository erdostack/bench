# Model

`nodes(id, kind, ref, loop, status)`

| kind | ref | notes |
|---|---|---|
| `plant` | `PL-<name>` | energy centres |
| `pipe` | `P-<loop>-<n>` | one pipe section (flow and return together) |
| `substation` | `SS-<loop>-<n>` | the heat exchanger in a building |
| `building` | `B-<loop>-<n>` | |
| `meter` | `HM-<loop>-<n>` | heat meter on a substation |

`loop` is the network loop a node belongs to: `CEN` (Central), `HAR` (Harbourside), `NG` (Northgate).

`edges(id, src, dst, rel)`

- `feeds`: plant to pipe, pipe to pipe, pipe to substation, in the direction of flow. The Central-Northgate
  interconnect is a `feeds` edge from a CEN pipe to the first NG pipe.
- `serves`: substation to building.
- `measures`: meter to substation.
