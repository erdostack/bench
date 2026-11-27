# Graph decision

Decision: in-process-library

The question is whether the capacity planning run should use a graph database, networkx in the planner, recursive SQL, or no graph at all, now that the Brno and Pune exports have arrived and all three plants total 1.2 million BOM lines. The user's test host held that BOM in networkx at 1.4 GB resident and ran where-used for all 40,000 components in 3 minutes, which fits the 2 GB allowance and the 10-minute window on one copy, so the earlier wait for the BOM sizes is over. The choice depends on the load time, which has not been measured, and on there being only one copy of the graph per host.

## Workload facts

- Changed components per run: about 40,000 (stated by the user).
- Current call: sql/where_used.sql per component, an unbounded recursive upward walk over bom_line, returning distinct item ids (sql/where_used.sql, UNION over the node column only, so the query itself does not produce one row per route).
- Current cost: 90 ms per call on the Linz data (stated by the user); 40,000 x 90 ms = 3,600 s, about 60 minutes (matches the stated hour). Previously recorded as the same figure; unchanged.
- Time budget: 10 minutes per run, because of the shift handover (stated by the user). Serial SQL calls would need 600 s / 40,000 = 15 ms per component.
- Linz BOM size: 180,000 BOM lines (stated by the user); schema in db/schema.sql, index bom_line_component on component_id.
- All three plants together: 1,200,000 BOM lines (stated by the user). Brno and Pune together: about 1,020,000 lines (derived: 1,200,000 - 180,000). Previously recorded as unknown; this replaces that open fact.
- In-process run, test host: 1.4 GB resident with the BOM loaded into networkx (stated by the user). Per line: 1.4 GB / 1,200,000 = about 1,170 bytes per line, including interpreter and library overhead (derived from the stated figure).
- In-process where-used, test host: all 40,000 components in 3 minutes, 180 s (stated by the user). Per component: 180 s / 40,000 = 4.5 ms (derived). Load time into networkx: not stated.
- Time headroom for the in-process run: 600 s - 180 s = 420 s, about 7 minutes, for loading the BOM and everything else in the run (derived). Load time must come in under that.
- Planner memory allowance: 2 GB more on those hosts, "not a byte over" (stated by the user). Largest combined BOM that fits one copy at the measured rate: 2 GB / 1,170 B = about 1.7 million lines (derived; it is an extrapolation from one test-host figure).
- Headroom on the test host: 2 GB - 1.4 GB = 0.6 GB, about 30% of the allowance (derived). Two copies in one process space would be 2.8 GB, over the allowance (derived).
- Test host and planner host are different machines; the test host's specification is not stated, and the planner host's memory and speed are unknown.
- Freshness: BOMs are copied from PLM nightly (README.md); a run reads that copy.
- Engine: Postgres 16 for Linz (README.md); minor version unknown. Tests use SQLite.
- Measured by this agent: none. The repo holds no data (var/ is gitignored and absent), so no plan, row count or timing could be taken. The figures above are the user's measurements on a test host.
- No docs/graph/CONTEXT.md exists, so the read-only setting and engine version come from README.md only.
- unknown: the load time of 1.2 million lines into networkx; the planner host's memory and speed; the number of planner copies and processes per host; the distinct upward set size per component; the plan of where_used.sql on Postgres; the set-based rewrite's time (not run); Postgres minor version.

## Options considered

- graph-database (a dedicated graph store): rejected, because the run is a nightly-fed batch with a 10-minute window, not an online request with a latency budget, and an in-process copy already fits the allowance on the measured figures; no measurement shows Postgres failing at any depth, and the slow part is the per-statement loop, not the database engine. A second store and its load step would not be justified by the present evidence.
- in-process-library (networkx in the planner, the BOM held in memory): chosen, because the measured 1.4 GB for 1.2 million lines is inside the 2 GB allowance with one copy, and the measured 3 minutes for all 40,000 components leaves about 7 minutes of the 10-minute window for loading and the rest of the run. The batch job reads the whole BOM each night, which is the shape this option fits. Before go-live the load time and the planner-host figures must be measured.
- recursive-sql (recursive queries on Postgres, already operated): rejected for the approach in place, because it is measured failing the window: 90 ms per call on Linz (stated by the user) gives about 60 minutes for 40,000 components (derived), six times the 10-minute budget. A set-based rewrite could cut the per-statement overhead, but it has not been run, so under the rules it does not reopen this rung; it stays the fallback if the memory headroom is lost.
- no-graph (plain joins, no traversal): rejected, because the question is "every assembly above it at any depth", an unbounded walk.

## What would change the decision

1. Load time of the 1.2 million BOM lines into networkx on the planner host, measured on a run with the real export. If load time plus the 3-minute where-used run exceeds 10 minutes (load above about 7 minutes), in-process-library is out for this window; then measure the set-based recursive rewrite on Postgres, which would move this to recursive-sql. Owner of the 10-minute window: the shift handover (planners).
2. Copies per planner host and processes per run: two copies in memory at once (for example, a second process or a reload while the first is live) is about 2.8 GB, over the 2 GB allowance, and would move this to recursive-sql or a smaller load. Owner of the 2 GB limit: ops, who should state the copy count.
3. Combined BOM above about 1.7 million lines, or a measured per-line figure on the planner host above about 1,670 bytes (2 GB / 1.2 million lines), would take the BOM past the allowance for one copy. Owner of the 2 GB limit: ops.
4. Planner-host figures (memory, CPU) that differ from the test host. The 3-minute and 1.4 GB figures were measured on a test host; the planner host must be measured before go-live, and a slower host could push the run past the window.
5. A set-based recursive rewrite on Postgres 16 (one statement over all changed components), run on Linz and inside 10 minutes, would hold recursive-sql and be the preferred option if memory becomes the constraint. Not run yet.
6. graph-database would move here only if the walk must run online with a latency budget, many at once, over a BOM too large for a copy per process, and Postgres is measured failing at that depth, with the failure count and its total. Nothing in the present evidence shows this.

Nothing in the repo was changed beyond this file.
