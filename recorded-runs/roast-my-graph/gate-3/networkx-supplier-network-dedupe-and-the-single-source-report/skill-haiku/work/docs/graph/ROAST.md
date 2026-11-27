# Roast: supplynet

Verdict: Not nothing serious. The duplicate merge leaves a self-loop on nine companies, and those nine drop off the single-source list the risk team works from. Each of the nine has one real supplier, so each should be on the list. The tests pass because no test covers that case. Fix the in-edge loop, then add the test.

Judged against:
- README: edges point supplier -> customer; duplicates are folded into keep before any report runs; stock moved between the two entities of the same company is booked as a sale; the single-source list is the quarterly input for the risk team, and a company missing from it is not looked at (README.md).
- data/duplicates.csv: 24 keep,dup pairs, checked by hand. Nine of them have a ledger edge keep -> dup (C104 -> D01, C214 -> D02, C085 -> D03, C154 -> D04, C193 -> D05, C223 -> D06, C159 -> D07, C060 -> D08, C175 -> D09). Nine more have a dup -> keep edge, which the code handles correctly.

## Findings

### critical: `merge_duplicate`
The merge takes a sale between two halves of one company and files it as the company buying from itself, which is the one thing a single-source list cannot survive.
Problem: The in-edge loop does not skip supplier == keep. A keep -> dup ledger edge becomes a keep -> keep self-loop. That self-loop counts toward in_degree, so keep looks like it has two suppliers and drops off the single-source list. Shipped data: 9 companies (C060, C085, C104, C154, C159, C175, C193, C214, C223) each with one real supplier are missing from the 59-company list.
Fix: In the in-edge loop, add `if supplier == keep: continue`, the same guard the out-edge loop already has for customer == keep. In memory on the shipped data, this removes all self-loops and grows the list from 59 to 68 (the nine companies above are the ones added). Not written to the repo.

### low: `tests/test_dedupe.py`
The tests say the code is fine while the code is wrong.
Problem: No test has a supplier equal to keep. test_dup_selling_to_keep_is_not_kept covers only the customer side, so the passing suite says nothing about the keep -> dup direction.
Fix: Add a case with an edge K -> D and a second supplier S1 -> K. After merge_duplicate(G, K, D), assert no self-loop on K and that K is not single-source.

### low: `apply_merges`
A typo in the pair list fails quietly.
Problem: Rows whose keep or dup is missing from the graph are skipped with no message, so an unmerged duplicate would leave the single-source list wrong without any signal. The shipped pairs all match.
Fix: Raise or log when a row's keep or dup is not in the graph.

### low: `load`
Question to confirm: can two ERPs book the same supply?
Problem: add_edge overwrites the spend of a repeated supplier and customer pair instead of adding to it. The shipped supplies.csv has no repeated pairs, and README says the data comes from both ERPs.
Fix: If repeats can occur, sum the spend as merge_duplicate does. Otherwise, fail on a repeated pair.

## Holds up
- Out-edge branch of `merge_duplicate`: skipping customer == keep correctly drops dup -> keep sales, which are stock moved within one company, as README says.
- Spend summing in `merge_duplicate`: the test test_spend_is_added matches the code, and the sums are correct for both directions.
- `single_source`: in_degree == 1 is the right test once self-loops are gone; the 68-company result on the shipped data is consistent with the 9 companies above.
- `load`: every id in both CSVs exists in companies.csv, so no node is created by accident.

## Not checked
- The ledgers themselves were not available beyond the CSVs in the repo, so the duplicate pairs were checked only against README and the files.
- The fix was run in memory against the shipped data, not written into the repo, and the test was not added.
- Nothing was run beyond the tests and the report.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
