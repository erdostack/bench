# Review

The model stops being a graph below the feeder: transformer and meter supply links are id lists in a
property, so every outage question reads every meter. Make them SUPPLIES relationships like the
substation-feeder links and traverse from the tripped asset.

## upstream_ids (high)

Which feeder feeds a transformer and which transformer feeds a meter are kept as lists of ids on the nodes. The outage queries therefore cannot start at the tripped asset and follow its links: they read all 2.1 million meters (and 380 thousand transformers for a feeder) and check each list, with an operator waiting. Nothing checks that the ids in the lists exist either.

Fix: Load the links as relationships: (f:Feeder)-[:SUPPLIES]->(t:Transformer) for each feeder id and (t)-[:SUPPLIES]->(m:Meter). Then outage_by_feeder is MATCH (:Feeder {id: $feeder_id})-[:SUPPLIES]->(t)-[:SUPPLIES]->(m) RETURN count(DISTINCT t), count(m).

Roasted with erdostack: npx skills add usergraphtheory/erdostack
