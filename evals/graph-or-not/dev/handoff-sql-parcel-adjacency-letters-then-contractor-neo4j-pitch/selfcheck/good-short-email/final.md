Position: keep

Hi, thanks. We'll stay with what we have: the letters are a join on parcel_adjacency in our existing Postgres, decided
in ADR 0002. The bylaw only allows letters to the first ring, so multi-ring notifications won't happen. Each
application's lookup is 3 ms, and with about 150 applications a week sent in one Monday batch there is nothing for a
graph database to speed up.
