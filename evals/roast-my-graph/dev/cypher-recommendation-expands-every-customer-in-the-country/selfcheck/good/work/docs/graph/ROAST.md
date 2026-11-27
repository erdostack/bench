# Roast: neo4j/recs.cypher

Four of these five queries do their jobs and go home. The fifth one hears "popular near you" and decides the only honest way to answer is to personally interview everyone in the country.

## Findings

### 1. popular_near_you (critical)

**Problem.** The pattern walks from the shopper to their Country and straight back out to everyone else who lives there. There are nine Country nodes for 14 million customers; the biggest has 5.8 million attached. So one page view visits up to 5.8 million customers and then every one of their purchases to find the recent ones, to produce ten rows that are the same for every shopper in that country. It cannot fit in 100 ms and it will pin the replicas whenever a busy market wakes up.

**Fix.** Stop computing a per-country answer per shopper. Work it out once per country on a schedule (hourly is plenty) and store it where it can be read in one step, for example relationships (:Country)-[:TRENDING {rank, buys}]->(:Product) refreshed by a job; the page query becomes MATCH (me:Customer {id: $customer_id})-[:LIVES_IN]->(:Country)-[t:TRENDING]->(p:Product) RETURN p.sku, p.title ORDER BY t.rank LIMIT 10. A cache keyed by country in the service layer does the same job.

### 2. buy_again (low)

**Problem.** Aggregates all of a customer's purchases on each view; fine for ordinary shoppers, slower for the few with thousands of orders.

**Fix.** Leave it, or add a date cutoff on b.at.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
