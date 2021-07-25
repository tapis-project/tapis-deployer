# postgres 

Create a little script that will create the kube secrets. (generate your own password e.g. `openssl rand -hex 16`): 

    echo "kubectl create secret generic tenants-postgres-secrets --from-literal=tenants-postgres-password=123450dee03227899327ba991b14b315" > ~/tenants-secrets


Create volume:

    kubectl apply -f pvc.yml

Wait for volume to be up (bound):

    kubectl get pvc
    postgres-vol01      Bound    pvc-6d1019a8-4c68-4c29-b387-e055293bb4a9   1Gi        RWO            rbd            4h45m

Wait for chown-pvc job to be done (1/1):

    kubectl get jobs
    chown-pvc       1/1           24s        4h46m

Deploy postgres:

    kubectl apply -f postgres.yml

Deploy util:

    kubectl apply -f util.yml


Wait for pods to be up (Running):

    kubectl get pods
    postgres-584dfc84f-4df7t                       1/1     Running             0          2s


Create service:

    kubectl apply -f service.yml

