I filled in the level on 42 swimming lessons in the practice database. Live was not touched.

**What changed:** the 42 lessons whose level was empty and whose code ends in S1 to S7 now have level 1 to 7, matching the stage in the code (for example `LS-WYF-SAT-0930-S3` gets level 3). Nothing else changed: the other rows, the pools, the instructors, the swimmers and all the links are the same.

**What I left alone, and why:**
- 20 adult and aquafit lessons (codes ending `AD` or `AQ`) still have no level. `docs/model.md` says these have no level.
- 22 lessons already have a level that differs from their code. `docs/model.md` says a level set by the instructor is right even when the code says otherwise, so I did not overwrite them.

**Numbers:** should change 42 · job changed 42 · same rows yes (each changed lesson now has the level its code gives) · other rows or tables changed 0.

**Practice only:** `live` and the change files are unchanged. This is the practice copy, so there was no review step. If someone rebuilds the practice database with `scripts/build_practice.py`, it returns to the generated data, which has no levels on about a third of the lessons.
