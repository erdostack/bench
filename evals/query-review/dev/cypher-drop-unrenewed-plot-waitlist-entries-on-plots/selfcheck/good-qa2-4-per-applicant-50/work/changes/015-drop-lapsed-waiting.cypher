// 015: delete WAITING_FOR entries last renewed before 2025-11-01 (docs/waiting-list.md); applicants stay. Count first: MATCH ()-[w:WAITING_FOR]->() WHERE w.renewedOn < date('2025-11-01') RETURN count(w)
MATCH (a:Applicant)
CALL (a) { MATCH (a)-[w:WAITING_FOR]->(:Site) WHERE w.renewedOn < date('2025-11-01') DELETE w } IN TRANSACTIONS OF 50 ROWS;
