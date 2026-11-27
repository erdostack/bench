CREATE (:Leg {flight: 'CP101', origin: 'MAN', destination: 'AMS'}),
       (:Leg {flight: 'CP102', origin: 'AMS', destination: 'MAN'}),
       (:Leg {flight: 'CP215', origin: 'AMS', destination: 'CPH'}),
       (:Leg {flight: 'CP216', origin: 'CPH', destination: 'AMS'}),
       (:Leg {flight: 'CP330', origin: 'MAN', destination: 'DUB'}),
       (:Leg {flight: 'CP331', origin: 'DUB', destination: 'MAN'});
MATCH (a:Leg), (b:Leg) WHERE a.destination = b.origin AND a.flight < b.flight
CREATE (a)-[:CONNECTS {minutes: 40 + toInteger(substring(b.flight, 4)) % 30}]->(b);
