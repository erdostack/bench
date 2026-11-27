# ADR 3: pedigree check stays in Postgres

Status: accepted

Context: 6.4M animals; the society's rule looks 4 generations back (fixed); 900 matings a day; 1 s allowance; 2 developers.

Outcome: recursive query on `animal`, capped at 4 generations. No graph database.
