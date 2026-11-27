MATCH p = (a:Depot {code: 'NTH'})-[:LEG *BFS ..8 (e, n | NOT e.closed)]->(b:Depot {code: 'QAY'})
RETURN [d IN nodes(p) | d.code] AS depots;
