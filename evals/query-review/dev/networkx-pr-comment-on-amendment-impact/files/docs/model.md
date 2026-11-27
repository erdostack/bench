# Reference graph

Each clause is a node. An edge points from the clause that contains a cross-reference to the clause it refers to:
`12.3 -> 1.1(b)` means "clause 12.3 says 'as defined in clause 1.1(b)'".

When a clause is amended, every clause that relies on it may change meaning: the clauses that refer to it, the
clauses that refer to those, and so on. The amendment checker lists them for legal to re-read. Definitions refer
to each other, so the graph has cycles.
