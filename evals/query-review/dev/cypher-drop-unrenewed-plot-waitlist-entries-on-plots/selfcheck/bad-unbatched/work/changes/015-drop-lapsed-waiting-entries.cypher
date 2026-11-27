// 015: delete WAITING_FOR entries last renewed before 2025-11-01
MATCH (:Applicant)-[w:WAITING_FOR]->(:Site)
WHERE w.renewedOn < date('2025-11-01')
DELETE w;
