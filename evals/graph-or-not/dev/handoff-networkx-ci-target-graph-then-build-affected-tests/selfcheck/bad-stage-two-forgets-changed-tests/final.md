Added ci/affected.py: walks deps edges only (tools-only changes go to the nightly run, see docs/graph/DECISION.md) and
returns the tests that depend on the changed targets.
