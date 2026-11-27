He's wrong about the tracking page. track starts from one shipment and takes one hop to its
carrier; customer_shipments starts from one customer. Neither ever walks the carrier's 14 million
shipments, so the size of Carrier does not matter to them, and there are no concurrent writers.
Only the monthly carrier_month batch reads a carrier's whole set, and it takes 25 seconds once a
month. No CarrierMonth bucketing needed. Details in docs/graph/ROAST.md and findings.json.
