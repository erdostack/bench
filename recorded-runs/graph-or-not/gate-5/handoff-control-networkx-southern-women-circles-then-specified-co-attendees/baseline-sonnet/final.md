I added `co_attendees(name, min_shared)` in `society/circles.py`. It reads the data with `society.data.load_attendance()` and returns the sorted names of the other women who share at least `min_shared` events with `name`. It returns an empty list when no one qualifies, and `name` is never in its own result.

Two behaviours to know about:
- If `name` isn't in the attendance list, it raises `KeyError`, the same as `circles_page` does. I did that instead of returning an empty list so a typo in a name doesn't look like "no co-attendees". Say so if you'd rather have `[]`.
- Events are counted once per woman, so a repeated row in the CSV can't inflate the count. A `min_shared` of 0 or less returns every other woman.

I ran it on `data/attendance.csv` for a few names and thresholds, including one so high that nothing matched (empty list) and an unknown name (`KeyError`). The repo has no test suite, so I didn't add tests.
