//! Opening the embedded database.

use std::path::Path;

use anyhow::{Context, Result};
use lbug::{Connection, Database, SystemConfig};

/// Opens the database directory. Read-only unless the caller is the loader.
pub fn open(path: &Path, read_only: bool) -> Result<Database> {
    let config = SystemConfig::default().read_only(read_only);
    Database::new(path, config).with_context(|| format!("opening {}", path.display()))
}

pub fn connect(db: &Database) -> Result<Connection<'_>> {
    Connection::new(db).context("connecting")
}
