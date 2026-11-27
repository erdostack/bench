I'd leave affected_by as it is; the comment has the direction of the edges backwards.

docs/model.md: an edge points from the clause that contains a cross-reference to the clause it refers to
(`12.3 -> 1.1(b)`: 12.3 says "as defined in 1.1(b)"). When 1.1(b) is amended, the clauses whose meaning can change
are the ones that refer to it, directly or through other clauses: the clauses with a path *to* it. That's
`nx.ancestors`. `nx.descendants` would give the clauses the amended clause itself refers to.

On data/references.json: amending definition 1.1(a) affects 59 clauses with ancestors; descendants returns none.
For schedule clause S3.1 it's the other way round: nothing refers to it (0), while descendants would list 25 clauses
it merely mentions. No change made; suggested reply: "edges point at the cited clause, so dependants are ancestors".
