# airnet

Inventory of ~3,000 air-quality sensors. The vendor portal exports a nightly JSON feed of devices;
`import/run.sh` sends it to Neo4j 5.26 as the `$rows` parameter of import/import_devices.cypher (one
transaction).

Feed notes:
- Rows without `serial` are the vendor's synthetic test pings. They are not devices and must be ignored.
- Devices waiting in our depot (bought, not yet installed) are in the feed with `site_code` missing.
  The inventory screen must list them (`depot_devices`).
- Test data used during development only had installed devices.
