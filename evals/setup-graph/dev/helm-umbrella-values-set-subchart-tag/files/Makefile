.PHONY: deploy forward

deploy:
	helm dependency build deploy/stack
	helm upgrade --install atlas deploy/stack --namespace atlas --create-namespace --wait

forward:
	kubectl -n atlas port-forward svc/atlas-graphdb 7687:7687
