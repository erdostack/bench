# shopgraph

Customers of the webshop and everything attached to them, in Neo4j 5.26.

See `model/model.md` for every relationship type. Duplicate customer accounts (same person, two sign-ups) are
merged by support with `merge/merge_customers.cypher`; about 300 merges a week. A merge must leave the kept
account with everything both accounts had: the customer should not notice anything except that their two
accounts are now one.
