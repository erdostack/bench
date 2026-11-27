.PHONY: load q

load:
	rm -f data/meeple.db
	sqlite3 data/meeple.db < sql/schema.sql
	sqlite3 data/meeple.db ".import --csv --skip 1 data/designer.csv designer" ".import --csv --skip 1 data/credit.csv credit"

q:
	dotnet run --project src/Meeple.Sql -- $(F)
