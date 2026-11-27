# Circular-reference warning

Decision: in-process-library

## Workload facts (from the conversation, 2026-11-23)

- Workbook: 9 sheets, 14,000 cells, 31,000 references. The check runs on every save.
- networkx simple_cycles over the whole workbook: about 60 ms; found 5 loops to flag, the current check finds 1
  (it only pairs two cells on the same sheet; misses a 3-cell loop on Costs, two cross-sheet loops, and a cell
  that refers to itself).
- Finance's rules:
  - flag every cell on a loop, anywhere in the workbook, including a cell that refers to itself;
  - EXCEPT loops that stay entirely on the Loan sheet: intentional, computed iteratively;
  - cells that only read from a loop are not flagged.

## Options considered

- graph-database: rejected; a server in the save path.
- in-process-library: chosen; networkx in sheets/circular.py.
- recursive-sql: rejected; cycle membership is awkward and slow as recursion.
- no-graph: rejected; loops can be any length.

## What would change the decision

- Workbooks large enough that the check no longer fits in the save path (seconds, not milliseconds).
