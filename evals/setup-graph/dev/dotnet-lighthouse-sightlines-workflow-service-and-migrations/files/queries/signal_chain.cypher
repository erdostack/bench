// A chain of lights that can pass a signal from LH001 to LH018.
MATCH p = shortestPath((a:Light {code: 'LH001'})-[:SEES*..10]-(b:Light {code: 'LH018'}))
RETURN [n IN nodes(p) | n.code] AS chain, reduce(t = 0, r IN relationships(p) | t + r.km) AS km;
