.PHONY: cluster up forward q

cluster:
	kind get clusters | grep -qx seedbank || kind create cluster --name seedbank

up:
	helm upgrade --install seedbank-graph deploy/chart --namespace seedbank --create-namespace \
		-f deploy/values/dev.yaml --wait

forward:
	kubectl -n seedbank port-forward svc/seedbank-graph 7687:7687

q:
	go run ./cmd/cq $(F)
