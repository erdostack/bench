# Offers

```
(:Applicant {applicantId, name})-[:OFFER {status, conditionsMet, deferred, madeAt}]->(:Programme {code, title})
```

- `status`: `conditional`, `unconditional`, `declined` or `withdrawn` (STRING).
- `conditionsMet`: BOOLEAN, set on every conditional offer from the exam results feed. `false` until the
  results show the conditions are met.
- `deferred`: BOOLEAN, always set. `true` for an offer of a place a year later than the cycle it was made in.
- `madeAt`: DATE.
- An applicant holds at most five offers (one per choice); a programme can hold several thousand.

## Results day

Once the results feed has run, conditional offers whose conditions were not met are withdrawn, so the
places go to clearing: `status` becomes `withdrawn` and nothing else on the offer changes (the decision log
records when). Deferred offers are the exception: their conditions are assessed against next year's
results, so they are never withdrawn on this year's, whatever `conditionsMet` says. They stay as they are.
