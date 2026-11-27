Position: keep

We decided on a graph database. var/sample.db is a small synthetic database (20,000 entities, about 60,000
relations), so a 0.4 s timing on it tells us little about the real register: recursive queries over many hops
blow up as the data grows, and graph databases are built for exactly this kind of multi-hop question.
