# Affected tests on PRs

Decision: in-process-library

Load the exported target graph in the CI step and walk it with networkx. It is small and arrives as a file, so a
graph database adds nothing.
