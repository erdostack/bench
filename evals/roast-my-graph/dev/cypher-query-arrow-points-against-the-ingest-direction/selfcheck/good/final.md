The big one: services_on_host has the RUNS_ON arrow backwards. It asks for host -> service, but the model doc, the ingest and owners_to_page all have service -> host, so it returns an empty list for every host, and the incident bot will read that as nothing being affected. One-character fix, in the roast.

Also lurking: host_by_serial filters on Host.serial, which has no index or constraint, so each of the 600 calls a second looks at every host. Add a uniqueness constraint (or an index) on Host.serial.

docs/graph/ROAST.md and findings.json are written. The other four queries check out against the model.
