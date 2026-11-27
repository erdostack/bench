// name: listener_card
MATCH (l:Listener {id: $id})
RETURN l.handle AS handle, l.joined_at AS joined_at;

// name: recent_plays
MATCH (l:Listener {id: $id})-[p:PLAYED]->(t:Track)-[:BY]->(a:Artist)
RETURN t.title AS title, a.name AS artist, p.at AS at
ORDER BY p.at DESC
LIMIT 50;

// name: mutual_follows
MATCH (a:Listener {id: $a})-[:FOLLOWS]->(m:Listener)<-[:FOLLOWS]-(b:Listener {id: $b})
RETURN m.handle AS handle
LIMIT 100;

// name: follower_reach
// How many people could end up seeing something this listener shares: their followers,
// the followers of those, and so on.
MATCH (me:Listener {id: $id})<-[:FOLLOWS*]-(fan:Listener)
RETURN count(DISTINCT fan) AS reach;

// name: listener_stats
// Profile header: plays in the window, plus the number of genres for the
// "explored x of y genres" badge.
MATCH (l:Listener {id: $id})-[:PLAYED]->(t:Track)
MATCH (g:Genre)
RETURN l.handle AS handle, count(t) AS plays, count(g) AS genres_total;

// name: genres_explored
MATCH (l:Listener {id: $id})-[:PLAYED]->(:Track)-[:IN_GENRE]->(g:Genre)
RETURN count(DISTINCT g) AS explored;

// name: follow_suggestions
MATCH (me:Listener {id: $id})-[:FOLLOWS]->(:Listener)-[:FOLLOWS]->(them:Listener)
WHERE them <> me AND NOT (me)-[:FOLLOWS]->(them)
RETURN them.handle AS handle, count(*) AS via
ORDER BY via DESC
LIMIT 20;
