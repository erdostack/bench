# staylist

Hotel search and booking history. The API embeds LadybugDB; one writer process applies changes, the
API reads.

    schema/schema.cypher      node and relationship tables
    queries/search.cypher     search and hotel page
    queries/account.cypher    guest account and reviews

## Sizes

| Table | Rows |
|---|---|
| Hotel | 38,000 |
| Amenity | 64 |
| HotelAmenity | 1.3 million (about 34 per hotel) |
| Guest | 4.2 million |
| Booking | 19 million |
| Review | 6.1 million, each about one booking |

## Traffic

Search (`hotels_with_amenities`): a city plus up to five amenities, about 400 a second; the mobile
app will add amenity filters next month. Hotel page: `hotel_amenities` and `hotel_reviews`.
