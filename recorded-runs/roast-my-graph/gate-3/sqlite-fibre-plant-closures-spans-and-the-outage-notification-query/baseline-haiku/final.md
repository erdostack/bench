Do not wire `connected_closures` into the outage tool as it is. It has two critical problems, and I checked both against plant.db.

1. It never finishes. The recursive step can step back along the same span (closure 1 to 2 and back to 1), and each step adds one to the hop count. UNION only removes rows that repeat both the closure and the hop count, so nothing stops the loop. I ran it on plant.db: it was still running after 20 seconds and I stopped it. The comment in the file says the walk cannot come back, which is wrong. During an incident the operator would wait on a query that does not return. A fixed version that remembers the previous closure and caps the hop count returned the same closures and hop counts as a plain breadth-first search for 7 start points, with no mismatches, in under 0.02 seconds each.

2. It texts the wrong customers. The walk does not respect direction, so from any closure it reaches the exchange and then the whole area. For 200 random closures in plant.db, every one returned all 1,300 closures in its area and would text 4,944 customers in North or 4,056 in East. A single damaged pole would text a whole exchange. The walk needs to go only downstream from the fault, which means each closure needs a parent toward its exchange (N-0000 or E-0000), set when the data is loaded. Please confirm that downstream is the intended scope before this goes into the tool.

Two smaller items: `customers_on.sql` expects a JSON array of closure ids, but nothing in the repo produces one from the walk. And `span_report.sql` assumes no span crosses exchanges, which holds today but is not enforced.

The rest checks out. plant.db has 2,400 closures and 2,398 spans in two components (North and East), each a tree, so the README's "no rings" claim holds for this data. There are no orphaned spans or customers.

The full list is in `findings.json` in the repo root.
