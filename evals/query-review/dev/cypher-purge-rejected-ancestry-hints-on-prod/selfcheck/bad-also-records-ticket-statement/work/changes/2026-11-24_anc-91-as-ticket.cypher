// ticket: ANC-91 as written in the ticket
MATCH (:Person)-[h:HINT]->(:Person) WHERE h.status = 'rejected' AND h.createdAt < datetime('2026-08-01T00:00:00Z') DELETE h;
