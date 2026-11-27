// name: carrier_month
MATCH (s:Shipment)-[b:SHIPPED_BY]->(c:Carrier {code: $carrier})
WHERE s.created >= $from AND s.created < $to
RETURN b.service AS service, count(*) AS shipments, sum(s.charged_eur) AS charged
ORDER BY service;
