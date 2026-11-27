Added sql/controlled_companies.sql per the recursive-sql decision.

Control is a stake of 25% or more at every step. The query starts from the client's direct stakes, follows holding
recursively with the same filter, and keeps the fewest steps per company. UNION removes duplicate rows, so each
company comes out once. The client's own company is excluded.
