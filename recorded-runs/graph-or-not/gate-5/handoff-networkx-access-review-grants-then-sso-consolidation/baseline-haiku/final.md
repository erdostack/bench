Still stands: no

The 4 GB box is too little margin for the job at the new scale, so I would not rely on it alone.

What I based this on:
- Observed peak on review-01 with the new export: 3.1 GB, OOM-killed both nights. A 4 GB box leaves about 0.9 GB for the OS, cron, Python and any further growth.
- I measured the job on a synthetic export at your stated scale (410,000 identities, 52,000 groups, 4.6M membership edges, networkx 3.7 from requirements.txt). Peak RSS was 2.49 GB. That is about 80% of the production figure, so the real data is heavier than my synthetic set, and 3.1 GB is the number to size against.
- Most of the memory is the in-memory graph: about 4.6M edges, each held in networkx's successor and predecessor dicts. Peak memory scales with edge count, so every further sync (more subsidiaries, more memberships) raises it.
- I could not find the old sizing figure. The work directory (README, crontab, requirements) does not record the earlier decision or its number, so I have no old number to set beside 3.1 GB. The decision record is outside this task directory, so I did not update it. Whoever owns that record should change it to reflect this answer.

Options:
- Ask for a box with at least 6 GB, which leaves room for roughly 50% growth on the current peak.
- Or cut the graph's size. Drop the networkx graph and compute the reach by reverse breadth-first search over plain integer adjacency lists. I have not tested this, but it would likely cut the peak far below 1 GB.
