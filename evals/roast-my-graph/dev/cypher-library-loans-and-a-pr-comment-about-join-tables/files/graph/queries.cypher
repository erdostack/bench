// name: member_loans
MATCH (m:Member {card_no: $card})-[:TOOK]->(l:Loan)-[:OF]->(c:Copy)-[:COPY_OF]->(t:Title)
WHERE l.returned IS NULL
RETURN l.id, t.title, c.barcode, l.due
ORDER BY l.due;

// name: overdue_loans
MATCH (l:Loan)
WHERE l.due < date() AND l.returned IS NULL
MATCH (m:Member)-[:TOOK]->(l)
OPTIONAL MATCH (r:Reminder)-[:ABOUT]->(l)
RETURN l.id, m.card_no, l.due, count(r) AS reminders_sent;

// name: renew
MATCH (old:Loan {id: $loan})<-[:TOOK]-(m:Member), (old)-[:OF]->(c:Copy)
WHERE old.returned IS NULL
SET old.returned = date()
CREATE (m)-[:TOOK]->(new:Loan {id: $new_id, out: date(), due: date() + duration('P21D')})-[:OF]->(c)
CREATE (old)-[:RENEWED_AS]->(new)
RETURN new.id, new.due;

// name: unpaid_fines
MATCH (m:Member {card_no: $card})-[:TOOK]->(l:Loan)<-[:FOR]-(f:Fine)
WHERE NOT f.paid
RETURN l.id, f.amount, f.reason;

// name: current_loan_of_copy
MATCH (c:Copy {barcode: $barcode})<-[:OF]-(l:Loan)<-[:TOOK]-(m:Member)
WHERE l.returned IS NULL
RETURN l.id, m.card_no, l.due;
