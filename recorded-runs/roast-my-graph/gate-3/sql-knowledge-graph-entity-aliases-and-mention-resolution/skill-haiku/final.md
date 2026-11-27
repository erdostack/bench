Not sound as it stands. The ingest slowdown is almost certainly the 2026-10-14 change.

That change added trim() to the alias match in queries/resolve_mention.sql. The index alias_norm is on lower(alias_text), so the query no longer uses it, and every mention scans the whole alias table. On a scaled-down copy, the scan took about 256 ms per mention, against about 0.07 ms with the index. At 50,000 mentions a minute, that cannot keep up. The 31-million-row cost is extrapolated, not measured.

The fix is to strip the stored trailing spaces once, trim on write in queries/add_alias.sql, and query lower(alias_text) = lower(trim($1)) so the existing index is used again. If the data cannot be cleaned yet, a stopgap index on lower(trim(alias_text)) fixes the query without changing the data.

The rest of the schema and the other queries check out. One low question: whether the seen count should count repeated alias rows or distinct sources.

Findings are in findings.json, and the full review is in docs/graph/ROAST.md. I ran the plans on a throwaway PostgreSQL 16 cluster and removed it afterwards. I did not change the repo.
