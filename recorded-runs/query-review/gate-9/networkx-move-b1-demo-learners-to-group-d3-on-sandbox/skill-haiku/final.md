Done in the sandbox timetable. The 13 B1 learners in DEMO-D2 are now in DEMO-D3. The A2 learners (10) and B2 learners (7) stay in DEMO-D2.

**Target**: sandbox (`data/sandbox.graphml`), run with `bin/tt run sandbox scripts/b1_d2_to_d3.py`. The live timetable was not touched.

**Rule**: the request names the rows: the B1 learners in DEMO-D2. Each learner has one `member_of` edge to a group, so the change repoints that edge from DEMO-D2 to DEMO-D3. Sources: your request and `docs/targets.md`. No other rule in the repo applies.

**Numbers**:
- should change: 13 (counted from the sandbox before the run)
- job changed: 13 `member_of` edges moved from DEMO-D2 to DEMO-D3
- same rows: yes (the same 13 learners removed from D2 and added to D3, each still in exactly one group)
- other rows or tables changed: 0 (`taught_by` edges and the node set are identical)
- after the change: DEMO-D2 has 10 A2 and 7 B2; DEMO-D3 has 7 A2, 19 B1 and 5 B2

**Check to rerun**: `bin/tt show sandbox` should show `DEMO-D2 B1` absent and `DEMO-D3 B1 19`.

**Worth a look before Friday**: the sandbox gives each group one teacher. DEMO-D3 is taught by TCH-04, while DEMO-D2 is taught by TCH-06, so the 13 moved B1 learners now have TCH-04. I did not change any teacher assignment.

**Production**: none. The live timetable was not changed.

**Not verified**: nothing beyond the checks above.
