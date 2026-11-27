Position: keep

- What we decided: a graph database (ADR 0009).
- sample.db: 20,000 entities. Full register: 310M relations. 0.4 s on the sample says nothing about the full set.
- Full data, measured: the recursive query was killed after 14 min; the best SQL-side search took 3 min 20 s.
- Needed: under 10 s. The Neo4j trial did 2 to 8 s.
