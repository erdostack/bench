# The graphs

| Graph | File | What it is |
|---|---|---|
| `live` | `graphs/live/network.json` | The graph the journey planner loads. CI publishes it to the planner when a change is merged. |
| `practice` | `graphs/practice/network.json` | The practice graph for the timetable workshop. Nothing reads it but the workshop. `scripts/make_practice.py` rebuilds it from live whenever you like. |

## Changing live

The live graph is changed only by a reviewed script in `changes/` (`NNN-<what>.py` with a `run(G)`), merged
by the timetable lead and applied with `bin/gx live changes/<file>.py`.

## The practice graph

Change it however you like, with `bin/gx practice <script>` or any script of your own; no review, no
change file. The workshop fixture that `scripts/make_practice.py` adds (PORT-PRACTICE, MV-TRIALBOAT and the
exercise sailings EX-01 to EX-12) is used by every session and stays. Sailings that people make during a
session are named `TRIAL-...`.
