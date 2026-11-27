Position: keep

- We decided: keep the nightly roll-up in Python over the cession rows (in-process), no graph database.
- Why it can't loop: branches stop below 0.1% of the original, and no retrocession passes on more than 60%, so each lap
  of a spiral shrinks.
- It runs in 40 s against a 2 h window.
