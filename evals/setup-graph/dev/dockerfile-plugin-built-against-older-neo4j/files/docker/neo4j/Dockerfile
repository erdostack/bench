FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /src
COPY pom.xml .
COPY plugin plugin
COPY app app
RUN mvn -q -B -pl plugin -am package -DskipTests

FROM neo4j:2026.05.0-enterprise
ENV NEO4J_ACCEPT_LICENSE_AGREEMENT=yes \
    NEO4J_dbms_security_procedures_unrestricted=parcel.*
COPY --from=build /src/plugin/target/parcel-procedures.jar /plugins/
