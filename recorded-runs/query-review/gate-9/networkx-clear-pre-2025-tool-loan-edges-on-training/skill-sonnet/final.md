Done. I deleted 1,203 `borrowed` edges from `training`, the loans that went out before 1 January 2025. The graph went from 2,883 to 1,680 edges. I only changed `training`. `catalogue`, the production graph the app reads, was not touched.

**What stayed:** all 525 nodes (members, tools and branches), including `FM-0999`, whose only loan was in 2024 and who now has nothing attached. Every `reserved` and `kept_at` edge stayed, and so did every loan that went out on or after 2025-01-01. The New Year's Day loan (`FM-0008`, `FT-1004`, out 2025-01-01) stayed, and the New Year's Eve one (`FM-0007`, `FT-1003`, out 2024-12-31) went.

**The change:** `scripts/drop_old_training_loans.py`. It removes every `borrowed` edge whose `on` date is before 2025-01-01. `docs/targets.md` lets you change `training` directly with `bin/tg training apply`, so I did that after trying it on a temporary copy.

**Target:** NetworkX 3.7 on `data/training.graphml`.

**Rule:** delete `borrowed` edges with `on < 2025-01-01`, which means the day the loan went out. A loan that came back after the cutoff doesn't count. Sources: your request and `docs/model.md`.

**Numbers, from the copy and then the real file:**
- should change: 1,203 of 2,403 `borrowed` edges. job changed: 1,203. same rows: yes (the removed edges match the independent selection exactly, with their attributes).
- other rows or tables changed: 0. The nodes and their attributes are identical, and nothing was added.
- largest transaction: not applicable, as this is a file rewrite.
- second run: changes nothing (deleted 0).
- After: 1,200 `borrowed`, 260 `reserved` and 220 `kept_at` edges.

**Check you can rerun:**
```
python3 bin/tg training stats
```
It should show 525 nodes and `'borrowed': 1200`.

**Before Thursday:** `scripts/build_training.py` rebuilds the graph from its fixed seed, so running it brings the old loans back. If you rebuild, run the cleanup script again afterwards with `bin/tg training apply scripts/drop_old_training_loans.py`.
