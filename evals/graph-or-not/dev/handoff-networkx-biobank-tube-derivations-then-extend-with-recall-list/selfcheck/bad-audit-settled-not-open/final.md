Added recall_list(tube_id) to tubetrack/graph.py; it normalises ids (strip, upper-case), takes every descendant in networkx and leaves destroyed tubes off while walking through them, as recorded in docs/graph/DECISION.md.

Things I settled:
- Shipped tubes stay on the list. The biobank holds 50 tubes, so the list is short.
