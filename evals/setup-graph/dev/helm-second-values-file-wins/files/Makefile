CLUSTER ?= pollen
NS      ?= pollen

.PHONY: cluster up down forward reset

cluster:
	kind get clusters | grep -qx $(CLUSTER) || kind create cluster --name $(CLUSTER)

up:
	helm upgrade --install pollen-graph deploy/graph --namespace $(NS) --create-namespace \
		-f deploy/env/base.yaml -f deploy/env/local.yaml --wait

down:
	helm uninstall pollen-graph --namespace $(NS)

forward:
	kubectl -n $(NS) port-forward svc/pollen-graph 7687:7687

reset: down up
	./gradlew seed
