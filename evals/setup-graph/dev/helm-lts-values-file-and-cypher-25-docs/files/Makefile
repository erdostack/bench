.PHONY: deploy forward

deploy:
	helm upgrade --install payflow-graph deploy/chart --namespace payflow --create-namespace \
		-f deploy/values/support.yaml --wait

forward:
	kubectl -n payflow port-forward svc/payflow-graph 7687:7687
