// MB-311: relabel closed AND settled (balancePence = 0) accounts as ClosedAccount in place of Account, so the planner and order site stop seeing them (docs/model.md). Closed accounts with a non-zero balance keep Account for the statements run. Question for reviewer: confirm status 'closed' + exact zero balance is the intended set (the ticket text says every closed account).
MATCH (a:Account {status: 'closed'}) WHERE a.balancePence = 0
WITH a LIMIT 5000
SET a:ClosedAccount
REMOVE a:Account;
