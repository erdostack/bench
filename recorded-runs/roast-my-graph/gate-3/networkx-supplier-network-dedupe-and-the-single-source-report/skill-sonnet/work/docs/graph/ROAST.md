# Roast: supplynet (build.py, dedupe.py, risk.py, report.py)

Verdict: One critical bug, and it sits in the file the tests are proudest of. `merge_duplicate` leaves a self-loop on `keep` whenever the keep company supplied its own duplicate, and 9 of the 24 pairs in `data/duplicates.csv` do exactly that. The single-source list printed 59 companies; the right list has 68. Nine single-source companies are missing, and the risk team does not look at anything missing from the list. The rest is fine.

Judged against:
- Engine and library: NetworkX 3.7 on Python 3.13 (checked on this machine); production versions: not stated.
- Edges point `supplier -> customer`, built from the purchase ledgers (README.md, `load` in `supplynet/build.py`).
- `data/duplicates.csv` lists `keep,dup` pairs, checked by hand; `apply_merges` folds each `dup` into its `keep` before any report runs. Duplicates are often linked to each other, in either direction, because stock moved between the two entities of one company is booked as a sale (README.md).
- `python -m supplynet.report` prints companies that buy from exactly one supplier. The risk team goes through it every quarter and does not look at a company missing from it (README.md).
- Sample data: 304 companies, 600 supply edges, 24 duplicate pairs (`data/`). Production size and write rate: not stated.

## Findings

### critical: `merge_duplicate`
The function carefully refuses to make `keep` a customer of itself, in one loop. In the other loop it merrily makes `keep` its own supplier. A company, supplying itself, is the first thing a risk team would love to believe in.
Problem: When `apply_merges` folds a `dup` that `keep` supplies (a `keep -> dup` edge, which README.md says occurs in either direction), the second loop in `merge_duplicate` (`for supplier, _, data in list(G.in_edges(dup, data=True))`) has `supplier == keep` and calls `G.add_edge(supplier, keep, ...)`, which is `keep -> keep`. The first loop has `if customer != keep`; this one has no such check. In `data/duplicates.csv` this happens for 9 pairs: C104/D01, C214/D02, C085/D03, C154/D04, C193/D05, C223/D06, C159/D07, C060/D08, C175/D09. `single_source` counts the self-loop as a supplier (`G.in_degree(n) == 1`), so each of those nine companies, with exactly one real supplier, has in-degree 2 and drops out of the list: C060, C085, C104, C154, C159, C175, C193, C214, C223. Run on the shipped data: 59 entries printed instead of 68. The tests do not catch it because `test_dup_selling_to_keep_is_not_kept` only covers `dup -> keep`.
Fix: Skip the self-loop in the second loop, the same way the first one does:
```python
for supplier, _, data in list(G.in_edges(dup, data=True)):
    if supplier != keep:
        spend = data["spend"] + G.edges[supplier, keep]["spend"] if G.has_edge(supplier, keep) else data["spend"]
        G.add_edge(supplier, keep, spend=spend)
```
Run on the shipped data (checked by merging the 24 pairs with this change and comparing against an independent merge): no self-loops and 68 single-source companies. Add a test for the other direction in `tests/test_dedupe.py`: `graph([("S1", "K"), ("K", "D"), ("D", "C1")])`, merge `K` with `D`, then assert `not G.has_edge("K", "K")` and `single_source(G) == ["C1", "K"]`. `nx.contracted_nodes(G, keep, dup, self_loops=False)` has no self-loop problem but overwrites the edge spend rather than adding it (checked on NetworkX 3.7: two edges of 1.0 give 1.0, not 2.0), so it is not a replacement here. The hand-written merge stays, with the guard.

## Holds up
- `single_source`: `in_degree(n) == 1` is the right definition once the graph has no self-loops, and the edge direction (`supplier -> customer`) matches `load`. It is correct on a clean graph, so it was not changed; the missing companies come from the merge. Optional insurance: ignore self-loops there too.
- `load` in `supplynet/build.py`: edges are written supplier to customer, as `README.md` and the docstring say. Every id in `data/supplies.csv` appears in `data/companies.csv`, so no node is created without a name.
- `merge_duplicate`, the rest: `dup -> keep` edges are dropped on purpose (a sale between two records of one company is not a supply relationship), and spend is added where `keep` already had the edge. Checked against an independent merge on the shipped data: no spend differs.
- `apply_merges`: the `in G` guard only skips a pair when one of the ids is not in the graph; all 24 pairs have both ids on the shipped data.
- `suppliers_of(G, company)[0]` in `supplynet/report.py`: only used on companies with exactly one supplier, so index 0 is the supplier.

## Not checked
- Production data, size and write rate: only the 304-company sample was available.
- Whether any pair in `data/duplicates.csv` is itself wrong (it is checked by hand, per the README) or would chain (a `dup` that is also a `keep`): none does on the shipped data.
- The 3 existing tests pass and I ran them (`python -m pytest tests`); they pass without the fix, which is the point.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
