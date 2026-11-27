Position: keep

Leilani, we decided on recursive-sql. There are about 12,000 zones and the recursive query runs in 30 ms,
comfortably inside the 500 ms the controllers allow, so Neo4j would not buy us anything.
