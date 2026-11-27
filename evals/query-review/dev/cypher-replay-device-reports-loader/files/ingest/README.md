# ingest

Subscribes to the gateway stream and calls `load/device_report.cypher` every few seconds with the
reports received since the last call.
