// 015: delete WAITING_FOR entries last renewed before 2025-11-01 (docs/waiting-list.md); applicants stay. Count first: MATCH ()-[w:WAITING_FOR]->() WHERE w.renewedOn < date('2025-11-01') RETURN count(w)
CALL apoc.periodic.iterate('MATCH (:Applicant)-[w:WAITING_FOR]->(:Site) WHERE w.renewedOn < $cut RETURN w', 'DELETE w', {batchSize: 1000, params: {cut: '2025-11-01'}});
