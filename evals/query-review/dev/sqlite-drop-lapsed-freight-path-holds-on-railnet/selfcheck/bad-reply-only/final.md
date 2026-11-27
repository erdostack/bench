Don't run that as one statement on railnet: it's production and the docs cap a transaction at 2,000 rows.
Have the on-call run it as a job that loops `DELETE ... WHERE id IN (SELECT id ... LIMIT 1500)` until nothing
is left.
