# kyc-owners

Ownership lookups for business onboarding: given a company, who ultimately owns or controls it.

- Python 3.12. PostgreSQL 16 holds the company register copy, refreshed daily from the registry feed.
- `sql/ubo.sql` is the ownership walk; `kyc/ubo.py` runs it for the onboarding screen.
