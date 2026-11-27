ops.md is right that DETACH DELETE should be batched: CALL { } IN TRANSACTIONS OF 1000 ROWS bounds
heap and lock contention, and you'd switch app/expiry.py from execute_write to an implicit
session.run so the inner transactions are allowed. I haven't changed anything yet; PROFILE it first.
