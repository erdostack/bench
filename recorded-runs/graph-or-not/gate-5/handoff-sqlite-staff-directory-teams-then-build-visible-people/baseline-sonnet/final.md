I added `visible_people(conn, person_id)` to the end of `directory/profiles.py`. It returns a list of ids. I didn't touch anything else.

It follows the same rule as the existing `can_view`:
- A person is visible if they share a current team with `person_id`, meaning both have `left_at IS NULL`, and that team has at most `MAX_SHARED_TEAM_SIZE` (40) distinct current members.
- Bigger teams (company-wide, offices) make nobody visible, and ended memberships count neither for who is in a team nor for its size.
- `person_id` itself is left out, and ids are de-duplicated, so a rejoiner with several rows appears once.
- Order is not specified.

I checked it against `can_view` on a small in-memory database. The data included a team of more than 40, a team that had ended, a rejoiner with duplicate rows, and a person with no teams. For every person I tried, `visible_people` returned exactly the ids that `can_view` accepts. It is one query, with no per-person calls.

The team `kind` column (team, project, location, company) isn't used, because `can_view` doesn't use it either. If the decision was that only some kinds should count, `can_view` and this function would both need that filter.
