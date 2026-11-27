// Archive the backlog: tickets closed more than two years ago (about 31 million, docs/data.md).
// Each archived ticket gets two changes, so 50,000 tickets per transaction is about 100,000 changes.
MATCH (t:Ticket)
WHERE t.status = 'closed' AND t.closedAt < datetime() - duration({years: 2})
CALL (t) {
  SET t:Archived
  REMOVE t.searchText
} IN TRANSACTIONS OF 50000 ROWS;
