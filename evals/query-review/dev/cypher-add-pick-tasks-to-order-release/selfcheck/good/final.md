Done in `cypher/release_order.cypher`. It is still one statement, takes `$orderId`, and returns the same `line, sku, qty, bins` rows.

One thing to know about where I put it. The query joins every line's product to its bins to build the `bins` list, and a product is in 2.3 bins on average (up to six, per `docs/model.md`). After that join there is a row per line and bin, so a `CREATE` just before the `RETURN` would have made a task per bin: two or three tasks for most lines. The task is therefore created right after the lines are matched, before the bins come in, and a `WITH l, p` carries on to the bin lookup as before.

Worth checking on a test order whose products sit in several bins: `PROFILE` the statement and look at the rows going into the `Create` (it should equal the number of lines), or count afterwards with `MATCH (:Order {id: $orderId})-[:HAS_LINE]->(l) RETURN l.no, COUNT { (l)-[:HAS_TASK]->() }`.

Not changed, but you may want it: releasing the same order twice creates a second set of tasks. If the handheld can retry, say so and I will make it a `MERGE` on the line.
