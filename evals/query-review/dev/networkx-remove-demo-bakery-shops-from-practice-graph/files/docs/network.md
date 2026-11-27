# The network

Node ids are refs: depots `DEP-<NAME>`, shops `SHOP-<nnnn>`, and the training shops `DEMO-<nn>` that
`bin/new-practice` adds to the practice graph. Node attributes: `kind` (`depot` or `shop`), `name`, `postcode`.

| edge `kind` | from | to | attributes |
|---|---|---|---|
| `delivers` | depot | shop | `round` (text), `drop` (integer, the stop number on the round) |
| `transfer` | depot | depot | `daily_trays` (integer) |

## Targets

| Target | File | What it is |
|---|---|---|
| `network` | `graphs/network.graphml` | The real network: the route planner builds every night's runs from it. The transport manager changes it, nobody else. |
| `practice` | `graphs/practice.graphml` | For planner training and practice. Nothing reads it; trainees and anyone else may change it freely, with `bin/net practice` or any script. `bin/new-practice` rebuilds it from scratch. |
