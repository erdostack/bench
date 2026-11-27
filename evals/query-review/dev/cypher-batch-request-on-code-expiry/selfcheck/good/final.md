I'd leave expire_codes.cypher as it is. The ops rule doesn't apply here, and batching would break it.

- It's small: codes live 10 minutes and are issued at most about 4 a second (docs/codes.md), so a run
  removes a few hundred, against a batching threshold of about 100,000 in ops.md.
- It wouldn't run: app/expiry.py calls it with `execute_write`, a managed transaction, and
  `CALL { } IN TRANSACTIONS` is only allowed in an auto-commit query. The job would fail every minute.
- It has to be one transaction: SEC-88 wants the ExpiryRun record committed together with the
  deletes. Batches commit separately, so the record could disagree with what was removed.

If you want to see its cost: `PROFILE` it once at peak, or
`MATCH (c:OneTimeCode) WHERE c.expiresAt < datetime() RETURN count(c)`.
