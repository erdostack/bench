// 015: delete WAITING_FOR entries last renewed before 2025-11-01 (docs/waiting-list.md); applicants stay. Count first: MATCH ()-[w:WAITING_FOR]->() WHERE w.renewedOn < date('2025-11-01') RETURN count(w)
:param cut => date('2025-11-01');
MATCH (:Applicant)-[w:WAITING_FOR]->(:Site) WHERE w.renewedOn < $cut
CALL (w) { DELETE w } IN TRANSACTIONS OF 1000 ROWS;
