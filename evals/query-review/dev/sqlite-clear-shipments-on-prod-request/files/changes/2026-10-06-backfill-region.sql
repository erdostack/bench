-- OPS-412: sites imported before 2024 had no region. Approved by r.haddad.
UPDATE sites SET region = 'EMEA' WHERE region IS NULL AND code LIKE 'EU-%';
UPDATE sites SET region = 'AMER' WHERE region IS NULL AND code LIKE 'US-%';
