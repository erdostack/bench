Added sql/bonus_recipients.sql: the referrer at level 1 and the referrer's referrer at level 2, as in
docs/rules/referral-bonus.md, frozen or cancelled members included (the rule says they still receive it). Two
self-joins, so it runs unchanged on MariaDB and SQLite.
