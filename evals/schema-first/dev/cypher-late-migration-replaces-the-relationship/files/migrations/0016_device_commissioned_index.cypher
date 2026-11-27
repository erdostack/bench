CREATE INDEX device_commissioned IF NOT EXISTS FOR (d:Device) ON (d.commissionedOn);
