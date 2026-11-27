# Data rules

- Every leg joins two centres that exist. The schema declares both ends of `leg` as foreign keys to
  `centre`, and `Db.kt` switches foreign-key enforcement on through `SQLiteConfig`, so a leg can never
  point at a centre that is gone. Route queries therefore need no orphan checks.
- Retiring a centre with legs fails; move or end its legs first.
- Costs are per trailer, in pence.
