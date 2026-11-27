Decision: recursive-sql

6 ms p95 against a 3 s budget leaves a factor of 500. Even a tenant 40x bigger with deeper inheritance won't come
close, so SQLite stays and Kofi's graph store is not needed.
