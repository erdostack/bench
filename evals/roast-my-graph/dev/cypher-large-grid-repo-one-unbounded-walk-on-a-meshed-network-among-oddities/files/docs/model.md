# Model

## Labels and keys

| Label | Key | Other properties |
|---|---|---|
| `Zone` | `code` | `name`, `level` (1 region, 2 district, 3 depot area, 4 block) |
| `Asset` | `tag` | `kind` (`substation`, `transformer`, `switch`, `joint`), `installed_ms`, `rating_kva`, `legacy_ref` |
| `Meter` | `mpan` | `phase` |
| `Customer` | `id` | `name`, `priority` (true for hospitals, dialysis at home and the like) |
| `WorkOrder` | `id` | `kind`, `due_ms`, `closed_ms` |

Every asset also carries a second label for its kind: `Substation`, `Transformer`, `Switch` or `Joint`. The key
and its constraint are on `Asset`.

Times are epoch milliseconds (`*_ms`), as the asset register exports them.

`legacy_ref` is the id from the old GIS. Two export scripts still read it; it goes when they do.

## Relationships

| Relationship | From | To | Properties | Reads as |
|---|---|---|---|---|
| `WITHIN` | `Zone` | `Zone` | | the smaller zone is inside the larger one |
| `LOCATED_IN` | `Asset` | `Zone` | | always a level 4 zone |
| `CONNECTS` | `Asset` | `Asset` | `cable_id`, `normally_open`, `length_m` | a cable, stored in the direction power normally flows |
| `SUPPLIES` | `Transformer` | `Meter` | | |
| `HOLDS` | `Customer` | `Meter` | `since_ms` | |
| `ON` | `WorkOrder` | `Asset` | | |

The zone tree comes from the property department once a quarter. The sync refuses a file in which any zone is
not exactly one level below its parent, so the tree is four levels everywhere.
