# Graph decision

Decision: recursive-sql

Piotr asks whether the BOM should move to a graph database so the references are real. The question is a rolled-up unit cost per quote, walking a BOM of up to 7 levels, and the finding it turns on is that a walk of this size runs in about 0.1 ms per quote on SQLite (measured on synthetic data at the stated scale, 200 walks in about 16 to 20 ms). The dangling references come from the ERP load, not from the storage engine, so a graph store would not make them real either.

## Workload facts

- Items: 9,000 (stated by the user)
- BOM lines: 31,000, about 3.4 per item on average, 31,000 / 9,000 = 3.44 (stated by the user; the repo sample has 6 items and 7 lines, not the export)
- Depth: BOMs up to 7 levels (stated by the user); the quote walk must stop at depth 7
- Load: about 200 quotes per day, so about 200 rolled-cost walks per day (stated by the user); no latency budget was stated for the quote page
- Writes and freshness: the database is rebuilt from the ERP CSV export by `quotecalc/load.py` (`README.md`); no online writes in the repo
- Orphan lines: about 300 BOM lines point at item ids that are no longer in the item table since the spring ERP purge (stated by the user); 300 / 31,000 = 0.97% of lines
- Finance rule: if anything anywhere under an assembly is missing from the item table, that assembly gets no cost and the quote page shows it incomplete, never a partial total (stated by the user)
- Schema: `bom_line.component_id REFERENCES item (id)` with primary key `(parent_id, component_id)` and no index on `component_id` (`db/schema.sql`)
- Enforcement: no `PRAGMA foreign_keys` appears anywhere in the code (grep of `quotecalc/`), and it is 0 after `load.load` (measured on a scratch copy of the sample), so the dangling references load silently
- Sample orphan: `bom_line` row `3,41,1` points at item 41, which is absent from `data/items.csv` (`data/bom_lines.csv`, `data/items.csv`); the sample holds 1 orphan line out of 7 (measured)
- Sample walks: from item 1 the depth-limited walk reaches 8 rows, one of them the missing id 41; from item 2, 5 rows with 1 missing; from item 3, 3 rows with 1 missing; from item 4, 1 row, complete (measured with the app's own loader on a scratch copy)
- Measured, synthetic, scale A (seed 7, generator in scratch, not the real export): 9,000 items, 29,458 lines, 4,500 made parents; distinct-node walk with `UNION` and depth limit 7 over 200 roots: mean 38 nodes, worst 218 nodes, 16.1 ms for 200 walks, about 0.08 ms per quote (measured)
- Measured, synthetic, scale B (same seed, generator in scratch): 9,000 items, 28,356 lines, 1,500 made parents, up to 38 children per parent; mean 72 nodes, worst 450 nodes, 19.5 ms for 200 walks, about 0.10 ms per quote (measured)
- Root-to-node paths within 7 levels (what a per-route walk would produce, counted by a dynamic-programming pass over the same synthetic graphs, first 50 roots): scale A median 14, max 218; scale B median 37, max 456 (measured)
- Daily database time at the stated load: 200 quotes x about 0.1 ms = about 20 ms per day (derived from the measurements above)
- Generator caveat: the synthetic graphs fall short of 31,000 lines because candidate children are rejected when they would break the level order, so the shape is an approximation, not the real export
- Memory: not measured; no in-process copy is needed for this rung, so none was sized
- unknown: real fan-out and depth distribution of the export (only 6 items are in the repo); how many ancestors each of the ~300 orphan lines affects, which needs a walk over the real data; the quote page latency budget; whether the ERP export has items with `kind` values other than `made` and `bought`; the data rows beyond the sample were not in the repo

## Options considered

- graph-database (a dedicated graph store; Piotr's proposal, no product named): rejected, because the walk is depth-limited to 7 and measured at about 0.1 ms per quote on SQLite, so a second storage engine adds a load step and a sync problem with no measured gain, and the dangling references would still exist in a graph store unless the loader rejects them, which Finance's rule does not allow (the assembly must be flagged, not dropped)
- in-process-library (the edges loaded into memory): rejected, because recursive-sql already meets the need at the stated load; loading 31,000 edges into memory adds a reload step against the rebuild from the export, and no measurement showed a need for it
- recursive-sql (recursive queries on the database already run): chosen, because the walk is a fixed-limit walk from one item (rung 2 of the ladder), SQLite is already operated, and the measured work of 14 to 456 paths and 38 to 450 distinct nodes per root is far inside the budget implied by 200 walks per day; the orphan rule is a `LEFT JOIN` to `item` that flags an assembly incomplete when any reached component has no item row
- no-graph (plain joins, no traversal): rejected, because the rolled-up cost follows a relation between items of the same kind (a made item to its components, which may be made) for a data-dependent depth of up to 7 levels

## What would change the decision

- A walk on the real export, loaded into a copy of the database, that exceeds the quote page's latency budget at depth 7 would move this to in-process-library (the budget is owned by whoever owns the quote page; the repo sets none)
- A percentile of walk time over budget, or a failure rate with its total, measured on the real export at depth 7 would move this to in-process-library, and to graph-database only if the required depth becomes unbounded or a whole-graph algorithm (such as where-used across all assemblies, every day) is needed
- A business need for depth beyond 7 or for an unbounded walk (stated by the user as a rule, not a claim about the workload) would move this to graph-database
- A rule that the export itself must reject dangling references (so that orphan rows never load) would not change the option, but it would change the data path in `quotecalc/load.py`; enabling `PRAGMA foreign_keys` now would make the load fail on the existing ~300 orphan lines, so it is not recommended until those are resolved
- Trial before committing to recursive-sql: load the real export into a copy, run the depth-7 rolled-cost walk for a sample of about 200 items drawn from the quote history, record the distinct-node and path counts and the time, and list every assembly whose walk reaches an orphan line
