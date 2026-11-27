UPDATE edges SET dst = (SELECT id FROM nodes WHERE code = 'ST-STO') WHERE dst = (SELECT id FROM nodes WHERE code = 'ST-HUN');
