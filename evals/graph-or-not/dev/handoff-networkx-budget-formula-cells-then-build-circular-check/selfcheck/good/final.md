Rewrote circular_cells in sheets/circular.py as recorded in docs/graph/DECISION.md: the references go into a
networkx DiGraph, and every strongly connected component that is a real loop (more than one cell, or a cell
that refers to itself) is flagged, unless the whole loop is on the Loan sheet, which finance computes
iteratively on purpose. Cells that only read a loop are not flagged. Signature unchanged. You'll need
networkx in requirements.txt; I left that file alone.
