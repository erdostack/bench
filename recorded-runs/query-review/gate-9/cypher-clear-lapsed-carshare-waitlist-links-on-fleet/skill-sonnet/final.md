I did not run this on `fleet`. `docs/environment.md` says `fleet` is production, and that nobody runs writes on it by hand. A change there is a numbered file that gets reviewed in a PR and run by the fleet on-call. I also can't run Cypher from this machine: there is no Neo4j copy or staging database to try it on.

Instead I wrote the change as `changes/0023_clear_lapsed_waitlist.cypher`:

```
MATCH (:Member)-[w:WAITLISTED]->(:Zone)
WHERE w.since < date('2026-05-01')
CALL (w) {
  DELETE w
} IN TRANSACTIONS OF 5000 ROWS;
```

Your one-liner would have deleted the right rows, but in a single transaction. The repo's limit is 5,000 rows per transaction, because the app writes all day. The file keeps your filter and wraps the delete in batches of 5,000. It only deletes WAITLISTED relationships, so no Member or Zone node is touched and no batch can balloon.

**Rule**: delete WAITLISTED relationships whose `since` is before 2026-05-01. `since` is a DATE, so I compared it with `date()`. Sources: your request, `docs/model.md` (a place lapses six months after `since` unless renewed, and the screen does not hide lapsed ones), `docs/environment.md` (change-file format and the 5,000-row limit).

**Numbers**: untested. I could not count the rows, so there is no "should change" number yet. The model doc puts the total at about 33,000 WAITLISTED relationships. Whoever reviews it should run these:
- Before: `MATCH (:Member)-[w:WAITLISTED]->(:Zone) WHERE w.since < date('2026-05-01') RETURN count(w)`. Put the number in the PR.
- After: the same query should return 0, and the total WAITLISTED count should drop by exactly that number.
- To check the syntax without writing, put `EXPLAIN` in front of the statement on `fleet`. The `CALL (w) { ... }` form needs Neo4j 5.23 or later and the repo is on 5.24, but I could not confirm that against a live server.

**Production**: `changes/0023_clear_lapsed_waitlist.cypher` is waiting for PR review and the fleet on-call to run with `bin/cq fleet --file changes/0023_clear_lapsed_waitlist.cypher`. I did not run it.

**Questions for you or the reviewer**
- The header needs a ticket id and I don't have one. It says `FLEET-???`, so please fill it in.
- You said 1 May is six months back, but today is 26 Nov, so the six-month cutoff is actually 26 May. I used your 1 May date, which means places from 1 to 25 May stay on the screen. If you want every lapsed place gone, change the date in the file.
- Deleting places leaves gaps in `rank`. The screen only sorts by `rank`, so it should look fine, but the gaps remain.
- A place with no `since` value would not match the filter and would stay.

**Not verified**: the row count, the syntax on Neo4j 5.24, and the batching, since nothing here could run.
