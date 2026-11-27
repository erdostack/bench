plugins {
    java
}

repositories { mavenCentral() }

java { toolchain { languageVersion.set(JavaLanguageVersion.of(21)) } }

dependencyLocking { lockAllConfigurations() }

dependencies {
    implementation("org.postgresql:postgresql:42.7.+")
}

tasks.register<JavaExec>("sql") {
    description = "Run one query file: ./gradlew sql -Pfile=<file.sql>"
    classpath = sourceSets["main"].runtimeClasspath
    mainClass.set("org.waymarks.RunSql")
    args(project.findProperty("file") ?: error("pass -Pfile=<file.sql>"))
}

tasks.register<JavaExec>("load") {
    description = "Recreate the tables and load data/*.csv"
    classpath = sourceSets["main"].runtimeClasspath
    mainClass.set("org.waymarks.Load")
}
