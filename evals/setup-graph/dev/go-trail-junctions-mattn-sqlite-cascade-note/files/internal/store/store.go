// Package store opens the trail database.
package store

import (
	"database/sql"

	_ "github.com/mattn/go-sqlite3"
)

// OpenRead opens the database read-only, for queries.
func OpenRead(path string) (*sql.DB, error) {
	return sql.Open("sqlite3", "file:"+path+"?mode=ro")
}

// OpenWrite opens the database for the loader and for closures.
func OpenWrite(path string) (*sql.DB, error) {
	return sql.Open("sqlite3", "file:"+path+"?_busy_timeout=5000")
}
