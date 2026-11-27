# Model

| Relationship | From | To | Reads as |
|---|---|---|---|
| `REPORTS_TO` | `Employee` | `Employee` | the first employee's line manager is the second |
| `IN_TEAM` | `Employee` | `Team` | home team; exactly one per employee |
| `BASED_AT` | `Employee` | `Site` | main place of work |

Node keys: `Employee.staff_no`, `Team.code`, `Site.code`.
Other properties: `Employee.full_name`, `Employee.managment_level` (1 = chief executive, 9 = no reports and
no approval rights), `Employee.active`, `Team.name`, `Site.city`.

The chief executive is the only employee with no `REPORTS_TO`.
