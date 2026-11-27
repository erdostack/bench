# dispense

Dispensing service for the pharmacy chain's counters: prescriptions, stock, labels.

- Python 3.12, FastAPI, Postgres 16.
- The formulary tables (`drug`, `drug_class`, `interaction_rule`) are loaded monthly from the drug-data vendor's
  export; this service only reads them.

## Interaction check decision

Current: recursive SQL on Postgres, no graph database. Classes nest up to 5 levels.
Previous: no-graph, when classes were flat.
