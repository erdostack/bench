Added ci/affected.py as decided (networkx in the CI step). It follows deps and tools edges, since the release team
requires a tool change to retest everything built with it, and returns the affected test targets sorted.
