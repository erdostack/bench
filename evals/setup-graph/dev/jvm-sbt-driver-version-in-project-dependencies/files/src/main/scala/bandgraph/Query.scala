package bandgraph

import java.nio.file.{Files, Path}
import org.neo4j.driver.{AuthTokens, GraphDatabase, QueryConfig, RoutingControl}
import scala.jdk.CollectionConverters._

/** Runs one saved Cypher file against Memgraph (Bolt) and prints each record. */
object Query:
  def main(args: Array[String]): Unit =
    val cypher = Files.readString(Path.of(args(0)))
    val uri = sys.env.getOrElse("BANDGRAPH_URI", "bolt://localhost:7687")
    val driver = GraphDatabase.driver(uri, AuthTokens.none())
    try
      val result = driver.executableQuery(cypher)
        .withConfig(QueryConfig.builder().withRouting(RoutingControl.READ).build())
        .execute()
      result.records().asScala.foreach(r => println(r.asMap()))
    finally driver.close()
