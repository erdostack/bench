Still stands: yes

The where-used query is not what makes the ECO impact screen slow on the numbers I can measure, so there is no case here for changing the decision. I could not find the decision record in the ecoboard repo, so I have not changed anything. I am reading "the call" as keeping where-used as the recursive SQL in sql/where_used.sql on the PLM replica, with no separate graph database or in-memory graph library. If the record says something else, check it against these numbers.

What I measured (SQLite, the same sql/where_used.sql through ecoboard.impact.where_used; production is Postgres 16, which I could not run here):

- Tree-like BOM with 1,200,000 items and 1,049,716 BOM lines, about 8% of components with two parents: where_used on 40 random components took 0.046 s to 0.099 s per call, with 1 to 25 assemblies returned.
- Denser variant with 600,000 items and 632,153 lines, 30% of components with two parents (more shared subassemblies): 25 random components took 0.024 s to 0.053 s, returning up to 171 assemblies.
- Your 1.1M lines and 1.3 s p95: the where-used step on a comparable structure is one to two orders of magnitude below that. So the screen's remaining time is most likely elsewhere (the Postgres replica, the joins that follow the query, or a small set of heavy ECOs). I did not measure the full screen, so this is a hypothesis, not a finding.

Where the call could fail: the query walks every path, not every assembly, so a random graph of many overlapping levels with an average of four or more parents per part gets slower very quickly. In a 10,000-line random test with that density, the query did not return within 100 s. Real Ostrava BOMs may be closer to the tree case, but I have not checked that. Loops are handled by the path check, and I did not test that on this data.

Suggested next steps: time where_used on the Postgres replica for the 20 slowest ECO items from the last week, log the parents-per-part distribution for the Ostrava import, and profile the whole impact() call so we know which step owns the 1.3 s before any decision is revisited.
