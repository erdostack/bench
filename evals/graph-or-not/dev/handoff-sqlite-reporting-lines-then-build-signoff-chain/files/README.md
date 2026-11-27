# signoff

Sign-off for expense claims and leave requests. The HR app exports the people directory to a SQLite file
(schema in `db/schema.sql`) once an hour; this service reads it.

- `hr/approvals.py`: who approves what.
- `hr/messages.py`: the text of the approval emails.

Python 3.11+, standard library only.
