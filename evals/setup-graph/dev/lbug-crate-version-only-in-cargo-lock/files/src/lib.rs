//! tunebook: tunes, sets and what follows what.

pub mod store;

/// Splits a `.cypher` file into statements, dropping comments and blank statements.
pub fn statements(text: &str) -> Vec<String> {
    text.lines()
        .filter(|line| !line.trim_start().starts_with("//"))
        .collect::<Vec<_>>()
        .join("\n")
        .split(';')
        .map(str::trim)
        .filter(|statement| !statement.is_empty())
        .map(str::to_owned)
        .collect()
}

#[cfg(test)]
mod tests {
    use super::statements;

    #[test]
    fn comments_and_blank_statements_are_dropped() {
        let got = statements("// first\nMATCH (t:Tune) RETURN t.name;\n\n;\n");
        assert_eq!(got, vec!["MATCH (t:Tune) RETURN t.name".to_owned()]);
    }
}
