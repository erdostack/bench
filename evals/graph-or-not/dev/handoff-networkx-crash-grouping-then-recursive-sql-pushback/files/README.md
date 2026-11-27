# crashdesk

Crash report intake and triage for the mobile apps.

- Python 3.12; Postgres 16 holds reports and the links between them.
- `jobs/` are the nightly batch jobs, run by cron on the batch box. `jobs/group_crashes.sql` groups reports into
  issues before the morning triage stand-up.
