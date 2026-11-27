UPDATE edges SET dst = (SELECT id FROM nodes WHERE code = 'OLT-KB2') WHERE kind = 'served_by' AND dst = (SELECT id FROM nodes WHERE code = 'OLT-KB1');
