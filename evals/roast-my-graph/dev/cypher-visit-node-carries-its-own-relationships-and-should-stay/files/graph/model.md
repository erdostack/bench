# Model

| Relationship | From | To | Properties |
|---|---|---|---|
| `OWNS` | `Client` | `Animal` | `since` |
| `HAD` | `Animal` | `Visit` | |
| `SEEN_BY` | `Visit` | `Vet` | |
| `PRESCRIBED` | `Visit` | `Drug` | `dose`, `days` |
| `FOLLOW_UP_OF` | `Visit` | `Visit` | the later visit points at the earlier one |

Node keys: `Client.id`, `Animal.id`, `Vet.id`, `Visit.id`, `Drug.code`.

`Visit` properties: `day` (date), `slot` (position on the day sheet), `reason`, `notes`, `weight_kg`.
