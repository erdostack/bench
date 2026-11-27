Position: keep

Tomas, two problems with the change:

1. Depth: our nesting goes 14 levels deep (all-company down through divisions and departments to teams). A cap of 10
   would silently drop the members of the deepest lists from mail to all-company.
2. UNION won't save us once there's a depth column: on a loop each lap produces the same list with a new depth, so the
   rows are never identical and UNION doesn't remove them. With 37 loops in the config today, every one of them would
   be walked round until the cap.

The path guard costs nothing: expansion is 3 ms p95 against the 500 ms delivery allows. So we keep sql/expand.sql as it
is (recursive SQL, decided when Pia proposed Neo4j).
