Position: keep

Ana, we decided to keep `parent_id` and read descendants with a recursive query, and the numbers that decided it are
on the write side:

- We tried a materialised path in 2023. Moving the largest section rewrote 410k rows and blocked publishing for
  7 minutes, and it was taken out.
- Editors move pages about 25 times a minute, and the news desk re-files whole sections a couple of times a week.
- The recursive query is not slow here: 6 ms p95 for a typical section and 180 ms for the largest, against a 500 ms
  page budget, on 3.4M pages up to 14 levels deep.

A LIKE prefix query would be faster to read, but every section move turns into a rewrite of everything under it. If
readability is the worry, I can put the query in one well-commented function.
