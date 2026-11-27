Decision: recursive-sql

Keep the hierarchy where it is. The nightly rollup takes about 2 minutes against the 20-minute point at which ops agreed to reopen the storage question, and the account-page subtree query is 12 ms p95 against 150 ms. Both traversals are recursive SQL on indexed tables, and both are well inside those limits, so a graph database would add a second system and a sync from the nightly load for no measured gain. Change nothing for now.

The number that matters most is the rollup headroom: 10 times. Its cost grows with invoice rows, not with the depth of the hierarchy, and the invoice count is not in the repo. If invoice volume grows about 10 times, a linear extrapolation puts the rollup near 20 minutes. The first thing to try then is to sum invoices once per organisation and roll the sums up the tree, which removes the repeated join. That is a remedy to run and measure, not a tested result.

Not known: the invoice row count and how fast it is growing, whether the CRM can produce a loop (the code assumes not), and whether the two figures are single runs or logged percentiles. The timings in the repo are from synthetic data, not the production file, so the figures above are the ones you gave.

Nothing in the repo was changed except the new file docs/graph/DECISION.md.
