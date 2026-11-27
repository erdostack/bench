# Model

| label | count (2026-11) | notes |
|---|---|---|
| `Object` | 6.2 million | `objectId` (unique), `accessionNumber` (string, always starts with the four-digit year the object was accessioned, then a dot: `1987.214.3`), `accessionYear` (INTEGER; set by the importer since May 2025, so about 1.1 million objects have it), `title`, `objectType` |
| `Maker` | 410,000 | `makerId` (unique), `displayName` |
| `Place` | 96,000 | `placeId` (unique) |
| `Exhibition` | 7,800 | `exhibitionId` (unique) |

`(:Maker)-[:MADE {role}]->(:Object)`, `(:Object)-[:FROM]->(:Place)`, `(:Object)-[:SHOWN_IN]->(:Exhibition)`.
