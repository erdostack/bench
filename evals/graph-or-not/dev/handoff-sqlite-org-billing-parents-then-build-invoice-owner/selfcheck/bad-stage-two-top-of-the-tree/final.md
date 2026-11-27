Added invoice_owner(conn, org_id): the group's top organisation pays for everything under it, so it walks up
parent_id to the last org that exists and returns that.
