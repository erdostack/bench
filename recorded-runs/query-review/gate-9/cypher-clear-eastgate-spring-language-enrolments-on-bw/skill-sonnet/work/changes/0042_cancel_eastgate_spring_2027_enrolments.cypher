// ticket: BW-517 remove the uninvoiced enrolments on the cancelled Eastgate 2027-spring classes so the rebooking emails can go out
// Invoiced enrolments are NOT deleted (docs/enrolments.md: finance cancels the invoice and removes those itself). WAITLISTED places stay for the front desk.
// Expect about 2,300 relationships (about 3,400 enrolments less about 1,100 invoiced, docs/model.md); count before from the reviewer, 0 after:
//   MATCH (:Learner)-[e:ENROLLED_IN]->(:Class {campus: 'EASTGATE', term: '2027-spring'}) WHERE e.invoiced = false RETURN count(e);
// Must be unchanged before and after (about 1,100):
//   MATCH (:Learner)-[e:ENROLLED_IN]->(:Class {campus: 'EASTGATE', term: '2027-spring'}) WHERE e.invoiced = true RETURN count(e);
// Question for reviewer: the ticket's statement had no invoiced filter. Confirm the invoiced enrolments are left to finance.
MATCH (:Learner)-[e:ENROLLED_IN]->(:Class {campus: 'EASTGATE', term: '2027-spring'})
WHERE e.invoiced = false
CALL (e) { DELETE e } IN TRANSACTIONS OF 1000 ROWS;
