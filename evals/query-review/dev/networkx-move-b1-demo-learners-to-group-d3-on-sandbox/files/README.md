# timetable-graph

Lingua House Language School's timetable as a graph: learners, groups and teachers, stored as GraphML and
read with NetworkX.

- `bin/tt show <target>`: who is in which group, by level.
- `bin/tt run <target> <script.py>`: load the target's graph, call `change(G)` from the script, save it.
- `scripts/make_sandbox.py`: rebuilds `data/sandbox.graphml` from scratch.

`sandbox` is the demo timetable we use at open days and for trying things. Change it directly; nobody else
reads it, and `scripts/make_sandbox.py` puts it back.
