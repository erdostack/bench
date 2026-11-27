Still stands: yes

What we decided (docs/decisions/mutual-connections.md): stay on Postgres with the intersection query, and revisit
when it passes 50 ms p95 in prod. It was 7 ms p95 then, on 3.1M connections and 90 views a second; it is 19 ms now,
on 9.8M connections and 240 views a second. 19 ms is under the 50 ms line, and the panel's budget is 100 ms. The
merger didn't cross the line we set, so there is no reason to start a migration. I'd tell Lena exactly that, with
the line, rather than argue about graph databases in general.
