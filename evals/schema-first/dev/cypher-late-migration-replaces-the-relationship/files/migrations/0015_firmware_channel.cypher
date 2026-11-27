MATCH (f:Firmware) WHERE f.channel IS NULL
SET f.channel = 'stable';
