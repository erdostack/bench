MATCH (d:Departure {departureId: $departureId})
RETURN d.capacity - COUNT { (d)<-[:ON]-(:Leg) } AS seatsLeft;
