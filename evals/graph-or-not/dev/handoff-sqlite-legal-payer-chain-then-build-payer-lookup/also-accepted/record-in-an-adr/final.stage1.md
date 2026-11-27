Decision: recursive-sql. Written up in docs/adr/0007-paying-account-for-consolidated.md.

The graph here is the legal chain only: account_link rows with kind 'legal', 61k of them over 240k accounts, at most
7 links deep. Once a month, in a 2 hour window, the run needs each account's top legal parent: a recursive query
that follows `child_id -> parent_id` for kind 'legal' until there is no parent. The index on (parent_id, kind) is
the wrong way round for walking upwards, but (child_id, kind) is the primary key, so each step is a key lookup.
A graph database would be a second store to keep in sync for a monthly job that needs seven lookups per account.
parent_account_id is ignored, as you said: it is the unmaintained CRM import.
