Done in the sandbox graph (graphs/sandbox.json) only. live.json was not touched.

- I moved all 7 `feeds` links from RLY-HILLTOP to RLY-BEACON: TX-18, TX-12, TX-32, TX-09, TX-07, TX-15 and TX-28. Each link kept its band, km and channel exactly as before.
- None of those transmitters was already fed by Beacon, so nothing clashed. Beacon now feeds 12 transmitters (5 before, 7 added).
- RLY-HILLTOP still has its other links: the studio link in, the backhaul from RLY-MARSH in, and the backhaul out to RLY-RIDGE. I only moved the `feeds` links, as you asked.
- Node and edge totals are unchanged (44 nodes, 45 edges).

The km values are the old Hilltop distances. If you want the model to reflect Beacon's real distance to each transmitter, those would need updating. Channels may also need a look, since Beacon's existing feeds now share its mast with the new ones. `bin/reset-sandbox` puts the sandbox back to live.
