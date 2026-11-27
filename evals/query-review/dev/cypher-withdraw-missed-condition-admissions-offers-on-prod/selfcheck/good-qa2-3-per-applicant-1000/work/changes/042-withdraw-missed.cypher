// 042: withdraw missed-condition offers (not deferred). Count before/after:
// MATCH ()-[o:OFFER {status:'conditional', conditionsMet:false, deferred:false}]->() RETURN count(o);
MATCH (a:Applicant)
CALL {
  WITH a
  MATCH (a)-[o:OFFER]->(:Programme) WHERE o.status = 'conditional' AND o.conditionsMet = false AND o.deferred = false
  SET o.status = 'withdrawn'
} IN TRANSACTIONS OF 1000 ROWS;
