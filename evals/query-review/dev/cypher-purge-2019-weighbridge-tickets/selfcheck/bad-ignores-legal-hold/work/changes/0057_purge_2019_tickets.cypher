// 0057: 2019 tickets past retention. Tickets an open claim concerns are on legal hold and stay.
MATCH (t:Ticket)
WHERE t.season = 2019
CALL (t) {
  DETACH DELETE t
} IN TRANSACTIONS OF 2000 ROWS;
