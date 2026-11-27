DELETE FROM edges WHERE src IN (SELECT id FROM nodes WHERE kind = 'order' AND ref LIKE 'LT-%');
DELETE FROM nodes WHERE kind = 'order' AND ref LIKE 'LT-%';
DELETE FROM nodes WHERE kind = 'customer' AND id NOT IN (SELECT dst FROM edges WHERE kind = 'placed_by');
