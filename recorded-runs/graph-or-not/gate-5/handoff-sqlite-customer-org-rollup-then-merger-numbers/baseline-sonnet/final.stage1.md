Decision: recursive-sql

Stay on SQLite with the recursive queries you have. I'd tell Bram it isn't worth moving now. I made no code changes.

**Why**
- Your own trigger for revisiting storage is a nightly rollup past 20 minutes or an account-page subtree query over 150 ms p95. Today the rollup takes about 2 minutes, which is a tenth of the limit and well inside the 30-minute window. The subtree query is 12 ms p95, about a twelfth of the limit, at around 40 loads a minute. Neither trigger is close.
- The data is small: 2,300 organisations, at most 7 levels deep. Both queries use the existing `org_parent` and `invoice_org` indexes. A graph database would add a second system to run, secure and keep in sync with the CRM load, and a new query language for the team. In exchange it would speed up two jobs that already have plenty of headroom.
- An in-memory graph library wouldn't change that. It would add a dependency, which the README rules out ("no third-party packages"), and an in-memory copy to keep fresh, so it's not worth it either.

**"Before it gets out of hand"**
That is a prediction, not evidence, and the agreed thresholds exist so we don't act on predictions. Even a merger that doubled the organisation count would leave a lot of room before either limit. I can't say exactly how the cost grows, because I haven't been able to measure it from here (there is no `var/orgbook.db` in the repo). The two figures I have are your reported timings.

**What I'd do instead of migrating**
- Re-check the two numbers after the merger data is loaded, against the same 20-minute and 150 ms limits.
- Watch two things in particular. The rollup query builds one row per organisation per ancestor, so its work grows with organisations times depth. And the subtree query is cheap per page load, so the risk there is load, not size.

**What would change my answer**
- The thresholds are crossed after the merger and the query or index fixes are exhausted.
- The merger brings in relationships that don't fit a single `parent_id`, such as joint ventures or shared ownership. Then the data is a general graph, not a tree. The current queries and the rollup's sums assume one parent per organisation. A graph model, or at least a link table plus a rethink of the rollup, would be worth looking at at that point.
- A cycle appears in the data. The queries already stop at depth 30 as a safeguard, but that guard doesn't make the numbers right.

If either trigger fires, bring the timings back and we can decide with data.
