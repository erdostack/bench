# Roast: crumb invoicing

Denormalisation with a reason, maybe.

## Findings

### 1. Invoice.bill_to_name (medium)

**Problem.** Denormalised customer attributes on Invoice (name, address, VAT number) duplicate Customer and risk update anomalies.

**Fix.** Consider normalising: keep the details on Customer only, or add a sync step when Customer changes.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
