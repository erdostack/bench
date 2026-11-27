-- 0042 (PB-288): permits on parcels condemned for the Route 9 widening are revoked.
UPDATE node SET status = 'revoked'
WHERE kind = 'permit' AND status = 'open'
  AND id IN (SELECT e.src FROM edge e JOIN node p ON p.id = e.dst
             WHERE e.rel = 'ON' AND p.ref IN ('APN-0907-114', 'APN-0907-115', 'APN-0907-121'));
