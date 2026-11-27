# Roast: innkeep graph

340 hotels, 61,000 rooms, and as far as this graph is concerned a single room 101 that is somehow in all of them.

## Findings

### 1. room_number (critical)

**Problem.** The constraint says no two rooms in the graph may have the same number, and load_rooms follows it by merging on the number alone. Room numbers are per hotel: the README says so and data/sample/rooms.csv has 101 in AMS-CAN, LIS-ALF, PRG-OLD and VIE-RNG. Those cannot be four nodes, so they are one node with an IN relationship to each hotel and the floor, beds and rate_class of the last row loaded. book_room for 101 in one hotel hangs the booking on that shared node, free_rooms then hides 101 in every other hotel for the same nights, and guest_bookings returns the booking once per hotel the node is in.

**Fix.** Make the hotel part of what identifies a room. Simplest: give Room a hotel_code property, replace the constraint with one over the pair (or a single key property such as 'AMS-CAN/101'), and change load_rooms to MERGE (r:Room {hotel_code: row.hotel_code, number: row.number}). Reload rooms from the export. Bookings already hanging on a shared room cannot be told apart from the graph alone; re-attach them from the booking engine's own records.

### 2. free_rooms (medium)

**Problem.** For every room of the hotel it checks all bookings the room has ever had. At 9 million bookings a year that list only grows.

**Fix.** Once rooms are separate, keep past bookings out of the check (for example a relationship type for upcoming stays only, or archive bookings after check-out).

### 3. book_room (medium)

**Problem.** Nothing in the statement checks that the room is still free; two guests booking the same room at once both succeed.

**Fix.** Do the availability check and the create in one transaction that first takes a lock on the room, and return nothing when the room is taken.

### 4. Room.number (low)

**Problem.** Stored as text, so ORDER BY r.number puts 1001 before 101 and 12 before 2.

**Fix.** Fine if numbers like 12A exist; otherwise store a number.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
