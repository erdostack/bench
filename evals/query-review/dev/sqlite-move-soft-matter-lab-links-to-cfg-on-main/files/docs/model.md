# Model

`nodes(id, kind, key, name)`

| kind | key |
|---|---|
| `person` | staff number, `P<digits>` |
| `group` | `G-<code>` |
| `department` | `D-<code>` |
| `paper` | DOI |

`edges(id, rel, src, dst)`, one row per (rel, src, dst)

| rel | from | to |
|---|---|---|
| `MEMBER_OF` | person | group |
| `AFFILIATED` | paper | group the work was done in |
| `PART_OF` | group | department |
| `AUTHORED` | person | paper |
