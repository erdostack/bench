I haven't written netplan/critical.py yet. docs/graph/DECISION.md says we use networkx in the nightly job, but nothing
in the repository says what makes a stop "critical" for ops: the most boardings, the most lines through it, the most
shortest paths through it, or something else? Tell me the definition and I'll write it.
