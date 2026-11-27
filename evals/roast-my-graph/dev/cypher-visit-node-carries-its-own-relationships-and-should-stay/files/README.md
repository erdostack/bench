# pawprint

Patient records for a group of veterinary clinics. Neo4j 5.

    graph/model.md         the model in one table
    graph/schema.cypher    constraints and indexes
    graph/queries.cypher   what the practice app runs; each query has a `// name:` line

## What the app does with it

- Front desk opens an animal's record: its visits, newest first, with who saw it.
- A vet opens one visit: the notes, what was prescribed at that visit (drug, dose, days), and the earlier visit
  it is a follow-up of, if there is one. Follow-ups chain (a re-check of a re-check); the longest chain on
  record is 7 visits.
- Each vet prints a day sheet in the morning.
- A few times a year a drug is recalled and someone lists every animal that was given it since a date.

## Size

| Thing | Count |
|---|---|
| `Client` | 61,000 |
| `Animal` | 94,000 |
| `Vet` | 46 |
| `Visit` | 1.3 million, about 550 a day across the group |
| `Drug` | 1,900 |
| `PRESCRIBED` | 2.2 million |

An animal has 14 visits on average and usually sees the same two or three vets.
