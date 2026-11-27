Position: keep

We decided on a join on parcel_adjacency in Postgres. The lookup takes 40 ms, we get about 600 applications a week,
and the table has 9M adjacency rows, which Postgres handles fine. Multi-ring notifications are not planned.
