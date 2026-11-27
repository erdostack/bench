# Access model

Users belong to groups (`user_groups`). Groups can be members of other groups (`group_nesting`):
if group C is nested in group P, everyone in C is also in P. Departments nest their teams, projects
nest the teams working on them, and teams nest the projects they own, so nesting is not a tree and
it does go round in places.

A grant (`grants`) gives a group read access to a resource. A user can read a resource when a
group they are in, directly or through nesting, holds a grant on it.
