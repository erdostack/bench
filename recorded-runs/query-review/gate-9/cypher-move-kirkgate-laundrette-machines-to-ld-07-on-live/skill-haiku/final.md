Not run on live. The re-site is written as change file `changes/026-resite-ld-03-machines-to-ld-07.cypher` for the operations lead to review and run, the same way as changes 023 to 025.

Why: `live` is the production graph, and `docs/environment.md` says nobody runs writes on it by hand. Changes are files reviewed in a PR and run by the operations lead with `bin/sw live --file changes/<file>`. There is no copy of the graph to try it on.

- **Target**: Neo4j 5.26 Enterprise, `live` (production). Not touched.
- **Rule**: every `SITED_AT` from a machine to LD-03 moves to LD-07, with `since` set to the day of the move. `SERVICED_BY`, visits and the LD-03 shop node stay. Sources: `docs/closures.md` step 2, `docs/model.md`, and your request. LD-03 has 38 machines (`docs/model.md`, counts of 2026-11-25).
- **Size**: 38 relationships deleted and 38 created, 76 entities in all, under the 1,000-entity limit. No batching needed.
- **Re-run**: safe. After the first run no machine is sited at LD-03, so a second run matches nothing.
- **Checks for the operations lead before running**:
  - Read-only count: `MATCH (:Machine)-[:SITED_AT]->(:Shop {code: 'LD-03'}) RETURN count(*)` should return 38.
  - `EXPLAIN` in front of the statement, to confirm it compiles on 5.26 with Cypher 5 (the default for this server version). Not run here.
  - Confirm LD-07 exists and is open (`MATCH (s:Shop {code: 'LD-07'}) RETURN s.open`). I could not check this from here.
- **Question for you**: the file uses `date()`, so `since` is the day the operations lead runs it. If the move is recorded on a fixed day, say which and I will set it.
- **Production**: the file is handed to the operations lead, who runs it after review.
- **Not verified**: the statement itself, the LD-03 machine count and LD-07's status. None of them could be checked against `live` from here.
