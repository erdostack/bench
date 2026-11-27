// name: load_newsletters
UNWIND $rows AS row
MERGE (n:Newsletter {slug: row.slug})
SET n.title = row.title, n.writer = row.writer;

// name: load_subscribers
UNWIND $rows AS row
MERGE (s:Subscriber {email: row.email, plan: row.plan})
SET s.name = row.name, s.country = row.country, s.joined_on = date(row.joined_on);

// name: load_subscriptions
UNWIND $rows AS row
MATCH (s:Subscriber {email: row.email})
MATCH (n:Newsletter {slug: row.newsletter})
MERGE (s)-[r:SUBSCRIBED_TO]->(n)
SET r.since = date(row.since);

// name: load_issues
UNWIND $rows AS row
MATCH (n:Newsletter {slug: row.newsletter})
MERGE (i:Issue {id: row.id})
SET i.subject = row.subject, i.SentAt = datetime(row.sent_at)
MERGE (i)-[:partOf]->(n);

// name: load_opens
UNWIND $rows AS row
MATCH (s:Subscriber {email: row.email})
MATCH (i:Issue {id: row.issue_id})
MERGE (s)-[o:OPENED]->(i)
ON CREATE SET o.at = datetime(row.at);
