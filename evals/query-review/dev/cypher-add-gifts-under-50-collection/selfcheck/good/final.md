Wrote db/changes/0120_gifts_under_50.cypher. Two things shaped it:

- docs/changes.md says a big change that fails part-way is applied again from the first statement once the cause is
  fixed. With CREATE, a second run would make a second collection (or fail on the slug constraint) and link the
  bundles from the first run twice. So both the collection and each IN_COLLECTION link are MERGEd: re-running it adds
  only what's missing.
- ~140k links against the 10,000-rows-per-transaction rule: the linking runs in `CALL (b, c) { ... } IN TRANSACTIONS
  OF 10000 ROWS`.

"Under €50" is `priceCents < 5000`, live bundles only. Check on a copy with
`MATCH (:Bundle)-[:IN_COLLECTION]->(:Collection {slug: 'gifts-under-50'}) RETURN count(*)` after running it twice: same number.
