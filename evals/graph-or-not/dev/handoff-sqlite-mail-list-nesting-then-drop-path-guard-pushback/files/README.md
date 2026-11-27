# relay-lists

List expansion for the mail relay. The relay keeps a SQLite copy of the list config (`db/schema.sql`), synced
from the directory, and expands a list into mailboxes when a message arrives (`relay/expand.py`,
`sql/expand.sql`).
