# piste-planner

The "get me there" route planner behind the resort app: from where you are to a hut, a lift or the car park, by the
easiest pistes you are allowed on.

- Python 3.12, FastAPI, `networkx`. Runs as a service in the resort's Kubernetes cluster.
- The lift and piste network is in `data/resorts/*.yaml`, edited by the resort's ops team. It is loaded into memory
  when a pod starts.
