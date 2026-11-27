// name: next_approver
MATCH (c:Claim {ref: $ref})<-[:SUBMITTED]-(:Employee)-[:REPORTS_TO*1..8]->(boss:Employee)
WHERE boss.approval_limit >= c.amount
WITH c, boss ORDER BY boss.grade ASC LIMIT 1
MERGE (c)-[:AWAITS]->(boss)
RETURN boss.staff_no AS approver;

// name: approve
MATCH (c:Claim {ref: $ref})-[w:AWAITS]->(e:Employee {staff_no: $staff_no})
CREATE (e)-[:APPROVED {at: datetime()}]->(c)
DELETE w
SET c.status = 'approved';
