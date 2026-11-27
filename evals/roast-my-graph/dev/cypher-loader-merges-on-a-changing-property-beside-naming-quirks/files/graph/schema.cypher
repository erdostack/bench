CREATE CONSTRAINT newsletter_slug IF NOT EXISTS FOR (n:Newsletter) REQUIRE n.slug IS UNIQUE;
CREATE CONSTRAINT issue_id IF NOT EXISTS FOR (i:Issue) REQUIRE i.id IS UNIQUE;

CREATE INDEX subscriber_email IF NOT EXISTS FOR (s:Subscriber) ON (s.email);
