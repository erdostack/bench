Decision: in-process-library

Keep Kofi's query. It answers the question, inside the window, and it was reconciled to the cent. Notes in
docs/graph/DECISION.md.

- The spirals are handled by the cut-off: a branch is dropped below 0.1% of the original, and since no retrocession
  passes on more than 60%, a share after k laps is at most 0.6^k, below 0.1% within 14 steps. The walk ends.
- 40 seconds against a 2 hour window, on 21,000 cession rows and chains up to 9 deep.
- A graph database would need the same cut-off (an unbounded path pattern over a spiral never ends either) and a
  second copy of the treaty data.
