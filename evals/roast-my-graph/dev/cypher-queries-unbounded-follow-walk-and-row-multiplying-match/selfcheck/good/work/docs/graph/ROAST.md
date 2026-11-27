# Roast: queries/feed.cypher

Seven queries. Five of them are minding their own business. One wants to visit every listener on the platform before lunch, and one is doing arithmetic that would get a calculator recalled.

## Findings

### 1. follower_reach (critical)

**Problem.** The star after FOLLOWS has no number on it, so the match keeps walking followers of followers until it runs out of graph. With 1.9 billion FOLLOWS that is, for any account with a handful of followers, most of the 38 million listeners, on a query with a 150 ms budget that runs on the profile screen.

**Fix.** Decide how far reach really means and say so in the pattern, e.g. `<-[:FOLLOWS*1..2]-`, or stop serving it live: compute the number in a nightly job and store it on the Listener as a property the profile reads.

### 2. listener_stats (high)

**Problem.** The second MATCH (g:Genre) shares nothing with the first one, so every play row is paired with every one of the 610 genres. plays comes back 610 times too large, genres_total is the same inflated number, and the database builds plays x 610 rows to get there.

**Fix.** Count the two things separately: `MATCH (l:Listener {id: $id}) OPTIONAL MATCH (l)-[:PLAYED]->(t:Track) WITH l, count(t) AS plays MATCH (g:Genre) RETURN l.handle, plays, count(g) AS genres_total`. Or fetch the genre total once at startup, it is 610 and it does not change per listener.

### 3. follow_suggestions (medium)

**Problem.** Two hops out from a listener who follows a very popular account can be a lot of rows before the LIMIT applies.

**Fix.** Cap the first hop (for example the 200 most recent follows by `since`) before expanding the second.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
