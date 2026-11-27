# Fare classes

Since the fares change of 2026-03-01 every booking has a `fareClass`: `standard`, `concession`,
`island-resident` or `flexi`. The booking site sets it when the booking is made.

Bookings made before 2026-03-01 had no fare class. The March migration (change 044) gave one to the
roughly 11,000 old bookings that the old discount table shows were sold at a concession or residents'
fare, and left the others without one. Every one of those others was sold at the standard fare, so its
fare class is `standard`.

A booking's fare class is what it was sold at: once a booking has one, nothing changes it.
