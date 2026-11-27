# monorepo CI tooling

Scripts the CI pipeline runs around the build tool. Python 3.12, standard library plus `networkx`.

- `ci/export_graph.sh` asks the build tool for the target graph and writes `var/graph.json` (not committed).
  The format is described in `ci/EXPORT_FORMAT.md`.
- `ci/run_tests.py` runs the test targets for a pipeline.
