Added invoice_owner(conn, org_id): the nearest org from org_id upwards (itself first) that has a billing account
pays; if none in the chain has one, org_id itself. A missing parent ends the chain.
