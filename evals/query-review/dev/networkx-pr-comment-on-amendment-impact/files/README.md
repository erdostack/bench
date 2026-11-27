# clausegraph

Cross-references between the clauses of the framework agreement and its schedules, for the amendment checker.

- `data/references.json`: every cross-reference found by the parser, `{"from": "12.3", "to": "1.1(b)"}` meaning
  clause 12.3 refers to clause 1.1(b). See `docs/model.md`.
- `contracts/impact.py`: `load_references()` and `affected_by(G, clause)`.
