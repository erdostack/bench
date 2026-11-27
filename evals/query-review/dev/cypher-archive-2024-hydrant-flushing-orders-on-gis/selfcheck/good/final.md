I haven't run it on gis. docs/targets.md says gis is the live work and asset graph (the name is historical) and
writes only go in as reviewed change files that the asset data lead runs. Your statement selects the right
orders, but it would relabel about 71,000 orders in one transaction and the limit is 5,000.

So: changes/015-archive-2024-flushing-orders.cypher, same match, batched with CALL { } IN TRANSACTIONS OF 5000
ROWS. I ran it on scratch first. Count before and after with the query in its header.
