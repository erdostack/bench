Wrote queries/friends.sql. Per the closure rule in docs/graph/DECISION.md it leaves out friends whose account is
closed (looked up by label in account_state, code 2) and keeps suspended and pending ones; friendships are stored
once with the smaller id first, so it matches the member in either column. I also return no rows when the member's
own account is closed, since a closed account has no Friends tab to show; tell me if you want that case listed.
