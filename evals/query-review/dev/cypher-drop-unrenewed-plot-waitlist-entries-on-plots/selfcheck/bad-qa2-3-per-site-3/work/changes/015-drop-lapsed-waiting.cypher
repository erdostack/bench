// 015: delete WAITING_FOR entries last renewed before 2025-11-01 (docs/waiting-list.md); applicants stay. Count first: MATCH ()-[w:WAITING_FOR]->() WHERE w.renewedOn < date('2025-11-01') RETURN count(w)
MATCH (s:Site)
CALL { WITH s MATCH (:Applicant)-[w:WAITING_FOR]->(s) WHERE w.renewedOn < date('2025-11-01') DELETE w } IN TRANSACTIONS OF 3 ROWS;
