// Bags whose inbound flight landed less than the minimum connection time before the outbound left.
MATCH (b:Bag)-[:ARRIVED_ON]->(inb:Flight), (b)-[:BOOKED_ON]->(outb:Flight)
WHERE duration.between(inb.onBlock, outb.offBlock).minutes < outb.minConnectMinutes
RETURN b.tag, inb.number, outb.number, duration.between(inb.onBlock, outb.offBlock).minutes AS minutes
ORDER BY minutes;
