package ferrylink

import java.nio.file.{Files, Path}
import java.sql.DriverManager

/** Runs one .sql file against data/ferry.db and prints each row tab-separated. */
object Sql:
  def main(args: Array[String]): Unit =
    val sql = Files.readString(Path.of(args(0)))
    val con = DriverManager.getConnection("jdbc:sqlite:data/ferry.db")
    try
      val rs = con.createStatement().executeQuery(sql)
      val n = rs.getMetaData.getColumnCount
      while rs.next() do println((1 to n).map(i => rs.getString(i)).mkString("\t"))
    finally con.close()
