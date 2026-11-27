// Command server exposes /walk?from=A1&to=C7.
package main

import (
	"encoding/json"
	"net/http"

	"example.org/depotwalk/internal/config"
	"example.org/depotwalk/internal/graph"
	"example.org/depotwalk/internal/routes"
)

func main() {
	cfg := config.FromEnv()
	driver, err := graph.Open(cfg)
	if err != nil {
		panic(err)
	}
	http.HandleFunc("/walk", func(w http.ResponseWriter, r *http.Request) {
		rows, err := routes.Walk(r.Context(), driver, r.URL.Query().Get("from"), r.URL.Query().Get("to"))
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadGateway)
			return
		}
		_ = json.NewEncoder(w).Encode(rows)
	})
	panic(http.ListenAndServe(cfg.Listen, nil))
}
