Decision: recursive-sql. I wrote it up in docs/graph/DECISION.md.

A graph database is not warranted. The rule looks 4 generations back and no further, so the check touches at most 30
ancestors per animal (2 + 4 + 8 + 16) however deep the pedigree goes (23 generations on record). That is a bounded
walk over `animal.sire_id` / `animal.dam_id`, which are both indexed, on the Postgres you already run: a recursive
query with a generation counter capped at 4, run once for the sire and once for the dam, then intersect. At about 900
matings a day and a one second allowance there is no load to speak of. With 2 backend developers and no graph
database experience, a second datastore holding a copy of 6.4M animals would be all cost. Loading the herd book into
application memory is ruled out for the same reason in reverse: 6.4M rows held to answer a 30-row question.

Nothing was built; say the word and I'll write the query.
