# Offers

`nodes.kind` is `applicant` or `programme`. An `applied_to` edge goes from an applicant to a programme,
with `cycle` (the entry year), `status` and, once an offer is made, `reply_by`.

| status | meaning |
|---|---|
| `pending` | no decision yet |
| `offer` | an offer is out and the applicant has not replied |
| `firm` | the applicant accepted the offer |
| `declined` | the applicant declined it |
| `expired` | the applicant did not reply by `reply_by` |
| `rejected` | no offer |

`reply_by` is the last day the applicant may reply, as text `YYYY-MM-DD`. An offer whose `reply_by` is
today can still be accepted today; from the day after, an unanswered offer is `expired`. The nightly
expiry job sets that; nothing else changes on the edge.
