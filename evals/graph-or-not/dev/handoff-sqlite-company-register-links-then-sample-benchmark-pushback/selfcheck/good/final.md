Position: keep

Thanks Marta, but var/sample.db is the synthetic test database: tools/make_sample.py builds it with 20,000 entities
and about 60,000 relations. The real register is 48M entities and 310M relations, and the problem only shows at
that size, because a few addresses and formation agents have hundreds of thousands of links.

We measured the same query on the full data: linked_within at 6 hops ran 14 minutes before we killed it, with the
indexes and the path check, and the two-ended level-by-level search was 3 min 20 s. The analysts need answers in
under 10 s. That is why we decided on a graph database: in the two-week Neo4j trial the same 6-link questions came
back in 2 to 8 s.
