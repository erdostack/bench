Done. LAB-31 is now merged into LAB-07 in scratch (live untouched).

I followed the merge steps in `docs/labs.md`. All 179 of LAB-31's `sent_to` edges now point at LAB-07 with their `sent_on` and `fee` kept. LAB-07 keeps its own name ("Brightsmile Dental Lab") and city, and the LAB-31 node and its `in_city` edge are gone. Nodes went from 2427 to 2426 and edges from 4789 to 4788. LAB-07 now has 829 `sent_to` edges (650 + 179).

In the lab spend report, Brightsmile is now the top lab at 129,643.00. The merge script is `changes/merge_lab31_into_lab07.py`. If you want the pre-merge numbers back, `python3 tools/build_scratch.py` rebuilds scratch.
