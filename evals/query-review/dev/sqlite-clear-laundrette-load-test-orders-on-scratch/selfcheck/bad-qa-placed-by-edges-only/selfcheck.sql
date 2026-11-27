DELETE FROM edges WHERE kind = 'placed_by' AND src IN (SELECT id FROM nodes WHERE kind = 'order' AND ref LIKE 'LT-%');
DELETE FROM nodes WHERE kind = 'order' AND ref LIKE 'LT-%';
