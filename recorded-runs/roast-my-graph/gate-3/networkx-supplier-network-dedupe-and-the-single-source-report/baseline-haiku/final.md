The tests pass, but the single-source list is wrong. It is missing nine companies that buy from exactly one supplier, and the tests do not catch it. Findings are also in `findings.json` in the repo root.

**Critical: `merge_duplicate` creates self-loops.** The out-edge loop skips customers equal to keep, but the in-edge loop has no matching check for suppliers equal to keep. When keep sold to dup, which the README says happens with intra-company stock transfers, the result is a keep -> keep edge. Nine companies in the shipped data get one: C060, C085, C104, C154, C159, C175, C193, C214 and C223. Each has exactly one real supplier, but the self-loop makes its in-degree 2, so it drops off the list. I ran the pipeline in memory: the list has 59 rows, and 68 with self-loops excluded. Fix: add `if supplier != keep` to the in-edge loop, and add a test for the keep -> dup case. The existing test only covers dup -> keep.

**High: `single_source` counts self-loops.** It uses in-degree, so a self-loop counts as a supplier. Compute the supplier count without self-loops, and remove them in the merge and load steps as well.

**High: `apply_merges` skips rows silently.** Any row whose keep or dup is missing from the graph is skipped without a message. That includes a dup already folded into another keep, so a chain such as (A, B) then (B, C) leaves C unmerged with no warning. The shipped duplicates.csv has no chains and no unknown ids, so this does not affect today's output, but nothing guards against it. Resolve chains first, and make report.py refuse to run if any row was skipped.

**Medium: `load` overwrites spend.** A repeated supplier and customer pair replaces the earlier spend instead of adding to it. The shipped data has no repeats, but two ERPs feeding one ledger make them likely. Sum the spend per pair.

**Low: `load` accepts unknown ids.** An id missing from companies.csv creates a node with no name, and report.py would then raise a KeyError. There are none in the current data.

**Medium: the tests.** `tests/test_dedupe.py` passes while nine companies are missing from the output. Add the keep -> dup test, and add an end-to-end test on the real data that asserts every company with exactly one non-self supplier appears in the list.

I did not change any files apart from writing findings.json. The checks I ran were in memory, with no writes to the repo, and `python -m pytest tests` passes as it stands.
