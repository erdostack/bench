# Model

| Relationship | From | To | Notes |
|---|---|---|---|
| `ON` | `Station` | `Line` | a station can be on several lines |
| `NEXT` | `Station` | `Station` | consecutive stops; has `line` and `minutes` |
| `IN_ZONE` | `Station` | `Zone` | exactly one zone per station |
| `AT` | `Tap` | `Station` | the gate where the card was tapped |

Keys: `Station.code`, `Line.code`, `Zone.number`. A `Tap` has `day` (date), `at` (time of day) and
`card_kind`.
