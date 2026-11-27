//! tq --db <dir> <file.cypher>: run one saved query read-only and print the rows, tab separated.

use std::path::PathBuf;

use anyhow::Result;
use clap::Parser;
use tunebook::{statements, store};

#[derive(Parser)]
struct Args {
    /// database directory
    #[arg(long, default_value = "var/tunebook.lbug")]
    db: PathBuf,
    /// a .cypher file with one read query
    file: PathBuf,
}

fn main() -> Result<()> {
    let args = Args::parse();
    let db = store::open(&args.db, true)?;
    let conn = store::connect(&db)?;
    for statement in statements(&std::fs::read_to_string(&args.file)?) {
        let result = conn.query(&statement)?;
        println!("{}", result.get_column_names().join("\t"));
        for row in result {
            let cells: Vec<String> = row.iter().map(|value| value.to_string()).collect();
            println!("{}", cells.join("\t"));
        }
    }
    Ok(())
}
