The slowness and the random-looking suggestions both come from `suggest` in `clubgraph/suggest.py`. The fix is one filter: walk friend edges only.

- Slow: `suggest` walks through interest nodes, so every call touches every user who likes an interest. The README puts `music` at about 1.3 million users. Measured here on a synthetic hub: 65 ms at 100,000 fans and 275 ms at 300,000. Extrapolated to prod, `music` alone is about 1.2 s against the 100 ms budget. A friend-only walk took 0.06 ms on the 300,000-fan hub.
- Random-looking: shared interests are scored the same as mutual friends, and ties go to whoever was loaded first. In the sample, 32 of 2,000 suggestions (1.6%) have no mutual friend. Synthetic ties came out in load order.
- The files disagree on the purpose: the README says "friend suggestions", the docstring says "neighbours they share". Someone needs to decide whether interests belong in this box.
- Tests cover only a graph with no interests, so none of this is caught.
- Not checked: production itself. The prod-scale timing is an extrapolation from synthetic data on this machine.
- Roast written to `/run/work/docs/graph/ROAST.md`; `findings.json` in the repo root has four findings (one high, two medium, one low).
