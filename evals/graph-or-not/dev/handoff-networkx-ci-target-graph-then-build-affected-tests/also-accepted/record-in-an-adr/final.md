Added ci/affected.py. affected_tests(graph, changed) builds the deps graph, takes every changed target plus everything
that depends on it through deps edges, and returns the test targets among them, sorted. tools edges are not followed:
per docs/adr/0007-affected-tests-on-prs.md, on PRs only deps count and tools-only changes are left to the nightly full run.
