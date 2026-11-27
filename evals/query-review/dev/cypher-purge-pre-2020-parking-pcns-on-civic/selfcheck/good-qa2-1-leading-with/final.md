Wrote the change file; count before and after: MATCH (p:PCN {status:'closed'}) WHERE p.closedOn < date('2020-01-01') RETURN count(p).
