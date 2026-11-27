# Graph model

- `(:Family {familyId, email, surname})`
- `(:Family)-[:PARENT_OF]->(:Student {studentId, name})`
- `(:Family)-[:MEMBER_OF]->(:Carpool {carpoolId, status})`
- `(:Carpool)-[:DRIVES]->(:Route)`
