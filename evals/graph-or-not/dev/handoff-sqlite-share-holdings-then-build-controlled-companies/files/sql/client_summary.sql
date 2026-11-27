SELECT c.id, c.name, c.registry_no, c.country, cl.manager
FROM client cl
JOIN company c ON c.id = cl.company_id
WHERE cl.id = :client_id;
