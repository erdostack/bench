# parcelboard

Parcel tracking and carrier reporting. The API embeds LadybugDB and opens `data/parcels.lbug`
read-only; `load/nightly.py` rebuilds that file every night from the warehouse export with COPY FROM,
one process, and the API switches to the new file when it is done.

    schema/schema.cypher    node and relationship tables
    queries/app.cypher      the API's queries
    queries/batch.cypher    the monthly reconciliation job

## Sizes

| Table | Rows |
|---|---|
| Carrier | 7; the largest has 14.2 million shipments |
| Depot | 220 |
| Customer | 380,000; the largest has 61,000 shipments |
| Shipment | 31 million (18 months kept) |
| SCANNED_AT | about 4 per shipment |

## Workload

- Tracking page: `track`, about 300 a second in November and December.
- Customer portal: `customer_shipments`, about 20 a second.
- `carrier_month`: on the 2nd of every month, once per carrier, to compare against the carrier's
  invoice. About 25 seconds per carrier.
