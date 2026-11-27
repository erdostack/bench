# grid-graph

Network model of the distribution grid in Neo4j 5.26 (LTS), loaded nightly from the asset register
exports in `import/` (not in this repo).

| label | nodes |
|---|---|
| Substation | 1,100 |
| Feeder | 14,000 |
| Transformer | 380,000 |
| Meter | 2,100,000 |

A transformer is normally fed by one feeder but can be switched to a second one, so the export lists one or
two feeder ids for it. Each meter hangs off one transformer.

The control-room outage screen answers "how many customers are off if this transformer or this feeder
trips?" while an operator waits; during storms it is run hundreds of times an hour.
