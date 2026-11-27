# Review: waternet (waternet/, tests/, data/)

Review: waternet/trace.py calls trace_source, which the duty engineer runs on a discoloured or contaminated water report. On the shipped data it can leave out a tank that feeds the reported point. It reads the 2023 `fed_from` column, not pipes.csv, and the two already disagree.

Judged against:
- Engine: NetworkX 3.x (README.md). NetworkX 3.7 with Python 3.13 was installed here.
- Size: 365 nodes and 470 pipes, counted from data/nodes.csv and data/pipes.csv. README.md gives no size.
- Interactive path: trace_source, run by the duty engineer when a customer reports discoloured or contaminated water (README.md). How often that happens: not stated.
- Writers: the field team, through waternet/edits.py, "whenever a main is laid, replaced or cut off" (README.md). How often: not stated.
- Invariant: pipes.csv lists each pipe "in the direction water flows" and "the field team keeps this file current" (README.md).
- Required result: trace must list "every reservoir, tank and junction that could have fed the water" to the reported point (README.md).
- Stored feed relation: the `fed_from` column in nodes.csv "came with the 2023 GIS export" (README.md). Nothing in the files says it is updated.

## Findings

### critical: `fed_from`
The feed relation is written down twice, and the old copy is the one trace_source reads.
Problem: The `fed_from` column in data/nodes.csv (2023) and the rows in data/pipes.csv (kept current by waternet/edits.py) disagree on the shipped data. Six `fed_from` pairs have no pipe, for example J-0009 is listed as feeding J-0016 and no pipe joins them. Eighteen pipes are missing from `fed_from`, for example J-0070 to J-0092 and J-0072 to J-0083. trace_source takes its candidate set only from `fed_from`, so for these nodes it omits tank T-2, which does reach them by pipe: J-0083, J-0088, J-0092, J-0098, J-0102, J-0111 and J-0119. For J-0092 the pipe path is T-2 to J-0003 to J-0014 to J-0030 to J-0051 to J-0070 to J-0092. add_pipe and remove_pipe in waternet/edits.py change pipes.csv and never touch `fed_from`, so each edit widens the gap.
Fix: Remove the `fed_from` column from data/nodes.csv and its load in waternet/loader.py. Make upstream return `nx.ancestors(G, node)` on the pipe DiGraph, and have trace_source take both the set and the hop counts from that graph. Before the change, write a test that asserts trace_source("J-0092") includes T-2 on the shipped data, and run it against the current code so it fails first. Confirm the result after the change.

### medium: `trace_source`
Problem: `dist.get(c, 99)` gives any candidate that no pipe path reaches the hop count 99, and sorts it in with real distances. On the shipped data there are 712 such (node, candidate) pairs. For J-0016 the trace ends with J-0009 at 99 hops, and J-0009 is not connected to J-0016 by any pipe. An engineer reads 99 as far away, not as not connected.
Fix: Once `fed_from` is gone, every candidate is a pipe ancestor, so the sentinel can go. Read distances from the same reversed graph used for the candidate set, and raise if a candidate is missing from it rather than returning 99.

### low: `tests/test_analysis.py`
Problem: The two tests build a four-node graph where `fed_from` matches the edges by construction, so they pass (2 passed) and cannot catch the drift. Nothing tests trace_source, isolation_set, the loader or edits.py.
Fix: Add a test that checks trace_source against the pipe ancestors for every node on the shipped data, and a test that checks the order and hop counts of trace_source on a small graph where `fed_from` is wrong. Write them before the fix, as the eval for the change.

## Holds up
- `downstream`: nx.descendants on the pipe DiGraph built by waternet/loader.py follows the direction in pipes.csv, so it returns what water from the node can reach. This changes only if the flow direction in pipes.csv is wrong.
- `isolation_set`: returns the pipes that leave the node, which is what stops its water reaching anyone downstream. No defect found, though no test covers it.
- `upstream`: the `seen` set stops the walk, and the shipped `fed_from` graph has no cycles (checked). The walk is guarded even though it reads the stale column.
- `waternet/loader.py`: every pipe endpoint is in data/nodes.csv (0 missing), so `G.nodes[c]["kind"]` in trace_source does not fail on the shipped data. No pipe pair is duplicated (470 rows, 470 unique pairs).

## Not checked
- Nothing was written. The shipped data was read in memory with NetworkX, and the test suite was run with pytest (2 passed).
- waternet/edits.py was not executed, because it writes data/pipes.csv. Its effect on `fed_from` comes from reading the code.
- `python -m waternet.trace` was not run. trace_source was called directly.
- Whether the 2023 `fed_from` or the current pipes.csv is the real network is not in the repo. This review assumes the README is right that pipes.csv is current.
- An unknown node name raises a bare KeyError from `G.nodes[n]` in upstream. Not filed.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
