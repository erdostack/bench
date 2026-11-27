Done in the sandbox: `bin/tt run sandbox scripts/move_b1_to_d3.py` moved the B1 learners of DEMO-D2
to DEMO-D3 (their old member_of edge removed, a new one to DEMO-D3). The A2 and B2 learners are still in DEMO-D2;
`bin/tt show sandbox` shows D2 with only A2 and B2 now. live wasn't touched.
