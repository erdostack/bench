// Package config reads settings from the environment.
package config

import "os"

type Config struct {
	GraphURI      string
	GraphUser     string
	GraphPassword string
	Listen        string
}

func FromEnv() Config {
	return Config{
		GraphURI:      getenv("DEPOTWALK_GRAPH_URI", "bolt://localhost:7687"),
		GraphUser:     "neo4j",
		GraphPassword: os.Getenv("DEPOTWALK_GRAPH_PASSWORD"),
		Listen:        getenv("DEPOTWALK_LISTEN", ":8080"),
	}
}

func getenv(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}
