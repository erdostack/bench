Nothing to fix. The LIKE is a prefix match on a NOCASE-indexed column with the pattern bound as a single
parameter, so SQLite uses the index (range search). The review's "LIKE never uses an index" doesn't apply.
