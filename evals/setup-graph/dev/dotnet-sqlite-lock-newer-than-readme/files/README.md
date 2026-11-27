# meeplenet

Board-game designers and the games they co-designed (generated), as two SQLite tables: designer and credit.
Co-design paths and "designer distance" are recursive CTEs in sql/.

- .NET, Microsoft.Data.Sqlite 8.0.8
- Database: data/meeple.db, built by `make load` from data/*.csv
- `make q F=sql/designer_distance.sql`
- Schema: sql/schema.sql
