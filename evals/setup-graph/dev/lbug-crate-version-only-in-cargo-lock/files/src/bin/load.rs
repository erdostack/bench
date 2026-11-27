//! load <data dir> <db dir>: recreate the database from the CSV files.

use std::path::PathBuf;

use anyhow::{bail, Result};
use tunebook::{statements, store};

fn main() -> Result<()> {
    let mut args = std::env::args().skip(1);
    let (Some(data), Some(db)) = (args.next().map(PathBuf::from), args.next().map(PathBuf::from)) else {
        bail!("usage: load <data dir> <db dir>");
    };
    if db.exists() {
        std::fs::remove_dir_all(&db)?;
    }
    let database = store::open(&db, false)?;
    let conn = store::connect(&database)?;
    for statement in statements(include_str!("../../schema/tables.cypher")) {
        conn.query(&statement)?;
    }
    for (table, file) in [("Tune", "tunes.csv"), ("TuneSet", "sets.csv"), ("IN_SET", "in_set.csv"), ("FOLLOWS", "follows.csv")] {
        conn.query(&format!("COPY {table} FROM '{}' (header=true)", data.join(file).display()))?;
    }
    Ok(())
}
