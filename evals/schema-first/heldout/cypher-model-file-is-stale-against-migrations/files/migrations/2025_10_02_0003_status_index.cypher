CREATE INDEX shipment_status IF NOT EXISTS FOR (s:Shipment) ON (s.status);
