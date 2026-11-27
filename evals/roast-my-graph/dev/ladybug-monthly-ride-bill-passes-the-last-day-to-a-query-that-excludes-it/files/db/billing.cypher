// name: account_totals
MATCH (r:Ride)-[:BilledTo]->(a:Account)
WHERE a.id = $account AND r.ended_on >= $first_day AND r.ended_on < $last_day
RETURN count(r) AS rides, sum(r.minutes) AS minutes;

// name: account_statement
MATCH (p:Rider)-[:RodeOn]->(r:Ride)-[:BilledTo]->(a:Account)
WHERE a.id = $account AND r.ended_on >= $first_day AND r.ended_on <= $last_day
RETURN r.id AS ride, p.name AS rider, r.started_on AS started_on, r.ended_on AS ended_on,
       r.minutes AS minutes
ORDER BY r.ended_on, r.id;

// name: billable_accounts
MATCH (a:Account)
RETURN a.id AS id, a.company AS company, a.rate_cents_per_minute AS rate;
