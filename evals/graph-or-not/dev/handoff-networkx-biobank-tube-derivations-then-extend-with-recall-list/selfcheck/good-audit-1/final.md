Added recall_list(tube_id) to tubetrack/graph.py; it normalises ids (strip, upper-case), takes every descendant in networkx and leaves destroyed tubes off while walking through them, as recorded in docs/graph/DECISION.md.

Things to decide before the lab uses this:
- Shipped tubes stay on the list. The largest recall list in the export has 50 tubes, so a shipped filter is one line.
