# Graph model

    (:Assembly {sku, name})-[:CONTAINS {quantity}]->(:Assembly | :Part)
    (:Part {sku, description, discontinued})
    (:Supplier {name})-[:SUPPLIES {lead_time_days}]->(:Part)

An assembly is also labelled `:Part` when it is sold on its own, which is why `where_used.cypher` matches on
`:Assembly` for the container and `:Part` for the thing contained.

`CONTAINS` never forms a cycle; the nightly import rejects a file that would create one.
