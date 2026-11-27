- `(:Member)-[:TOOK]->(:Loan {id, out, due, returned})-[:OF]->(:Copy)-[:COPY_OF]->(:Title)`
- `(:Fine {amount, reason, paid})-[:FOR]->(:Loan)`: overdue and damage fines.
- `(:Reminder {sent, channel})-[:ABOUT]->(:Loan)`: each reminder letter or e-mail.
- `(:Loan)-[:RENEWED_AS]->(:Loan)`: a renewal closes the old loan and opens a new one, so the chain shows
  how long a member really kept a copy.
