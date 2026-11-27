Decision: recursive-sql

Do not move the unit tree into a graph database, and do not add a graph library. A recursive query in the existing SQLite file does this job.

Why:
- The data is tiny: about 1,900 units, at most 8 levels, 23,000 people. A rollup over that is a few thousand rows of work.
- It runs once a month plus the odd rerun, so there is no performance case for a second system.
- `unit.parent_id` is already indexed (`unit_parent`) and assignments are indexed by unit, so SQLite can do this directly. SQLite supports recursive CTEs, and the repo is standard library only.
- A graph database would mean a second store, a nightly sync from the HR system, and new things to run and secure, for a question that is one recursive query.

What I added: `reports/headcount_rollup.sql`, run the same way as the other reports:

    python -m orgunits.run reports/headcount_rollup.sql as_of=2025-06-30

It lists each unit with the number of people assigned to it or to any unit below it on `:as_of`, using the same assignment date rules as `assignments_by_unit.sql`. I checked it on a small made-up tree in a throwaway SQLite file (which I deleted afterwards): ended and future-dated assignments were excluded and parents summed correctly. I did not have the real `var/unitbook.db`, so I have not timed it on real data.

Things to confirm:
- A person with assignments in two units under the same parent is counted once for that parent (`COUNT(DISTINCT person_id)`). If HR wants assignment counts instead, change that to `COUNT(a.id)`.
- Like the existing report, it lists every unit, including closed ones, which will show zero. Filter on `closed_on` if the pack should hide them.
- If unit data could ever contain a cycle (a unit that is its own ancestor), this query would not terminate. With `UNION ALL` and a clean tree it is fine; tell me if the HR feed cannot guarantee a clean tree and I will add a depth limit of 8.

Revisit only if the requirements change substantially, for example relationship queries across many different kinds of links, or interactive exploration at scale. Neither is in this request.
