DELETE FROM edges WHERE src IN (SELECT id FROM nodes WHERE ref LIKE 'lt-%');
