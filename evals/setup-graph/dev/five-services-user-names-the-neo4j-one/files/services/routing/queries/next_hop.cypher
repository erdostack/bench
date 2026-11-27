// First depot after $origin on the cheapest route to $destination.
MATCH path = (a:Depot {code: $origin})-[:LINK *WSHORTEST (r, n | r.minutes)]->(b:Depot {code: $destination})
RETURN nodes(path)[1].code AS next_hop;
