KIND_CLUSTER ?= partsbin
NAMESPACE    ?= partsbin
RELEASE      ?= partsbin-graph

.PHONY: cluster dev-up dev-down forward template

cluster:
	kind get clusters | grep -qx $(KIND_CLUSTER) || kind create cluster --name $(KIND_CLUSTER)

dev-up: cluster
	helm upgrade --install $(RELEASE) deploy/chart \
		--namespace $(NAMESPACE) --create-namespace \
		-f deploy/values/dev.yaml --wait

dev-down:
	helm uninstall $(RELEASE) --namespace $(NAMESPACE)

forward:
	kubectl --namespace $(NAMESPACE) port-forward svc/$(RELEASE) 7687:7687 7474:7474

template:
	helm template $(RELEASE) deploy/chart -f deploy/values/dev.yaml
