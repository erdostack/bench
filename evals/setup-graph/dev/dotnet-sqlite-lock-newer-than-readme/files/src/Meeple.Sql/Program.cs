using Microsoft.Data.Sqlite;

// Runs one .sql file against data/meeple.db (opened read-only) and prints each row tab-separated.
if (args.Length < 1)
{
    Console.Error.WriteLine("usage: Meeple.Sql <file.sql> [designer]");
    return 2;
}
using var con = new SqliteConnection("Data Source=data/meeple.db;Mode=ReadOnly");
con.Open();
using var cmd = con.CreateCommand();
cmd.CommandText = File.ReadAllText(args[0]);
if (args.Length > 1) cmd.Parameters.AddWithValue("$designer", args[1]);
using var reader = cmd.ExecuteReader();
while (reader.Read())
{
    var cells = Enumerable.Range(0, reader.FieldCount).Select(i => reader.GetValue(i)?.ToString());
    Console.WriteLine(string.Join("\t", cells));
}
return 0;
