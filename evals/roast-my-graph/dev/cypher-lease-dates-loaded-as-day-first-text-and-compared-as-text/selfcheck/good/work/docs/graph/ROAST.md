# Roast: leasebook graph

A lease register that believes the 15th of anything comes before the 31st of everything.

## Findings

### 1. load_leases (critical)

**Problem.** starts and ends are stored as the text that is in the CSV, and the CSV writes dates as day/month/year (01/09/2024, 31/08/2026). Nothing converts them; compare toInteger(row.monthly_rent) two lines below. Every comparison on them is then a comparison of text, read from the left: day of month first, then month, then year. expiring_leases asks for ends between $from and $to and gets the leases whose text happens to sort between the two strings, so a lease ending 14/02/2027 and one ending 14/02/2019 are treated alike, and the ORDER BY lists by day of month. rent_roll_on has the same comparison on both ends. Renewal letters go to the wrong tenants and finance's monthly figure is wrong.

**Fix.** Store dates: split the text in the load and build a date from the three parts (year, month, day), for starts and ends alike; run the same conversion once over the existing Lease nodes; have the portal pass date values for $from, $to and $day. Then add an index on Lease.ends for the renewal desk.

### 2. rent_roll_on (medium)

**Problem.** Reads every Lease to find those in force on one day. Monthly, 96,000 leases: tolerable, but it grows with every year of history.

**Fix.** Once ends is a real date, index it and start from the leases that end on or after $day.

### 3. unit_card (low)

**Problem.** Counts all leases a unit has ever had on every page view.

**Fix.** Fine at this size.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
