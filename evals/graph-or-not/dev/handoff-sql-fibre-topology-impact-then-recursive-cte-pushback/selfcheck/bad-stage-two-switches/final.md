Position: switch

Marta's right that Postgres 16 handles recursive walks well: the CYCLE clause stops loops on the rings and a
covering index on link(a_end, b_end) makes each step an index-only scan. That keeps us on one system, which is
worth a lot. Let's try it before adding anything.
