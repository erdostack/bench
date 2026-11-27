// ticket: BW-517 remove the uninvoiced enrolments on the cancelled Eastgate 2027-spring classes so learners can rebook
// Invoiced enrolments are left for the finance office (docs/enrolments.md). Waitlist places are left for the front desk.
// Count before (expected count, recorded by the reviewer: ____):
//   MATCH (:Learner)-[e:ENROLLED_IN]->(:Class {campus: 'EASTGATE', term: '2027-spring'}) WHERE e.invoiced = false RETURN count(e);
// Count after (0 expected):
//   MATCH (:Learner)-[e:ENROLLED_IN]->(:Class {campus: 'EASTGATE', term: '2027-spring'}) WHERE e.invoiced = false RETURN count(e);
MATCH (:Learner)-[e:ENROLLED_IN]->(:Class {campus: 'EASTGATE', term: '2027-spring'})
WHERE e.invoiced = false
CALL (e) { DELETE e } IN TRANSACTIONS OF 1000 ROWS;
