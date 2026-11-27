Decision: in-process-library. Written up in docs/adr/0007-affected-tests-on-prs.md.

The question is reverse reachability over 12k targets and 70k edges that arrive as a JSON file on every pipeline:
load it, reverse the deps edges, walk from the changed targets, keep the tests. In memory that is milliseconds, well
inside the 30 s you have after the 20 s export, and networkx is already in requirements-ci.txt. A hosted graph
database would need loading from the same export on every pipeline before it could answer anything. There is no SQL
database in this picture. Following deps edges only, per the rule agreed with release; tools-only changes are left
to the nightly full run.
