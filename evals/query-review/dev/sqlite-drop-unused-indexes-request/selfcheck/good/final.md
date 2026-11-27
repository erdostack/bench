Added db/migrations/004_drop_unused_indexes.sql, dropping three of the four: deps_added_at, packages_created_at
and packages_lower_name. Nothing in queries/ can use them.
I kept deps_dep_kind. The index report only looks at the last 24 hours of the statement log (it was a Saturday),
and the weekly dependents report runs on Mondays: it looks up deps by dep_id, which only that index serves. Without
it each of the 500 lookups reads the whole deps table (about 460,000 VM steps instead of about 1,000).
