# Graph

`nodes(id, kind, name, created)`; `edges(id, kind, src, dst, created)`. See `db/schema.sql`.

| node kind | what | `name` |
|---|---|---|
| `person` | a member | first and last name |
| `wall` | a person's own forum, one per person | `Wall of <name>` |
| `group` | a club or interest forum | title |
| `post` | a post in a wall or a group | first words |
| `comment` | a reply to a post or to another comment | first words |
| `tag`, `city` | | name |

| edge kind | src | dst |
|---|---|---|
| `knows` | person | person: stored once per pair, `src` is whoever sent the friend request |
| `has_interest` | person | tag |
| `is_located_in` | person | city |
| `has_member` | wall or group | person |
| `has_moderator` | wall or group | person (a wall's moderator is its owner) |
| `container_of` | wall or group | post |
| `has_creator` | post or comment | person |
| `reply_of` | comment | post or comment |
| `likes` | person | post or comment |
| `has_tag` | post or comment | tag |

Times are TEXT, `'YYYY-MM-DD HH:MM:SS'`, UTC. There are no foreign keys, so nothing stops an edge from
pointing at a node that has gone; at the moment none does.
