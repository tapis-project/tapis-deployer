# Tapis Deployment

## Startup 

Order of startup

- vault
- 


# api

  
Create a ~/tenants-config-local.json, something like this. Note that you will need to know your already created postgres password:
    
    {
      "service_name": "tenants",
      "tenants": ["dev"],
      "use_sk": true,
      "log_level": "DEBUG",
      "show_traceback": false,
      "test_jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL2RXdi5hcGkudGFwaXMuaW8vdG9rZW5zL3YzIiwic3ViIjoianN0dWJic0BkZXYiLCJ0YXBpcy90ZW5hbnRfaWQiOiJkZXYiLCJ0YXBpcy90b2tlbl90eXBlIjoiYWNjZXNzIiwidGFwaXMvZGVsZWdhdGlvbiI6ZmFsc2UsInRhcGlzL2RlbGVnYXRpb25fc3ViIjpudWxsLCJ0YXBpcy91c2VybmFtZSI6ImpzdHViYnMiLCJ0YXBpcy9hY2NvdW50X3R5cGUiOiJzZXJ2aWNlIiwiZXhwIjozMTQ5MDc4MDU2fQ.NoiGj7l8uCGhDyo-12345i5M9TKBXNb3bTzaJuTOwma9gUPTOtAO2C9yfeistsZY8fuhpCx0lL0D8Bnr3jWrGMVM_wGAKbF-fRcBEiRX6YfL0oi03MU4w2Ab9z-CD9woBdBeS93IBvelYun7yvGDmaUizFzgaVvF120vsWdJB0Y",
      "sql_db_url": "postgres://tenants:8a6e995c2aab35xyzpdq70d7dd391d64@tenants-postgres:5432/tenants"
    }

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

# test
