Wrote the change file; count before and after: MATCH (c:Callout {kind:'pager-test'}) WHERE c.paged_at < '2026-01-01' RETURN count(c).
