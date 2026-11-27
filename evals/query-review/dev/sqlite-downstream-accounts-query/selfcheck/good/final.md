Added `queries/downstream_accounts.sql`. It walks transfers forward from `:src` and returns each reachable account once, without `:src`.

The ledger has loops (accounts that pay each other in a ring, and the exchange account pays and is paid by thousands), so the recursion keeps only account ids and uses `UNION`: each account is expanded once and the query stops when no new account turns up. I looked at the plan first; both steps use `transfers_src`. From account 17 it returns 9,696 accounts in well under a second.

    ./gq -f queries/downstream_accounts.sql -p src=17
