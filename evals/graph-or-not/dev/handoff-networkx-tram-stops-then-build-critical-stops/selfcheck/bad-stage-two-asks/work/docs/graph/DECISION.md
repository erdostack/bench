# Critical stops

Decision: in-process-library

Use networkx inside the nightly report job. The network is small and the report is a batch job, so a graph
database is not worth running and SQL is the wrong tool for a whole-network question.
