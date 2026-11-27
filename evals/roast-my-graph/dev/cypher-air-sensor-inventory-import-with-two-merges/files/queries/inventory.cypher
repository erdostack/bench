// name: depot_devices
MATCH (d:Device)
WHERE NOT (d)-[:INSTALLED_AT]->(:Site)
RETURN d.serial, d.model, d.firmware
ORDER BY d.serial;

// name: site_devices
MATCH (s:Site {code: $site})<-[:INSTALLED_AT]-(d:Device)
RETURN d.serial, d.model, d.last_seen
ORDER BY d.last_seen;
