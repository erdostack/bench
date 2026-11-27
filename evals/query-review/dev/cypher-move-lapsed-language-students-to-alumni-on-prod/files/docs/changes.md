# Changing data

Nobody changes `prod` from a shell. A data change is a file `changes/V<nn>__<what>.cypher` (next number)
whose first line is `// ticket: <id> <what it does>`, followed by the count query that shows the change
worked. It is reviewed in a pull request and run by the school's systems contractor with
`bin/lh prod --file changes/<file>`.

Lessons are registered in prod while a change runs, so a change commits at most **5,000 nodes per
transaction** (a node relabelled or updated counts once): `CALL { ... } IN TRANSACTIONS OF n ROWS`.
