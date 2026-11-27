Still stands: yes

The decision stays `graph-database`. Markus's work helped, but Postgres is still far over the 30 s limit in the OEM contract.

Old number next to new, against the 30 s contract limit (stated by the user):
- Forward containment trace on Postgres, full copy: 14 minutes (840 s) recorded, 6 minutes (360 s) now. That is 28 times the limit before and 12 times now (360 / 30).
- Backward root-cause trace on Postgres, full copy: no number was recorded, 4 minutes (240 s) now. That is 8 times the limit (240 / 30).
- Graph database trial on a full copy, from the record: 1.2 s forward and 0.9 s backward, while keeping up with the MES write rate.

The covering indexes and the replica cut the forward time by more than half (840 s to 360 s). The record's own condition for moving back to `recursive-sql` is Postgres at or under 30 s on the full copy, forward and backward, and that is not met. The other conditions are not met either. The only two ways to stay on Postgres are making the traces about 12 times faster or having the OEM relax the contract. A relaxed limit would have to be more than 14 minutes, so 6 minutes is not enough. The in-memory option is unchanged at about 1.9 TB against the 64 GB limit.

Markus's "good enough" is a judgement against a different bar. 6 and 4 minutes might be fine for an internal investigation, but the OEM contract says 30 s for containment and for root cause. Only the OEM contract owner can relax that. If it did change, the decision would move to `recursive-sql`, and you would want that in writing first.

I did not change `docs/graph/DECISION.md` or anything else in the repo, because no condition for changing it was met. If you want the new figures on record, I can add them next to the old ones (14 minutes now 6, backward 4) under the facts and the "tried" line. The record's "tried" line currently covers only the DBA's indexing and partitioning, so the covering indexes and the replica are not in it.

What I did not check: the 6 and 4 minutes are Markus's figures. There is no database copy in the repo, so I could not re-measure. I also don't know the query mix or whether the replica was under write load while he measured.
