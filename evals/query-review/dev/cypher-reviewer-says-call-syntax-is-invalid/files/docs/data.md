# Data

| | |
|---|---|
| `Ticket` | 46 million, 31 million of them closed more than two years ago |
| `Message` | 610 million, on average 13 per ticket |
| `Customer` | 3.8 million |

## Retention

Tickets closed more than two years ago are archived: they get the `Archived` label (the desk app hides
archived tickets from its default views) and lose `searchText`, the concatenated message text that only
the full-text index uses. Messages stay. Change 0057 does the backlog; afterwards the nightly job keeps up.

Keep one transaction under about 200,000 changes.
