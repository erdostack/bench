MATCH p = (lender:Station)-[:CAN_LEND*1..2]->(target:Station {code: 'ST04'})
RETURN lender.name AS lender, [r IN relationships(p) | r.appliance] AS appliances,
       reduce(t = 0, r IN relationships(p) | t + r.minutes) AS minutes
ORDER BY minutes
