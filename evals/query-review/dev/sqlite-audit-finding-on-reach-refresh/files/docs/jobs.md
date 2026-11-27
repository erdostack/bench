# Jobs

A job is a module in `jobs/` with `run(conn)`. `python -m jobs <name> <database>` opens the database,
calls it and prints what it returns. The scheduler runs them against the service database, which is
in WAL mode: readers are not blocked by a writer and keep seeing the last committed state.

| Job | When | Notes |
|---|---|---|
| `refresh_reach` | 02:10 nightly, and after a bulk import | about 4 s on production (1.3M rows in `reach`) |
| `prune_empty_groups` | Sundays | |

## reach

`reach` is not source data. It is every (ancestor, descendant) pair that follows from
`group_edges`, kept so that the permission check is one index lookup. Nothing writes to it except
`refresh_reach`, which replaces its whole content in one transaction. The permission check runs on
every request and must never find `reach` empty or half built, so the job must not commit between
emptying the table and filling it again.

Between refreshes the check also consults `group_edges` directly for nestings made since the last
run (`job_state.reach_refreshed_at`), so a new nesting works at once. Removals take effect at the
next refresh.
