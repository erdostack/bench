# Review

The job lacks resilience. Add retries and a dead-letter folder.

## load_offers.cypher (medium)

Problem: No error handling: transaction failures abort the job; violates resilience best practices.

Fix: Wrap execute_write in try/except with retries and dead-letter the failing file.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
