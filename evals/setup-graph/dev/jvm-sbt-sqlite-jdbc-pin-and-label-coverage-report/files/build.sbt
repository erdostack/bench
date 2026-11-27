ThisBuild / scalaVersion := "3.3.4"
ThisBuild / organization := "org.propagation"

lazy val root = (project in file("."))
  .settings(
    name := "propagation",
    libraryDependencies ++= Seq(
      "org.xerial" % "sqlite-jdbc" % "3.36.0.3",
      "org.scalameta" %% "munit" % "1.0.3" % Test
    ),
    run / fork := true
  )
