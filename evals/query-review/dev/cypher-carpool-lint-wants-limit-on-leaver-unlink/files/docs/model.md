# Graph model

- `(:Student {studentId, name, leftOn})`: `leftOn` (DATE) is set when the child leaves the
  district's schools; absent for current pupils.
- `(:Student)-[:RIDES_IN {since}]->(:Carpool)`: the carpools a child is on. The pickup sheets and
  the drivers' lists are built from it.
- `(:Family)-[:PARENT_OF]->(:Student)`, `(:Family)-[:MEMBER_OF]->(:Carpool)`.

About 64,000 `RIDES_IN` relationships still belong to children who have left (the old admin tool
never removed them); drivers keep getting them on their lists.
