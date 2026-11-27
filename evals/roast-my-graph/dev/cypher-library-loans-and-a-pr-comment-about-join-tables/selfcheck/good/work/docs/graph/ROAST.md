# Review

He's not right, and I wouldn't spend the sprint. Loan isn't just linking a member to a copy: fines,
reminder letters and renewals all point at a specific loan, and renewals chain loans together. If Loan
were a relationship, none of those would have anything to attach to (a relationship can't have
relationships). The extra hop is the price of being able to say "this fine is for that loan". Keep it.

## overdue_loans (low)

Problem: Reads every unreturned loan with a past due date; fine for a nightly letter run, not for a page.

Fix: Keep it in the nightly job.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
