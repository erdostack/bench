# Change files

The release job applies each new `db/changes/` file with cypher-shell (auto-commit), one statement
after another. If a statement fails (a leader switch, a lock timeout, a deploy), the job retries the
whole file from its first statement, up to three times. Batches already committed by an
`IN TRANSACTIONS` statement stay committed. So a change file must leave the same result whether it
ran once, or ran partway and then again from the top.

Anything that touches more than a few thousand nodes or relationships commits in batches of at most
10,000 rows: `CALL (...) { ... } IN TRANSACTIONS OF n ROWS`.
