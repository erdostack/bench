"""Case-local helper: drop SQL comments before handoff_lib runs a file.

handoff_lib finds the :named parameters a statement uses after blanking quoted strings, and it does not
skip comments, so an apostrophe in a comment ("-- the submission's authors") opens a "string" that hides
the parameters after it and a correct file fails with "You did not supply a value". Comments are removed
here, outside quoted strings and quoted names, before the file reaches handoff_lib. Nothing else changes."""


def strip_comments(sql: str) -> str:
    out, i, n, quote = [], 0, len(sql), None
    while i < n:
        ch = sql[i]
        if quote:
            out.append(ch)
            if ch == quote:
                if i + 1 < n and sql[i + 1] == quote:   # doubled quote inside a literal
                    out.append(sql[i + 1])
                    i += 1
                else:
                    quote = None
        elif ch in "'\"`":
            quote = ch
            out.append(ch)
        elif sql.startswith("--", i):
            j = sql.find("\n", i)
            i = n if j == -1 else j
            continue
        elif sql.startswith("/*", i):
            j = sql.find("*/", i + 2)
            out.append(" ")
            i = n if j == -1 else j + 2
            continue
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def install(handoff_lib) -> None:
    original = handoff_lib.run_sql

    def run_sql(build, sql, params, scratch_parent, *args, **kwargs):
        return original(build, strip_comments(sql), params, scratch_parent, *args, **kwargs)

    handoff_lib.run_sql = run_sql


if __name__ == "__main__":
    assert strip_comments("SELECT 1 -- it's\nFROM t WHERE a = :x") == "SELECT 1 \nFROM t WHERE a = :x"
    assert strip_comments("SELECT '--not a comment', :y /* the user's */ FROM t") == "SELECT '--not a comment', :y   FROM t"
    assert strip_comments("SELECT 'it''s' -- x\n") == "SELECT 'it''s' \n"
    print("ok")
