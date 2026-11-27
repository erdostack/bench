Added visible_people(conn, person_id) to directory/profiles.py.

It applies the DPO's rule from docs/graph/DECISION.md: the viewer sees people they currently share a team with, and
a team only counts if it has at most 40 current members. Ended memberships (left_at set) count for nothing, not for
who is in a team and not for its size. The viewer is left out. One query, no graph store.
