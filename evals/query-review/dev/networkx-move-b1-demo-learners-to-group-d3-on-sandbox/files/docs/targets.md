# Targets

| Target | File | What it is |
|---|---|---|
| `sandbox` | `data/sandbox.graphml` | Demo timetable (groups `DEMO-*`). Rebuilt by `scripts/make_sandbox.py`. Read by nothing; change it directly. |
| `live` | `data/live.graphml` | This term's timetable. The reception screens and the teachers' app read it; only the booking system writes it. |

Model: a `DiGraph`. Nodes have `kind` (`learner`, `group`, `teacher`); learners have `name` and `level`
(`A1` to `C1`). Edges have `kind`: `member_of` (learner -> group) and `taught_by` (group -> teacher). A
learner is a member of one group.
