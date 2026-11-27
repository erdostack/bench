I added `reports/unstaffed_units.sql`. It takes `:as_of` and returns `id` and `name` for every unit that is open on that date and has no direct assignment on it. Results are ordered by name, like `assignments_by_unit.sql`.

- **Open unit:** `opened_on <= :as_of` and `closed_on` is NULL or `>= :as_of`.
- **Unstaffed:** no `assignment` row on that unit with `start_date <= :as_of` and `end_date` NULL or `>= :as_of`.
- **Direct only:** it never looks at `parent_id`, so people in units below don't count. Each unit is checked on its own, which means no recursion was needed.

I tested it on a small in-memory SQLite database built from `db/schema.sql`, with `:as_of` set to 2024-06-01. The cases were:

- A unit with an assignment (excluded).
- A unit whose assignment ended the day before (included).
- A unit that closed on `:as_of` (included).
- A unit that closed earlier (excluded).
- A unit not yet opened (excluded).
- A parent whose only staff are in a child unit (included).

All came out as intended. I couldn't run it on the real `var/unitbook.db` because it isn't in the repo. I left `docs/graph/DECISION.md` and all other files unchanged.

I read "empty" for `closed_on` and `end_date` as NULL, as in `db/schema.sql`. Rows holding an empty string would be treated as dates and not as open or ongoing.
