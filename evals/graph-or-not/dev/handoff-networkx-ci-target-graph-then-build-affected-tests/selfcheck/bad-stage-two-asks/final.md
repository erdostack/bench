Not written yet. The export has two kinds of edge, deps and tools, and docs/graph/DECISION.md doesn't say whether a
change to a tool (protoc, a linter) should select the tests of everything built with it. Should affected_tests follow
tools edges or not?
