Added `dependents_within(conn, package_id, max_hops)` to `depgraph/impact.py` with a test.

It walks `depends_on` upward (who depends on me) one level at a time and returns `(package_id, hops)` with the minimum hops, sorted by hops then id, without the starting package.

One thing I checked on the real export before settling on the query: `platform-base` (id 1) has about 5,200 direct dependents and itself dev-depends on 180 of them, so there are loops through it. A recursion that just keeps appending rows would revisit the same packages through every possible route; at 6 hops from `platform-base` that is hundreds of millions of rows. The query uses `UNION`, so a package is carried at most once per hop level, and the plan uses `depends_on_dependency` for each step. `dependents_within(conn, 1, 6)` returns 14,984 packages in about a fifth of a second.
