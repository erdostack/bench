// name: audience_size
MATCH (n:Newsletter {slug: $slug})<-[:SUBSCRIBED_TO]-(s:Subscriber)
RETURN count(s) AS subscribers;

// name: plan_mix
MATCH (n:Newsletter {slug: $slug})<-[:SUBSCRIBED_TO]-(s:Subscriber)
RETURN s.plan AS plan, count(*) AS subscribers
ORDER BY subscribers DESC;

// name: recent_issues
MATCH (n:Newsletter {slug: $slug})<-[:partOf]-(i:Issue)
RETURN i.id AS id, i.subject AS subject, i.SentAt AS sent_at
ORDER BY i.SentAt DESC
LIMIT 20;

// name: issue_opens
MATCH (i:Issue {id: $issue_id})<-[:OPENED]-(s:Subscriber)
RETURN count(s) AS opened;

// name: subscriber_card
MATCH (s:Subscriber {email: $email})
OPTIONAL MATCH (s)-[:SUBSCRIBED_TO]->(n:Newsletter)
RETURN s.name AS name, s.plan AS plan, s.country AS country, collect(n.slug) AS newsletters;
