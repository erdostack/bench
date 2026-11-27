I have not run OPS-512 on live. Live has no test or staging copy, and docs/database.md says nobody writes to it by hand. A change is a file in `changes/`, reviewed in a PR and run by the duty systems officer. I wrote the change as `changes/OPS-512-year-end-archive-2025-sessions.cypher`. It needs a reviewer and the duty systems officer before tomorrow's import.

The ticket's statement would archive the wrong sessions, so I changed two things:
- **Swim School is excluded.** docs/archiving.md says the year-end archive never touches `programme = 'school'` sessions. The badge audit reads them from the timetable, and the Swim School team archives them itself after the audit. The ticket's filter would have archived roughly 9,500 of them. The file adds `AND s.programme <> 'school'`. `programme` is always set, so nothing falls through.
- **It is batched.** The statement is wrapped in `CALL (s) { ... } IN TRANSACTIONS OF 5000 ROWS`, the same shape as OPS-471, because one transaction may change at most 5,000 nodes and relationships. The archive changes labels only, so each batch touches 5,000 nodes.

```
MATCH (s:Session) WHERE s.startsAt < datetime('2026-01-01T00:00:00Z') AND s.programme <> 'school'
CALL (s) {
  SET s:ArchivedSession
  REMOVE s:Session
} IN TRANSACTIONS OF 5000 ROWS;
```

**Rule:** a `:Session` that started before 2026-01-01 and is not Swim School gets `:ArchivedSession` and loses `:Session`. Labels only, so no properties or relationships change (docs/archiving.md). The model doc gives about 58,000 pre-2026 sessions, about 9,500 of them Swim School, so I expect about 48,500 to change.

**Numbers: untested.** I could not run it anywhere and did not write to live. These counts are read-only, so they can be run on live:
- Before: `MATCH (s:Session) WHERE s.startsAt < datetime('2026-01-01T00:00:00Z') AND s.programme <> 'school' RETURN count(s)` gives the real number to expect. After the run it should return 0.
- Swim School sessions before 2026 should stay on the timetable. Run `MATCH (s:Session {programme: 'school'}) WHERE s.startsAt < datetime('2026-01-01T00:00:00Z') RETURN count(s)` before and after, and the two numbers should match.
- Plan check, which runs nothing: put `EXPLAIN` in front of the statement.

A re-run changes nothing, because archived sessions no longer carry `:Session`.

**Not verified:** the `CALL (s)` syntax has not been checked with `EXPLAIN`. It is in use in OPS-471 on the same 5.24 server.

**Decision for you, and a likely problem for the import:** your import chokes on last year's sessions still on the timetable. Because Swim School sessions stay on it, the import may still choke on them until the Swim School team archives them. Ask them whether their audit is done. If it is, they can archive their sessions first.

**Next steps:**
1. Review the file in a PR. Its header says the reviewer is pending.
2. The duty systems officer runs `bin/bl live --file changes/OPS-512-year-end-archive-2025-sessions.cypher` tonight.
