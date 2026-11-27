I have not run the statement on `league`. It is the registrations database for the league, it is production, and it is the only copy, so changes there go through a file the registrations secretary reviews and runs. I've written that file instead.

**File:** `changes/2026-11-26_lapse_2026-27_players.cypher`. It lapses every player whose `lastSeason` is before `'2026-27'`, the same rule as your statement and as `docs/registration.md`. It is batched at 500 players per transaction, because the league's limit is 1,000 nodes per transaction (`docs/operations.md`). The one-liner would have changed about 3,900 players in one transaction. Last year's file was about 800 players, so it fitted in one. The secretary runs it with `bin/reg league --file changes/2026-11-26_lapse_2026-27_players.cypher`.

- **Rule:** every `:Player:Registered` whose `lastSeason` is before `'2026-27'` gets `:Lapsed` and loses `:Registered`. Nothing else changes, and `PLAYS_FOR` stays. Source: `docs/registration.md`. Coaches are not included, because they lapse on their DBS check.
- **Target:** `league`, Neo4j 5.24, production: yes.
- **Count:** about 3,900 players, from `docs/model.md` (2026-11-25). I could not count it here. Before the run, the secretary should check it with `MATCH (p:Player:Registered) WHERE p.lastSeason < '2026-27' RETURN count(*)`, and with `EXPLAIN` on the change.
- **Limit:** 500 nodes per transaction, under the 1,000 limit. Each player is one node.
- **Re-run:** safe. A lapsed player no longer matches `:Registered`, so a second run changes nothing.
- **Test:** not done. There is no copy of `league` to try it on, and `bin/reg` only queues statements; it returns no results. The `CALL (p) { … } IN TRANSACTIONS` form needs Neo4j 5.23 or later, which 5.24 has. The database's default query language is not in the repo, so the secretary should confirm the statement with `EXPLAIN` first.
- **Also check:** whether any registered player has a `lastSeason` that is not in `YYYY-YY` form, or is null. Such players would not match `<`, so they would stay `:Registered`. The secretary should count these before the run.

**Production:** not run. The file is for the registrations secretary to review and run.
