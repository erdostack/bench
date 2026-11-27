import sbt._

object Versions {
  val bolt  = "5.28.1"
  val munit = "1.1.1"
}

object Dependencies {
  val boltDriver = "org.neo4j.driver" % "neo4j-java-driver" % Versions.bolt
  val munit      = "org.scalameta" %% "munit" % Versions.munit
}
