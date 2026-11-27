# syntax=docker/dockerfile:1

# Build libsqlite3 ourselves so the query runner does not depend on whatever the base image carries.
FROM golang:1.23-bookworm AS sqlite
ARG SQLITE_VERSION=3.46.1
ARG SQLITE_TARBALL=sqlite-autoconf-3460100
ARG SQLITE_YEAR=2024
RUN curl -fsSL "https://www.sqlite.org/${SQLITE_YEAR}/${SQLITE_TARBALL}.tar.gz" | tar xz \
 && cd "${SQLITE_TARBALL}" \
 && CFLAGS="-O2 -DSQLITE_DQS=0" ./configure --prefix=/opt/sqlite --disable-static \
 && make -j"$(nproc)" && make install

FROM golang:1.23-bookworm AS build
COPY --from=sqlite /opt/sqlite /opt/sqlite
ENV CGO_ENABLED=1 CGO_CFLAGS="-I/opt/sqlite/include" CGO_LDFLAGS="-L/opt/sqlite/lib -lsqlite3"
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
# -tags libsqlite3: link the library built above instead of the copy bundled with the driver
RUN go build -tags libsqlite3 -o /out/stopq ./cmd/stopq

FROM debian:bookworm-slim
COPY --from=sqlite /opt/sqlite/lib/ /usr/local/lib/
RUN ldconfig
COPY --from=build /out/stopq /usr/local/bin/stopq
WORKDIR /work
