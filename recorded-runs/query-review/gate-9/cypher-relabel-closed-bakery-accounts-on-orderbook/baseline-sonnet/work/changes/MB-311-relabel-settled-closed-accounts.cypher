// MB-311: relabel closed accounts with a zero balance as ClosedAccount (in place of Account) so the van planner and order site stop matching them. Accounts with a non-zero balance keep Account (docs/model.md).
MATCH (a:Account)
WHERE a.status = 'closed' AND a.balancePence = 0
SET a:ClosedAccount
REMOVE a:Account;
