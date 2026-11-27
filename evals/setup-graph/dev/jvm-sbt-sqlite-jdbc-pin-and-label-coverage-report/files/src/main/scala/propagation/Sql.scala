package propagation

import java.nio.file.{Files, Path}
import java.sql.DriverManager

/** runMain propagation.Sql <file.sql> [arg ...]: runs one read query against data/garden.db. */
@main def Sql(file: String, args: String*): Unit =
  val conn = DriverManager.getConnection("jdbc:sqlite:data/garden.db")
  try
    conn.setReadOnly(true)
    val st = conn.prepareStatement(Files.readString(Path.of(file)))
    args.zipWithIndex.foreach((a, i) => st.setString(i + 1, a))
    val rs = st.executeQuery()
    val cols = rs.getMetaData.getColumnCount
    while rs.next() do println((1 to cols).map(rs.getString).mkString("\t"))
  finally conn.close()
