Position: keep

We decided to stay on Postgres with a recursive query, so Marta's suggestion matches: the CYCLE clause and a
covering index are the tuning we planned. The walk was 11.2 s with the loop and 7.9 s as a recursive query.
